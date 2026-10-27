# 01. Game flow: modes, start, race, finish

## FLOW-1. Modes [code]
Single-player: Arcade, Time Trial, Challenge, League, League Challenge, Academy, Eliminator, Zone, Endurance.
Two-player (split screen): Arcade, Time Trial, League, Eliminator, Endurance.
In two-player modes the first two ships are humans. Some rules apply only in single-player modes
(rubber band RACE-7, weapon filter WPN-4).

## FLOW-2. Event [code; Challenge and League — ✓]
Each race is described by an **event** (a record in `GAME.BNI`, FMT-8): type, track, number of laps, number of ships,
pilot arrangement, medal thresholds, allowed weapons. Event number by mode:

| mode | event number |
|---|---|
| Arcade | track code (0–47); the same events also hold the Time Trial thresholds in seconds |
| Time Trial, Zone | 48 (one shared) |
| Challenge | `120 + team·6 + challenge_number` (number 0–5) |
| League | from the league schedule (FMT-9) |
| League Challenge | `42 + league_number` — overlaps with the Arcade numbers for devilia, see OQ-15 |

## FLOW-3. Race parameters
Needed by the rules: track, speed class (1–4, SHIP-14), team and pilot of the player (and of the second player), number of ships (≤ 16),
number of laps, **whether weapon pads are enabled** [✓: disabled in the duel and in the lap-time challenge, enabled
in races, League, Elimination], **whether the pit lane is enabled** (PHY-24) [✓: enabled in Arcade, League and Time Trial, disabled in the Elimination
challenge and in Zone], start time T.

## FLOW-4. Race preparation (restart) [✓]
1. Ships are reset; each is assigned a pilot and team according to the event.
2. A ship's live parameters are copied from `SHIPS.INI` for its slot, then **upgrades** are applied (SHIP-5).
   The AI has upgrades too.
3. The start time T is determined and the generator is seeded (FLOW-5).
4. The race clock is zeroed.

## FLOW-5. Start time and generator seed [✓ T in the range 4.06…6.97 over 11 starts; seed — code]
- `T = 4.0 + U·3.0` s, where U is a random `[0, 1)` (GEN-4). In Time Trial and Zone `T = 4.0` exactly (without calling the generator).
- Then the generator is seeded with the value `floor(T·64)`.

## FLOW-6. Start sequence [code; GO and T — ✓]
t — time by the race clock, s.

| moment | what happens |
|---|---|
| 0 | board shows "HOLD"; in Time Trial an immediate jump to the row "t > T − 0.1" |
| t > 1.0 | commentator line |
| t > T − 0.1 | a human who is **already holding the throttle** **stalls** |
| immediately after | line, board "GO" |
| t ≥ T | **the race has started** (bursts — below) |
| T … T + 0.3 | **perfect start**: the first throttle press in this window gives a burst of 0.2 |
| t > T + 1.0 | stalled ships can accelerate again |

Bursts at the moment of the start:
- AI in Arcade [code; B = 0 — ✓ recording of 69 races; burst falling off by position — ✓ start recording]. Grid position s = 0…15
  (0 — the first row). If `16 − s ≥ 5` (positions 0…11): burst `0.01·(16 − s)` (from 0.16 to 0.05). For the last four positions
  (12…15) — by the pilot's skill level (AI-4): levels 2 and 3 — burst 0.2; level 1 — no burst, and the ship **stalls**
  (throttle is dropped from T + 0.5 to T + 1.0). The formula also has a pilot term B, but it is always 0.
- Human in Time Trial: burst 0.2.

Before the moment of the start the speed for the speedometer is not computed (it shows 0), although the ship sways slightly in place. [✓]

Intro before the start (Time Trial, Alca Vexus 2F, PAL) [✓ player observation, PAL]: after the "loading" screen the camera looks down from above at an
octagonal hatch in the track surface; the hatch leaves open, and the ship **rises from below on a lift**; the camera
moves behind the ship and sweeps around it sideways along the hull; then — the normal race camera with the countdown board. The cockpit canopy is
closed and does not move throughout.

**Board above the start straight** [✓ player observation, PAL]: there is no "3-2-1" countdown — the board shows in turn the screens "Hold ✕",
"Ready", "Go"; later in the race — "Final Lap 👌" and "Finish 👌" (with an "okay" picture). File check: each track has exactly five board states —
HOLD, READY, GO, FINAL, FINISH (separately for the forward and reverse layouts), no others; so the board shows everything
it has. The start without a countdown is "sudden" — this is by the game's design. How it works in other modes (a starting grid of 16 ships) — not examined.

## FLOW-7. Throttle before the start [code]
Throttle held before the start is a separate input state (SHIP-12). If it is held at the moment `T − 0.1`, the ship
stalls until `T + 1.0` (FLOW-6).

## FLOW-8. Race frame [✓ in order]
Every frame: input (humans and AI, AI-1) → 2 physics substeps (PHY-3) → rules (laps, positions, weapons, 04/06).

## FLOW-9. Pause [code]
Pause stops the race clock; lap times do not count the pause.

## FLOW-10. Autopilot [✓]
With the AUTOPILOT weapon and after the finish, the player's ship is controlled by the AI, gamepad input is ignored.

## FLOW-11. Finish [✓]
A ship finishes when it completes lap `number_of_laps + 1` (the lap counter exceeds the number of laps, RACE-3).

## FLOW-12. Finish table and current position [✓]
- At the moment of the finish the ship gets its **final place** (1, 2, …) in a separate finish table; from then on it is
  out of the race and drives on autopilot.
- The current position (RACE-5) continues to be recomputed after the finish too; only the finish table is used for results.
  [✓: the player finished 2nd, 4 s later the current position showed 3]
- **When the race is over for the humans** (all human ships have finished or dropped out), the remaining ships are given places
  **immediately, in a single frame**, in the order of current positions (RACE-5): the next free number goes to each ship still driving,
  if it is alive and **not destroyed by another's weapon** (SHIP-10); destroyed ones — including those still burning — and
  all others without a place get "dropped out". [✓ modified game, US (the order of places does not depend on frame rate): player 4th → 9 ships still driving got 5…13 in order of positions, in
  the same frame; a ship being destroyed — "dropped out"]
- A ship that drops out is marked "dropped out" in the finish table and gets no place.

## FLOW-13. Demo races [✓ 13 demos]
If the menu is left untouched for a long time, the game shows a demo: an ordinary Arcade race, but the "player's" ship is on autopilot
from the very beginning. The simulation in the demo stops after ~46 s, after which a presentation without movement continues.
