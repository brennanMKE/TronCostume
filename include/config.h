#pragma once

// ---- Costume and role ----
// Set per build env in platformio.ini; the defaults here are for IDEs and
// bare builds.
//
// COSTUME_ID pairs a disc with its cloak. Every packet carries it and a board
// drops packets from any other costume, so two costumes in the same room
// never control each other.
#ifndef COSTUME_ID
#define COSTUME_ID 1
#endif

#if COSTUME_ID < 1 || COSTUME_ID > 255
  #error "COSTUME_ID must be 1-255"
#endif

// DEVICE_ROLE says which half of the costume this board is. Anything that
// has to differ between the Identity Disc and the cloak goes in the block
// below.
#define ROLE_DISC  0
#define ROLE_CLOAK 1

#ifndef DEVICE_ROLE
#define DEVICE_ROLE ROLE_DISC
#endif

#if DEVICE_ROLE == ROLE_DISC
  #define DEVICE_NAME "Disc"
  #define PEER_NAME   "Cloak"
  // One strip chain: the inner C first, then the outer ring (docs/disc-build.md;
  // 60 LEDs/m counts, change for the strip you buy).
  #ifdef BENCH_RING_LEDS
    // Bench strip (env disc-1-bench): every LED is outer ring, so the ring
    // effects can be tried on a short test strip.
    #define MAIN_LEDS 0
    #define RING_LEDS BENCH_RING_LEDS
  #else
    #define MAIN_LEDS 33      // inner C: always on, solid color
    #define RING_LEDS 41      // outer ring: on/off and effects
  #endif
#elif DEVICE_ROLE == ROLE_CLOAK
  #define DEVICE_NAME "Cloak"
  #define PEER_NAME   "Disc"
  #define MAIN_LEDS   30
  #define RING_LEDS   0
#else
  #error "DEVICE_ROLE must be ROLE_DISC or ROLE_CLOAK"
#endif

#define PEER_ROLE (DEVICE_ROLE == ROLE_DISC ? ROLE_CLOAK : ROLE_DISC)
#define NUM_LEDS  (MAIN_LEDS + RING_LEDS)

// ---- LEDs ----
#define LED_PIN        4       // through 330 ohm; beside 3V3/5V/GND on the C3 Super Mini
#define LED_MAX_MA     800     // FastLED power cap for the 18650 + MT3608 budget
#define LED_BRIGHTNESS 128
#define LED_GAMMA      2.6f    // screen hex -> LED; tuned on the ButtonsAndColors breadboard
#define FRAME_MS       20      // disc redraw rate for the outer ring effects (50 fps)

// Outer ring effects (disc)
#define RING_IGNITE_MS      400   // sweep around when the ring comes on
#define RING_MOTION_MS      1000  // motion effect: one turn of the bright head
#define RING_MOTION_FLOOR   50    // motion effect: base level behind the tail (0-255)

// ---- Buttons ----
// Wired from the GPIO to GND (internal pull-ups). Only GPIO 0-5 can wake the
// C3 from deep sleep, so each board's wake button is on GPIO 5.
//
// Disc: four buttons lined up on one side of the C3 Super Mini, in order
// black, white, green, blue. GPIO 8 (onboard LED, strapping) and 9 (BOOT,
// strapping) are skipped. Black is the outer ring button and the wake button.
// Gestures are in docs/controls.md.
//
// Cloak: one button, wake only (planned, docs/deep-sleep.md). It never
// lights the cloak by itself: it wakes the cloak, which then waits dark for
// the disc to say what to show. Holding it asks the disc to turn the costume
// off, so the pair stays in sync.
#define WAKE_PIN       5
#if DEVICE_ROLE == ROLE_DISC
  #define BUTTON_PINS  { 5, 6, 10, 7 }   // black, white, blue, green (board order: black 5, white 6, green 7, blue 10)
  #define BUTTON_COUNT 4
#else
  #define BUTTON_PINS  { 5 }
  #define BUTTON_COUNT 1
#endif
#define DEBOUNCE_MS    30
#define TAP_GAP_MS     350     // a further tap must start within this of the last release
#define SHORT_HOLD_MS  1000    // color button held: send the color to both costumes
#define LONG_HOLD_MS   3000    // black button held: this costume off

// Disc: off (black hold) puts the disc into deep sleep; black wakes it.
// Set to 0 to stay awake and dark instead, e.g. while debugging over USB,
// which disappears while the board sleeps.
#define DEEP_SLEEP        1
#define RELEASE_SETTLE_MS 200   // every button up this long before sleeping

// Disc saves its color to flash (NVS) once it has held this long, so a burst
// of taps is one write. Power-on and wake restore it.
#define COLOR_SAVE_MS  2000

// ---- Waking up and linking (planned, docs/deep-sleep.md) ----
// The disc lights in its saved color at once. The cloak stays dark until the
// disc tells it what to show.
#define CLOAK_HELLO_MS      200      // awake, unlinked cloak announces itself this often
#define CLOAK_LINK_WAIT_MS  300000   // dark cloak gives up waiting and sleeps after 5 min

// Strip power switch (planned P-channel MOSFET, docs/deep-sleep.md). HIGH =
// strip powered. Harmless before the MOSFET is fitted.
#define LED_POWER_PIN  20

// ---- ESP-NOW ----
// Both boards must be on the same channel. With no WiFi connection the
// channel is whatever we set here.
#define ESPNOW_CHANNEL     1
#define HEARTBEAT_MS       1000   // disc PING period; also the latency sample rate
#define PEER_TIMEOUT_MS    3500   // peer considered lost after ~3 missed heartbeats

// ---- Simultaneous color change ----
// A press changes both boards APPLY_DELAY_MS later. It has to cover one-way
// latency (a few ms) plus every SET_COLOR repeat; under ~80 ms reads as
// instant to a person.
#define APPLY_DELAY_MS       50
#define SET_COLOR_REPEATS    3      // broadcasts have no ACK, so send a few
#define SET_COLOR_REPEAT_MS  12     // spacing; REPEATS * this must be < APPLY_DELAY_MS
#define LATENCY_WINDOW       8      // pings kept for the min-RTT estimate
#define LATENCY_DEFAULT_US   1500   // used until the first PONG comes back

#if SET_COLOR_REPEATS * SET_COLOR_REPEAT_MS >= APPLY_DELAY_MS
  #error "SET_COLOR repeats must all go out before the change is applied"
#endif

// Toggled on every scheduled apply. Put a scope or logic analyzer on this
// pin on both boards to measure how far apart the changes really are.
// -1 = off. GPIO 0 is free on the disc and the cloak (bench use only).
// GPIO 3 is reserved for the disc's dock sensor.
#define SYNC_DEBUG_PIN     -1
