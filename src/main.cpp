// TronIdentityDisc — ESP-NOW link between an Identity Disc and its cloak.
//
// The Identity Disc and the cloak both build from this file; DEVICE_ROLE
// and COSTUME_ID (config.h, set per env in platformio.ini) are the only
// differences. COSTUME_ID pairs a disc with its cloak: packets from other
// costumes are dropped, so two costumes side by side stay independent.
//
// The disc owns the color. It has four buttons (docs/controls.md):
//
//   white, blue, green   tap: that color; double tap: its pair (yellow, red,
//                        orange); hold 1 s / tap then hold 1 s: the same for
//                        both costumes
//   black                double tap: flicker; triple tap: motion; tap: back
//                        to steady (never turns anything off); hold 3 s:
//                        this costume off, then the disc
//                        deep sleeps until black is pressed again
//
// The disc and its cloak always show the same color. The cloak has no color
// buttons and shows whatever the disc tells it. The disc's strip is two
// parts: the inner C (solid) and the outer ring (on/off and effects, disc
// only).
//
// The disc keeps its last lit color in flash (NVS). At power-on or wake it
// sends that color as a scheduled change as soon as ESP-NOW is up, so the
// disc and cloak light together. A button already held at boot (the black
// button waking the disc) is ignored until released. The cloak stores nothing: it starts
// dark and lights from the disc's first heartbeat.
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
#include <Preferences.h>
#include <esp_sleep.h>
#include <driver/gpio.h>

#include "config.h"
#include "every_n_millis.h"

static const char* TAG = "disc";

// ---- Colors ----
// COLOR_OFF travels like any other color so "lights off" is scheduled and
// synced exactly the same way as a color change.
enum DiscColor : uint8_t {
  COLOR_WHITE, COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_YELLOW, COLOR_ORANGE,
  COLOR_OFF, COLOR_COUNT
};
static const CRGB kColors[COLOR_COUNT] = {
  CRGB(0xE6FFFF),  // white
  CRGB(0x39FF14),  // green
  CRGB(0x6FC3DF),  // blue
  CRGB(0xFF2A2A),  // red
  CRGB(0xFFE64D),  // yellow
  CRGB(0xDF740C),  // orange
  CRGB::Black,
};
static const char* kColorNames[COLOR_COUNT] = { "white", "green", "blue", "red", "yellow", "orange", "off" };

// The hex values above are screen colors. A screen dims low channel values
// (gamma), but an LED shows them close to face value, so red's 0x2A of green
// and blue turns it pink. Applying the same curve here makes the strip match
// the screen: small values drop to almost nothing, full ones stay full.
// Tuned on the ButtonsAndColors breadboard.
static CRGB ledColors[COLOR_COUNT];

static uint8_t gammaByte(uint8_t v) {
  return (uint8_t)(powf(v / 255.0f, LED_GAMMA) * 255.0f + 0.5f);
}

static void buildLedColors() {
  for (uint8_t i = 0; i < COLOR_COUNT; i++) {
    const CRGB& c = kColors[i];
    ledColors[i] = CRGB(gammaByte(c.r), gammaByte(c.g), gammaByte(c.b));
  }
}

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
static uint8_t  currentColor = COLOR_OFF;  // dark until the disc restores or the cloak hears a color
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

// ---- Drawing ----
// The first MAIN_LEDS are the solid part: the disc's inner C, or the cloak's
// strip. On the disc the next RING_LEDS are the outer ring, which can be off
// and has effects.
enum RingMode : uint8_t { RING_SOLID, RING_FLICKER, RING_MOTION };
static const char* kRingNames[] = { "solid", "flicker", "motion" };
static bool     ringOn = true;
static uint8_t  ringMode = RING_SOLID;
static uint32_t ringLitMs = 0;   // start of the ignition sweep

#if RING_LEDS > 0
// Erratic flicker: the whole ring holds a level for a random time, mostly
// full, sometimes dipping, with the odd LED dropping out.
static uint8_t ringFlickerLevel(uint32_t now) {
  static uint8_t  level = 255;
  static uint32_t at = 0, holdMs = 0;
  if (now - at >= holdMs) {
    at = now;
    if (random8() < 80) { level = random8(20, 170); holdMs = random8(20, 90); }
    else                { level = 255;              holdMs = random16(60, 450); }
  }
  return level;
}

static void drawRing(uint32_t now) {
  CRGB* ring = leds + MAIN_LEDS;
  if (!ringOn || currentColor == COLOR_OFF) {
    fill_solid(ring, RING_LEDS, CRGB::Black);
    return;
  }
  // Ignition: the ring lights around from its first LED.
  uint32_t since = now - ringLitMs;
  uint16_t lit = since >= RING_IGNITE_MS ? RING_LEDS : (uint32_t)RING_LEDS * since / RING_IGNITE_MS;
  uint8_t flicker = ringMode == RING_FLICKER ? ringFlickerLevel(now) : 255;
  // Motion: a bright head travels round once per RING_MOTION_MS with a
  // fading tail, over a dim base.
  uint16_t head = (uint32_t)(now % RING_MOTION_MS) * RING_LEDS / RING_MOTION_MS;
  const uint16_t tail = RING_LEDS / 3;
  for (uint16_t i = 0; i < RING_LEDS; i++) {
    uint8_t level = 255;
    if (ringMode == RING_MOTION) {
      uint16_t behind = (head + RING_LEDS - i) % RING_LEDS;
      level = behind < tail ? 255 - (uint32_t)behind * (255 - RING_MOTION_FLOOR) / tail : RING_MOTION_FLOOR;
    } else if (ringMode == RING_FLICKER) {
      level = random8() < 6 ? flicker / 4 : flicker;
    }
    CRGB c = i < lit ? ledColors[currentColor] : CRGB::Black;
    c.nscale8_video(level);
    ring[i] = c;
  }
}
#endif

static void render() {
  fill_solid(leds, MAIN_LEDS, ledColors[currentColor]);
#if RING_LEDS > 0
  drawRing(millis());
#endif
  FastLED.show();
}

#if DEVICE_ROLE == ROLE_DISC
// ---- Disc: saved color ----
// Off is never saved, so power-on and wake always come back lit in the last
// color. A write waits until the color has held for COLOR_SAVE_MS, so a run
// of taps costs one flash write.
static Preferences prefs;
static uint8_t  savedColor = COLOR_OFF;
static uint32_t colorChangedMs = 0;

static uint8_t loadColor() {
  prefs.begin("disc", false);
  uint8_t c = prefs.getUChar("color", COLOR_BLUE);
  if (c >= COLOR_OFF) c = COLOR_BLUE;
  savedColor = c;
  return c;
}

static void saveColor(uint8_t color) {
  if (color == COLOR_OFF || color == savedColor) return;
  prefs.putUChar("color", color);
  savedColor = color;
  Serial.printf("Saved %s\n", kColorNames[color]);
}

static void runSave() {
  if (millis() - colorChangedMs < COLOR_SAVE_MS) return;
  saveColor(currentColor);
}
#endif

static void applyColor(uint8_t color, const char* why) {
  if (color == currentColor) return;
  if (currentColor == COLOR_OFF) ringLitMs = millis();  // coming on: ignite the ring
  currentColor = color;
#if DEVICE_ROLE == ROLE_DISC
  colorChangedMs = millis();
#endif
  render();
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

// ---- Disc: both costumes ----
// Needs SET_COLOR_GROUP (docs/controls.md), which isn't built yet. Until then
// it changes this costume only.
static void requestBoth(uint8_t color) {
  Serial.printf("Both costumes -> %s (group message not built yet: this costume only)\n",
                kColorNames[color]);
  requestColor(color);
}

// ---- Disc: buttons ----
// Two layers: debounce each button into press/release events, then a small
// state machine turns those into gestures: 1-3 taps, or a hold after 1-2
// taps. Taps wait TAP_GAP_MS after release in case another is coming, except
// the last tap a button understands, which fires on release.
//
//   IDLE --press--> DOWN --release--> GAP --TAP_GAP_MS--> taps(n)
//                    |  ^               |
//                 held  +--press same---+   (n + 1)
//                    v
//                  HELD --> hold(n)
static const uint8_t kButtonPins[BUTTON_COUNT] = BUTTON_PINS;

// Button order matches BUTTON_PINS: black, white, blue, green.
static const uint8_t BTN_BLACK = 0;
static const uint8_t kPrimary[BUTTON_COUNT]   = { COLOR_OFF, COLOR_WHITE,  COLOR_BLUE, COLOR_GREEN };
static const uint8_t kSecondary[BUTTON_COUNT] = { COLOR_OFF, COLOR_YELLOW, COLOR_RED,  COLOR_ORANGE };

static uint8_t maxTaps(uint8_t b) { return b == BTN_BLACK ? 3 : 2; }

// 0 = no hold gesture for this button and tap count.
static uint32_t holdMs(uint8_t b, uint8_t taps) {
  if (b == BTN_BLACK) return taps == 1 ? LONG_HOLD_MS : 0;
  return SHORT_HOLD_MS;
}

static void ringSet(bool on, uint8_t mode) {
  if (on && !ringOn) ringLitMs = millis();
  ringOn = on;
  ringMode = mode;
  Serial.printf("Outer ring %s (%s)\n", on ? "on" : "off", kRingNames[mode]);
}

static void onTaps(uint8_t b, uint8_t taps) {
  if (b != BTN_BLACK) {
    requestColor(taps == 1 ? kPrimary[b] : kSecondary[b]);
    return;
  }
  if (targetColor() == COLOR_OFF) {   // black brings a dark costume back on
    requestColor(savedColor);
    return;
  }
  // Double and triple tap pick an effect. A single tap is the way back to
  // steady: the ring on and solid. It never turns anything off.
  switch (taps) {
    case 1: ringSet(true, RING_SOLID); break;
    case 2: ringSet(true, RING_FLICKER); break;
    case 3: ringSet(true, RING_MOTION); break;
  }
}

static bool sleepRequested = false;   // off: deep sleep once every button is up

static void onHold(uint8_t b, uint8_t taps) {
  if (b == BTN_BLACK) {
    Serial.println("Hold: lights off");
    saveColor(targetColor());   // don't lose a color picked under COLOR_SAVE_MS ago
    requestColor(COLOR_OFF);
#if DEEP_SLEEP
    sleepRequested = true;
#endif
    return;
  }
  requestBoth(taps == 1 ? kPrimary[b] : kSecondary[b]);
}

enum SeqState : uint8_t { SEQ_IDLE, SEQ_DOWN, SEQ_GAP, SEQ_HELD };
static SeqState seqState = SEQ_IDLE;
static uint8_t  seqButton = 0;
static uint8_t  seqTaps = 0;
static uint32_t seqAt = 0;   // press time in DOWN, release time in GAP

static void onPress(uint8_t b, uint32_t now) {
  if (sleepRequested) return;  // going to sleep: nothing turns it back on now
  if (seqState == SEQ_GAP && b == seqButton) {
    seqTaps++;
  } else if (seqState == SEQ_IDLE || seqState == SEQ_GAP) {
    if (seqState == SEQ_GAP) onTaps(seqButton, seqTaps);  // another button ends the last sequence
    seqButton = b;
    seqTaps = 1;
  } else {
    return;  // a second button pressed mid-press: ignored
  }
  seqState = SEQ_DOWN;
  seqAt = now;
}

static void onRelease(uint8_t b, uint32_t now) {
  if (b != seqButton) return;
  if (seqState == SEQ_HELD) {
    seqState = SEQ_IDLE;
  } else if (seqState == SEQ_DOWN) {
    if (seqTaps >= maxTaps(b)) {
      seqState = SEQ_IDLE;
      onTaps(b, seqTaps);
    } else {
      seqState = SEQ_GAP;
      seqAt = now;
    }
  }
}

static void runSequence(uint32_t now) {
  if (seqState == SEQ_DOWN) {
    uint32_t h = holdMs(seqButton, seqTaps);
    if (h && now - seqAt >= h) {
      seqState = SEQ_HELD;
      onHold(seqButton, seqTaps);
    }
  } else if (seqState == SEQ_GAP && now - seqAt >= TAP_GAP_MS) {
    seqState = SEQ_IDLE;
    onTaps(seqButton, seqTaps);
  }
}

struct Button {
  bool     stable = HIGH;
  bool     lastRead = HIGH;
  uint32_t changedAt = 0;
  bool     ignore = false;   // held since boot: no events until released
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
      if (b.ignore) {
        if (b.stable == HIGH) b.ignore = false;
      } else if (b.stable == LOW) {
        onPress(i, now);
      } else {
        onRelease(i, now);
      }
    }
  }
  runSequence(now);
}

// ---- Disc: deep sleep (docs/deep-sleep.md) ----
// Off is a hold on black. The LEDs go dark straight away (that's the
// feedback), then the disc sleeps once the cloak has been told and every
// button has been up for RELEASE_SETTLE_MS. Wake is level-triggered, so
// sleeping with black still held would wake it again at once.
//
// Asleep, only black (WAKE_PIN, GPIO 5) can wake it: only GPIO 0-5 can, and
// white, green and blue are on 6, 7 and 10. Waking restarts the board, which
// lights in the saved color and ignores the waking press until it's released.
static void goToSleep() {
  Serial.println("Deep sleep: press black to wake");
  Serial.flush();

  // Strip already dark. Hold its data line low so noise on a floating pin
  // can't light LEDs while the strip still has power (no MOSFET yet).
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  gpio_hold_en((gpio_num_t)LED_PIN);
  gpio_deep_sleep_hold_en();

  esp_now_deinit();
  WiFi.mode(WIFI_OFF);

  // Keep black's pull-up on through sleep. If the disc wakes by itself or
  // won't wake, fit a 100k from GPIO 5 to 3.3V (docs/deep-sleep.md).
  gpio_pullup_en((gpio_num_t)WAKE_PIN);
  gpio_pulldown_dis((gpio_num_t)WAKE_PIN);
  esp_deep_sleep_enable_gpio_wakeup(1ULL << WAKE_PIN, ESP_GPIO_WAKEUP_GPIO_LOW);
  esp_deep_sleep_start();
}

static void runSleep() {
  static uint32_t allUpSince = 0;
  if (!sleepRequested) return;
  if (pending || repeatsLeft > 0) return;   // the cloak hasn't been told yet
  uint32_t now = millis();
  for (uint8_t i = 0; i < BUTTON_COUNT; i++) {
    if (digitalRead(kButtonPins[i]) == LOW) { allUpSince = 0; return; }
  }
  if (allUpSince == 0) allUpSince = now ? now : 1;
  if (now - allUpSince >= RELEASE_SETTLE_MS) goToSleep();
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
  // Serial logs don't survive deep sleep, so say why we're starting.
  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_GPIO) Serial.println("Woke: black button");
  // Release the LED data line held low through sleep (goToSleep).
  gpio_hold_dis((gpio_num_t)LED_PIN);
  gpio_deep_sleep_hold_dis();

  for (uint8_t i = 0; i < BUTTON_COUNT; i++) {
    pinMode(kButtonPins[i], INPUT_PULLUP);
    // Still held from the press that powered on or woke the disc: ignore
    // it until released, so it is neither a tap nor a hold.
    if (digitalRead(kButtonPins[i]) == LOW) {
      buttons[i].stable = buttons[i].lastRead = LOW;
      buttons[i].ignore = true;
    }
  }
  // Start dark: the saved color goes out as a scheduled change once ESP-NOW
  // is up (end of setup), so the disc and cloak light together.
  uint8_t bootColor = loadColor();
  Serial.printf("Restored %s\n", kColorNames[bootColor]);
#endif
#if SYNC_DEBUG_PIN >= 0
  pinMode(SYNC_DEBUG_PIN, OUTPUT);
#endif

  buildLedColors();
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, LED_MAX_MA);
  FastLED.setBrightness(LED_BRIGHTNESS);
  ringLitMs = millis();
  render();

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
#if DEVICE_ROLE == ROLE_DISC
    applyColor(bootColor, "power on, no radio");
#endif
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

#if DEVICE_ROLE == ROLE_DISC
  // Light like a button press: scheduled APPLY_DELAY_MS ahead and sent to
  // the cloak, so both strips come on at the same moment.
  requestColor(bootColor);
#endif
}

void loop() {
  RxPacket p;
  while (xQueueReceive(rxQueue, &p, 0) == pdTRUE) handlePacket(p);

  runSchedule();

#if DEVICE_ROLE == ROLE_DISC
  pollButtons();
  runRepeats();
  runSave();
  runSleep();

  static uint32_t tFrame = 0;
  if (everyMillis(tFrame, FRAME_MS)) render();  // outer ring animation

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
