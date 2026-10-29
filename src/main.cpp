// TronIdentityDisc — ESP-NOW link between an Identity Disc and its cloak.
//
// The Identity Disc and the cloak both build from this file; DEVICE_ROLE
// and COSTUME_ID (config.h, set per env in platformio.ini) are the only
// differences. COSTUME_ID pairs a disc with its cloak: packets from other
// costumes are dropped, so two costumes side by side stay independent.
//
// The disc owns the color. It has four buttons, one each for white, blue,
// red and green. Holding any button for LONG_HOLD_MS turns both boards' lights
// off; any press turns them back on in that button's color. The cloak has no
// buttons and shows whatever the disc tells it.
//
// Simultaneous change
// -------------------
// The two clocks are never synced. Instead the disc schedules every change
// APPLY_DELAY_MS in the future and tells the cloak how long is left:
//
//   disc:  press at T, applies at T + APPLY_DELAY_MS
//   SET_COLOR carries remainingUs = time left on the disc when it was sent,
//   and latencyUs = the disc's estimate of one-way air time.
//   cloak: applies at rxTime + remainingUs - latencyUs
//
// latencyUs comes from PING/PONG round trips, NTP style: the disc stamps a
// PING, the cloak echoes it with how long it held it, and the disc keeps
// half the smallest recent round trip. Only a short relative interval is
// carried across, so crystal drift (tens of ppm) is irrelevant.
//
// SET_COLOR is broadcast (no ACK), so it is sent SET_COLOR_REPEATS times
// inside the delay window; each copy carries its own remainingUs. The PING
// doubles as a heartbeat carrying the disc's target color, which catches the
// cloak up if every copy was lost or it rebooted.

#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <esp_timer.h>
#include <esp_log.h>
#include <FastLED.h>

#include "config.h"
#include "every_n_millis.h"

static const char* TAG = "disc";

// ---- Colors ----
// COLOR_OFF travels like any other color so "lights off" is scheduled and
// synced exactly the same way as a color change.
enum DiscColor : uint8_t { COLOR_WHITE, COLOR_BLUE, COLOR_RED, COLOR_GREEN, COLOR_OFF, COLOR_COUNT };
static const CRGB kColors[COLOR_COUNT] = { CRGB::White, CRGB::Blue, CRGB::Red, CRGB::Green, CRGB::Black };
static const char* kColorNames[COLOR_COUNT] = { "white", "blue", "red", "green", "off" };

// ---- Wire format ----
static const uint32_t MSG_MAGIC = 0x44495343;  // "DISC"
enum MsgType : uint8_t {
  MSG_PING      = 1,  // disc -> cloak, every HEARTBEAT_MS, carries target color
  MSG_PONG      = 2,  // cloak -> disc, echo of a PING
  MSG_SET_COLOR = 3,  // disc -> cloak, scheduled color change
};

struct __attribute__((packed)) DiscMsg {
  uint32_t magic;
  uint8_t  type;
  uint8_t  costume;      // sender's COSTUME_ID
  uint8_t  role;         // sender's DEVICE_ROLE
  uint8_t  color;
  uint16_t event;        // SET_COLOR: id shared by the repeats of one press
  uint32_t seq;
  int64_t  stampUs;      // PING: disc send time; PONG: that value echoed back
  int32_t  aUs;          // PONG: cloak hold time; SET_COLOR: remaining delay
  int32_t  latencyUs;    // SET_COLOR: disc's one-way latency estimate
};

struct RxPacket {
  uint8_t mac[6];
  int64_t rxUs;          // stamped in the receive callback, before queueing
  DiscMsg msg;
};

static const uint8_t kBroadcast[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

// esp_timer is 64-bit microseconds: no rollover to worry about.
static inline int64_t nowUs() { return esp_timer_get_time(); }

// ---- State ----
CRGB leds[NUM_LEDS];
static uint8_t  currentColor = COLOR_BLUE;
static uint32_t txSeq = 0;

// A scheduled color change, on either board.
static bool     pending = false;
static uint8_t  pendingColor = 0;
static int64_t  pendingAtUs = 0;
static uint16_t pendingEvent = 0;

static QueueHandle_t rxQueue;

// Peer link stats
static bool     peerSeen = false;
static uint8_t  peerMac[6];
static uint32_t lastPeerMs = 0;
static uint32_t lastPeerSeq = 0;
static uint32_t rxCount = 0;
static uint32_t rxLost = 0;
static uint32_t txFail = 0;

// ESP-NOW callbacks run in the WiFi task: stamp, copy and get out.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
static void onRecv(const esp_now_recv_info_t* info, const uint8_t* data, int len) {
  const uint8_t* mac = info->src_addr;
#else
static void onRecv(const uint8_t* mac, const uint8_t* data, int len) {
#endif
  int64_t rxUs = nowUs();
  if (len != sizeof(DiscMsg)) return;
  RxPacket p;
  p.rxUs = rxUs;
  memcpy(p.mac, mac, 6);
  memcpy(&p.msg, data, sizeof(DiscMsg));
  if (p.msg.magic != MSG_MAGIC) return;
  xQueueSend(rxQueue, &p, 0);
}

static void send(DiscMsg& m) {
  m.magic = MSG_MAGIC;
  m.costume = COSTUME_ID;
  m.role = DEVICE_ROLE;
  m.seq = ++txSeq;
  esp_err_t err = esp_now_send(kBroadcast, (const uint8_t*)&m, sizeof(m));
  if (err != ESP_OK) {
    txFail++;
    ESP_LOGE(TAG, "esp_now_send failed: %s", esp_err_to_name(err));
  }
}

static void showColor() {
  fill_solid(leds, NUM_LEDS, kColors[currentColor]);
  FastLED.show();
}

static void applyColor(uint8_t color, const char* why) {
  if (color == currentColor) return;
  currentColor = color;
  showColor();
#if SYNC_DEBUG_PIN >= 0
  digitalWrite(SYNC_DEBUG_PIN, !digitalRead(SYNC_DEBUG_PIN));  // scope this on both boards
#endif
  Serial.printf("Color -> %s (%s)\n", kColorNames[color], why);
}

static void schedule(uint8_t color, int64_t atUs, uint16_t event) {
  pending = true;
  pendingColor = color;
  pendingAtUs = atUs;
  pendingEvent = event;
}

static void runSchedule() {
  if (pending && nowUs() >= pendingAtUs) {
    pending = false;
    applyColor(pendingColor, DEVICE_ROLE == ROLE_DISC ? "button" : "disc button");
  }
}

static uint8_t targetColor() { return pending ? pendingColor : currentColor; }

#if DEVICE_ROLE == ROLE_DISC
// ---- Disc: latency estimate ----
// Half the minimum round trip over the last LATENCY_WINDOW pings. The minimum
// is the sample least inflated by retries and queueing.
static int32_t rttWindow[LATENCY_WINDOW];
static uint8_t rttCount = 0, rttNext = 0;
static int32_t latencyUs = LATENCY_DEFAULT_US;

static void addRtt(int32_t rtt) {
  rttWindow[rttNext] = rtt;
  rttNext = (rttNext + 1) % LATENCY_WINDOW;
  if (rttCount < LATENCY_WINDOW) rttCount++;
  int32_t best = rttWindow[0];
  for (uint8_t i = 1; i < rttCount; i++) best = min(best, rttWindow[i]);
  latencyUs = best / 2;
}

// ---- Disc: SET_COLOR repeats ----
static uint16_t eventId = 0;
static uint8_t  repeatsLeft = 0;
static int64_t  nextRepeatUs = 0;

static void sendSetColor() {
  DiscMsg m = {};
  m.type = MSG_SET_COLOR;
  m.color = pendingColor;
  m.event = pendingEvent;
  m.aUs = (int32_t)(pendingAtUs - nowUs());
  m.latencyUs = latencyUs;
  send(m);
}

static void runRepeats() {
  if (repeatsLeft == 0 || nowUs() < nextRepeatUs) return;
  if (!pending) { repeatsLeft = 0; return; }  // already applied: too late to help
  sendSetColor();
  repeatsLeft--;
  nextRepeatUs += SET_COLOR_REPEAT_MS * 1000LL;
}

static void requestColor(uint8_t color) {
  if (color == targetColor()) return;
  schedule(color, nowUs() + APPLY_DELAY_MS * 1000LL, ++eventId);
  sendSetColor();
  repeatsLeft = SET_COLOR_REPEATS - 1;
  nextRepeatUs = nowUs() + SET_COLOR_REPEAT_MS * 1000LL;
}

// ---- Disc: buttons ----
// Button i selects color i the moment it is pressed, so a tap feels instant.
// If the same press is then held for LONG_HOLD_MS, everything goes off. The
// color change on the way to "off" is harmless, and it means taps never wait
// to find out whether they will become holds.
static const uint8_t kButtonPins[BUTTON_COUNT] = BUTTON_PINS;

struct Button {
  bool     stable = HIGH;
  bool     lastRead = HIGH;
  uint32_t changedAt = 0;
  uint32_t pressedAt = 0;
  bool     holdFired = false;
};
static Button buttons[BUTTON_COUNT];

static void pollButtons() {
  uint32_t now = millis();
  for (uint8_t i = 0; i < BUTTON_COUNT; i++) {
    Button& b = buttons[i];
    bool r = digitalRead(kButtonPins[i]);
    if (r != b.lastRead) {
      b.lastRead = r;
      b.changedAt = now;
    }
    if (r != b.stable && now - b.changedAt >= DEBOUNCE_MS) {
      b.stable = r;
      if (b.stable == LOW) {
        b.pressedAt = now;
        b.holdFired = false;
        requestColor(i);
      }
    }
    if (b.stable == LOW && !b.holdFired && now - b.pressedAt >= LONG_HOLD_MS) {
      b.holdFired = true;
      Serial.println("Hold: lights off");
      requestColor(COLOR_OFF);
    }
  }
}
#endif

static void notePeer(const RxPacket& p) {
  const DiscMsg& m = p.msg;
  uint32_t now = millis();
  if (!peerSeen || memcmp(peerMac, p.mac, 6) != 0) {
    memcpy(peerMac, p.mac, 6);
    lastPeerSeq = m.seq - 1;  // don't count gaps from before we met
    Serial.printf("Peer %s found: %02X:%02X:%02X:%02X:%02X:%02X\n", PEER_NAME,
                  p.mac[0], p.mac[1], p.mac[2], p.mac[3], p.mac[4], p.mac[5]);
  } else if (now - lastPeerMs >= PEER_TIMEOUT_MS) {
    Serial.println("Peer back");
  }
  peerSeen = true;
  lastPeerMs = now;
  rxCount++;
  if (m.seq > lastPeerSeq + 1) rxLost += m.seq - lastPeerSeq - 1;
  if (m.seq < lastPeerSeq) Serial.println("Peer rebooted");  // seq restarted
  lastPeerSeq = m.seq;
}

static void handlePacket(const RxPacket& p) {
  const DiscMsg& m = p.msg;
  if (m.color >= COLOR_COUNT) return;
  if (m.costume != COSTUME_ID) return;  // another costume's pair: not ours
  if (m.role != PEER_ROLE) {
    static uint32_t tWarn = 0;
    if (everyMillis(tWarn, 5000)) {
      Serial.printf("Ignoring packet from role %u: both boards flashed as %s?\n",
                    m.role, DEVICE_NAME);
    }
    return;
  }
  notePeer(p);

#if DEVICE_ROLE == ROLE_CLOAK
  switch (m.type) {
    case MSG_PING: {
      DiscMsg r = {};
      r.type = MSG_PONG;
      r.color = currentColor;
      r.stampUs = m.stampUs;
      r.aUs = (int32_t)(nowUs() - p.rxUs);  // time spent here, removed from the RTT
      send(r);
      // Heartbeat catch-up: only when nothing is scheduled, so a ping sent
      // just before a press can't undo it.
      if (!pending && m.color != currentColor) applyColor(m.color, "disc sync");
      break;
    }
    case MSG_SET_COLOR:
      // Repeats of the same press are ignored; the first copy to arrive
      // has the least accumulated error.
      if (pending && m.event == pendingEvent) break;
      schedule(m.color, p.rxUs + m.aUs - m.latencyUs, m.event);
      break;
  }
#else
  if (m.type == MSG_PONG) {
    int64_t rtt = (p.rxUs - m.stampUs) - m.aUs;
    if (rtt > 0 && rtt < 100000) addRtt((int32_t)rtt);
  }
#endif
}

void setup() {
  Serial.begin(115200);
  delay(500);  // let USB CDC enumerate so the first lines aren't lost

#if DEVICE_ROLE == ROLE_DISC
  for (uint8_t i = 0; i < BUTTON_COUNT; i++) pinMode(kButtonPins[i], INPUT_PULLUP);
#endif
#if SYNC_DEBUG_PIN >= 0
  pinMode(SYNC_DEBUG_PIN, OUTPUT);
#endif

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, LED_MAX_MA);
  FastLED.setBrightness(LED_BRIGHTNESS);
  showColor();

  rxQueue = xQueueCreate(16, sizeof(RxPacket));

  // ESP-NOW needs the radio in STA mode but no AP connection.
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  esp_wifi_set_channel(ESPNOW_CHANNEL, WIFI_SECOND_CHAN_NONE);
  // Modem power save adds tens of ms of receive latency; keep the radio awake.
  esp_wifi_set_ps(WIFI_PS_NONE);

  if (esp_now_init() != ESP_OK) {
    ESP_LOGE(TAG, "esp_now_init failed");
    Serial.println("ESP-NOW init FAILED");
    return;
  }
  esp_now_register_recv_cb(onRecv);

  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, kBroadcast, 6);
  peer.channel = ESPNOW_CHANNEL;
  peer.encrypt = false;
  if (esp_now_add_peer(&peer) != ESP_OK) {
    ESP_LOGE(TAG, "esp_now_add_peer(broadcast) failed");
  }

  Serial.printf("\nTronIdentityDisc costume %d %s\nMy MAC: %s  channel %d\n",
                COSTUME_ID, DEVICE_NAME, WiFi.macAddress().c_str(), ESPNOW_CHANNEL);
  ESP_LOGI(TAG, "ready");
}

void loop() {
  RxPacket p;
  while (xQueueReceive(rxQueue, &p, 0) == pdTRUE) handlePacket(p);

  runSchedule();

#if DEVICE_ROLE == ROLE_DISC
  pollButtons();
  runRepeats();

  static uint32_t tPing = 0;
  if (everyMillis(tPing, HEARTBEAT_MS)) {
    DiscMsg m = {};
    m.type = MSG_PING;
    m.color = targetColor();
    m.stampUs = nowUs();
    send(m);
  }
#endif

  static uint32_t tLost = 0;
  if (everyMillis(tLost, 500) && peerSeen && millis() - lastPeerMs >= PEER_TIMEOUT_MS) {
    static uint32_t reportedAt = 0;
    if (reportedAt != lastPeerMs) {
      reportedAt = lastPeerMs;
      Serial.println("Peer LOST");
    }
  }

  static uint32_t tStats = 0;
  if (everyMillis(tStats, 5000)) {
    const char* link = !peerSeen ? "none" : (millis() - lastPeerMs < PEER_TIMEOUT_MS ? "up" : "LOST");
#if DEVICE_ROLE == ROLE_DISC
    Serial.printf("[stats] color=%s rx=%lu lost=%lu txFail=%lu peer=%s latency=%ldus\n",
                  kColorNames[currentColor], (unsigned long)rxCount, (unsigned long)rxLost,
                  (unsigned long)txFail, link, (long)latencyUs);
#else
    Serial.printf("[stats] color=%s rx=%lu lost=%lu txFail=%lu peer=%s\n",
                  kColorNames[currentColor], (unsigned long)rxCount, (unsigned long)rxLost,
                  (unsigned long)txFail, link);
#endif
  }
}
