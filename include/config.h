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
  #define NUM_LEDS    30
#elif DEVICE_ROLE == ROLE_CLOAK
  #define DEVICE_NAME "Cloak"
  #define PEER_NAME   "Disc"
  #define NUM_LEDS    30
#else
  #error "DEVICE_ROLE must be ROLE_DISC or ROLE_CLOAK"
#endif

#define PEER_ROLE (DEVICE_ROLE == ROLE_DISC ? ROLE_CLOAK : ROLE_DISC)

// ---- LEDs ----
#define LED_PIN        10      // through 330 ohm, see docs/esp32c3-18650-led-power.md
#define LED_MAX_MA     800     // FastLED power cap for the 18650 + MT3608 budget
#define LED_BRIGHTNESS 128

// ---- Buttons (disc only; the cloak has none) ----
// One button per color, each wired from the GPIO to GND (internal pull-ups).
// Order matches the colors: white, blue, red, green. All four are on GPIO0-4
// on purpose: only GPIO0-5 can wake the C3 from deep sleep, so any color
// button can become the wake button later. Avoid GPIO2/8/9 (strapping) and
// GPIO10 (LED data).
#define BUTTON_PINS    { 0, 1, 3, 4 }
#define BUTTON_COUNT   4
#define DEBOUNCE_MS    30
#define LONG_HOLD_MS   3000    // hold any button this long: all lights off

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
// -1 = off. GPIO 5 is free on the disc and the cloak.
#define SYNC_DEBUG_PIN     -1
