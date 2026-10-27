# Behaviour specification of Wipeout Fusion (PAL)

Русская версия: [docs/ru/spec/README.md](../ru/spec/README.md)

This is the **clean part** of the ReFusion project: a description of *what* the game does — rules, formulas, constants,
file formats. Your own implementation is written from these documents. The order of work, roles and what the clean team may and may not do
are in [`../process/README.md`](../process/README.md). Read it before starting work.

## Rules for this folder
- There are **no** addresses, disassembly, decompiled code, or internal names of the original's functions, variables and fields here.
- Names are taken from the **game data** (keys of `SHIPS.INI`, `WEAPONSTATS.INI`, track material names), from **on-screen text**
  or introduced descriptively (`shield`, `lap progress`). All terms are in the [glossary](00_glossary.md).
- Numbers are **observable behaviour and parameters**: constants, thresholds, durations, formulas.
- The evidence (how a rule was established) is kept by the dirty team separately and is **not available** to the clean team.
  If a rule is missing or unclear — ask in [QUESTIONS.md](QUESTIONS.md).
- Any change to this folder passes the [checklist](../process/review_checklist.md) and `python docs/process/check_spec.py`.

## What the specification covers
**Included:** game logic — race flow, ship physics, rules and scoring, AI, weapons, player progress,
data file and save formats.
**Not included:** rendering, sound, video, the look of menus and HUD. For these only file formats (07) are given — the implementation
does them its own way. If any of this affects logic (for example, a transition between screens), it is described explicitly.

The implementation does not contain **game data**: it reads files from the user's copy of the game. Numbers from data files
are given here only as examples and reference values.

## Rule IDs and evidence level
Every rule has an **ID** (`PHY-6`, `WPN-12` …) — questions, tests and the change log refer to it.
IDs are not reused: a deleted rule is marked "withdrawn" and does not disappear silently.

The specification describes the **PAL version** (SCES-50005). Observations on the American version (NTSC-U) are accepted as [✓]
only for facts that do not depend on frame rate or clock progress: order of places, conditions, percentages, levels,
captions. Durations and moments in time are taken only from PAL (20 ms frame, GEN-1). Differences between versions — OQ-46.

| label | meaning | how to treat it in the implementation |
|---|---|---|
| **[✓]** | confirmed by game **behaviour** (frame-by-frame observations), numbers matched | implement as is |
| **[✓ player observation, PAL]** | confirmed by what the player saw and measured while playing | implement as is |
| **[✓ modified game, PAL]** | formula verified on a modified copy of the game: confirms the formula, but not necessarily the behaviour of the original mode as a whole | implement as is; if it diverges from the game — ask a question |
| **[code]** | established, but not yet verified by behaviour | implement as is; if it diverges from the game — ask a question |
| **[?]** | hypothesis | implement as a temporary solution, isolated so that it is easy to replace |

## General conventions

### GEN-1. Time [✓]
The game lives in its own clock: frame = **20 ms** (PAL, 50 Hz); real time is not measured. If a frame is not ready in time,
the game slows down rather than skipping steps. Physics is **2 substeps of 0.01 s** per frame (100 Hz), see PHY-1.
Time is stored both as integer milliseconds and as floating-point seconds; start thresholds and lap timers
are compared with these values.

### GEN-2. Length units [✓]
Track world units. The **Y axis points up**.

### GEN-3. Speed [✓]
The velocity vector is in units/s. On the speedometer `|v| × 3.6` ("km/h"). Speed parameters in `SHIPS.INI`
(`maxspeed` and others) are given in the same "km/h"; in the thrust formulas they are converted back by dividing by 3.6.

### GEN-4. Randomness [code]
One shared generator — a linear congruential one, the same as in the example from the C language standard:
`seed = (seed · 1103515245 + 12345) mod 2^32`, the result is `seed mod 2^31` (range `[0, 2^31)`).
A random number `[0, 1)` = `result / 2^31`. Seeding before a race — FLOW-5.
Determinism is mandatory: with identical input a race is reproduced; the order of generator calls matters.
Reference values — TC-1.

### GEN-5. Track indices [✓]
Environment `env` 0–7: florion_height, mandrashee, cubiss_float, alca_vexus, vohl_square, temtesh_bay, katmoda_12,
devilia. Layout `circuit` 0–5: 1F, 1R, 2F, 2R, 3F, 3R. **Track code** = `env·6 + circuit` (0–47).
devilia has only F layouts (codes 42, 44, 46); 45 tracks in total.

### GEN-6. Teams and slots [✓]
Team numbers 0–7 and the ship slot `team·2 + pilot` — see SHIP-1, SHIP-2. These numbers are used in the data
files and the save, so they are fixed.

### GEN-7. American version (NTSC-U) [code; clock and distance — ✓]
The specification describes PAL. The American version is a **different build**, not the same game with a different display frequency.
An implementation that wants to behave like PAL does **not reproduce** these differences; they are needed to read
observations made on the US version correctly.
- **Frame** — 1/60 s. The game clock adds 16, 16, 18 ms in rotation (16.67 ms on average), so clock seconds are
  real seconds. [✓ recording: steps of 16 and 18 ms in the ratio 2:1]
- **Physics** — still 2 substeps per frame, that is 120 substeps per second; the substep step is 0.0083 s (not 1/120).
  The distance per second at the same speed is 0.996 of PAL (120 · 0.0083). [✓ recording: distance / (speed · time) in both
  versions matched to within 0.1 %]
- **Impulses per substep were not recalculated** (thrust, suspension, sliding off slopes — the same formulas and the same ship
  parameters, PHY-10): therefore acceleration, stiffness and suspension damping per second in the US version are **about 1.2 times
  larger**. Maximum speed is the same. [✓ measurement: the same ship without upgrades, Time Trial, throttle from
  standstill, both versions — acceleration 300→800 km/h in US is faster by 1.15–1.3 times (1.2 on average); the start burst gives the same
  speed per frame, that is in US it is shorter in time]
- Physics, AI and pilot mood timers were recalculated for 60 Hz (some exactly ×5/6, some ×0.83). The **movement
  speed** of some weapon effects per frame was reduced ×0.8 (for Flamer, Grenades, Plasma Bolt — ×5/6), so
  some of them move 4 % slower per second in the US version. One component of ship physics was changed
  much more (the coefficient is 6 times smaller); what it means — OQ-46.
- **Not everything was recalculated.** The "wrong way" timer (RACE-6) stayed in frames — in US it is 2.33 / 0.33 s instead of 2.8 / 0.4 s;
  the lava counter (PHY-21) stayed in substeps — its thresholds come 1.2 times earlier. The profile statistic "time in
  races" and one of the HUD timers count 16 ms per frame — they lag behind real time by 4 %.
- **Weapon timers** (lifetime of rockets and mines, effect durations, reload) were recalculated ×1.2 — per second
  they are the same as in PAL. (Not to be confused with the movement speed of effects above.)
- The **AI** thinks for each ship **every other frame** (30 times per second, even and odd ships in turn), in PAL —
  every frame (50 times per second). The "shoot or not" decision of bots is slightly changed, and after any bot uses Quake
  the others do not use it for **15 s** (in PAL — 5 s, AI-2).
- A **weapon pad** after a pickup does not grant a weapon for **1 s** (in PAL — 0.5 s, WPN-3).
- **Wall collisions** were rewritten: they are checked for each ship on every substep (in PAL — only in the first,
  PHY-13), the bounce force per touch is half as large. Exact behaviour in US — not studied.
- **Races on both versions** (one league of 5 races, the same ship with the same upgrades, one player)
  [✓ player observation, PAL and US]:
  - **Sliding.** In US the ship slides sideways less: the angle between the nose and the direction of movement at speed is
    on average ~20 % smaller on all five tracks (median 4.2–6.2° versus 5.2–7.4°); turn rate with the same
    steering command is almost the same.
  - **Weapons on pads.** All ships pick them up ~20 % less often (2.4–4.6 versus 3.2–6.0 pickups per ship per
    minute) — consistent with a pad that is "silent" for longer.
  - **US version bug.** On Alca Vexus 2R in US the player's ship on a climb was accelerated within half a second to ~11 000 km/h and
    thrown off the track (one case). In PAL at the same place over three laps this did not happen; another 5 repeats of the same
    race moment in PAL — autopilot, straight throttle, steering left and right, coasting — also did not produce it
    [✓ repeated runs of the same race moment]. This is a US version bug (project decision): not
    reproduced in the port and not investigated; the reference is PAL.
  - **Walls and brakes.** A bounce off a wall in US costs less speed (on 4 of 4 tracks where bounces occurred in both
    versions, by ~25 % on average); the player held airbrakes for 15–26 % of race time in PAL, 11–19 % in US (on two
    tracks the same).
  - **Player impression.** PAL — "sliding" handling, the feel of a heavy ship; you have to enter a corner
    early, difficult combinations (for example on Mandrashee) require technique and almost constant airbrakes; in
    tight places the ship can "bounce" between walls, walls throw it back harder and take more speed. US — the nose
    obeys better, corner entry is more predictable, brakes are needed mainly to throw the ship into a corner more sharply;
    walls are softer; races are calmer (less weapons, opponents less pushy). For an implementation that
    reproduces PAL, this is the "feel" reference.
- The speed cheat code multiplies the player ship's speed by 2 (in PAL — by 10).
- The Time Trial "ghost" stores 1080 records — the same 3 minutes at 60 Hz (RACE-15).
- The picture is 448 lines instead of 512; all on-screen coordinates were recalculated. New particle effects for weapons and tracks.
- **Data:** ship parameters are the same. The Flamer in the US version deals more damage (damage settings
  0.4 / 0.1 → 0.8 / 0.5, WPN). In one lap-time challenge (league 3, race 3, Cubiss Float 2F) the medal thresholds are
  looser by 2 s (85 / 80 / 75 instead of 83 / 78 / 73). The **track geometry** of Alca Vexus, Katmoda 12 and Temtesh Bay is changed
  (all 6 layouts of each), for Vohl Square only the visibility data; Florion Height, Mandrashee, Cubiss Float and
  Devilia — the same files. The file composition is almost the same (PAL 3280, US 3293) [✓ files]: only in PAL — the language selection clip
  and the animation of flying machines over Katmoda 12 (3 models and a texture: not in US); only in US — leftover copies of old
  tracks (18 files, not used by the game). The **start-straight board** is the same in both versions: the same 5 screens
  (HOLD, READY, GO, FINAL, FINISH) and the same pictures; the files differ only in service bytes and the source path.

### GEN-8. Screen shake [code; appearance — ✓ video]
The game can "shake" the **whole picture together with the interface**: in a frame where a shake is requested, the image is shifted
by a random distance horizontally and vertically, in the next frame it returns to place, and so on every other frame while
requests continue. Strength `A` — from 2 to 30 conventional units; the shift on each axis — from `A` to `3A` in a random direction.
In the recording (PAL, 640×480) the shakes are short bursts of 0.05–0.25 s with shifts up to ~18 lines. During pause
and in some screen modes — no shake. The sources are of two kinds [code]:
- **request a shake every frame while active**, with constant strength; a strength below 2 is raised to 2:
  the Quake wave near the player's ship — strength 1–4 by distance (that is 2–4); Seismic Field — 1 (that is 2);
  destruction of the player's ship — strength grows as the destruction proceeds (SHIP-9);
- **hits on the player's ship** set a number `N`: the shake lasts `N` frames, and its strength in each frame equals the number of remaining
  frames (no more than 30 and no less than 2) — a strong jolt decaying to zero. A new hit replaces the number. There are half as many visible
  shifts as frames (a shift every other frame):
  - collision with another ship — `N` = 10 (0.2 s);
  - a hit on the track that removed shield — `N` = 5 × hit damage (a wall touch −1 shield — 5 frames, weak and short);
    a hit on some track objects — `N` = 30 (0.6 s) [code; not checked against a recording — the counter was not recorded then];
- **falling ice blocks on Cubiss Float** (FMT: files `ANIM_FALLING_ICEA…I.MEM` in the track folder) [code; ✓ race recording]:
  each block hangs until the **best progress among humans** (RACE-1, laps with fraction) exceeds its threshold, then
  falls with acceleration; when it touches the track — a hit with `N` = 20: a shake of 20 frames (0.4 s), from strength 20 down to 2,
  **wherever the player is**. Thresholds: A 1.10, B 2.13, C 2.15, D 1.16, E 1.13, F 3.13, G 2.10, H 2.115, I 1.13 (that is almost all on the
  first and second lap). Each block falls once per race. **In a one-ship race (Time Trial) the blocks do not
  fall** — so there is no such shake there either. This is the strongest shake in the game; in the recording the player's "shaking" marks
  came right after the block impacts.

### GEN-9. Demo version (disc SCED-50768) [✓ demo data files; the rest — code]
The demo from a Sony magazine disc (disc label "1.10" — the version of the **disc**, not of the game) contains an **earlier build**
of the game — two weeks older than the PAL release. Differences visible in the game:
- two tracks: Alca Vexus 2F and Florion Height 3F; there is a demo splash screen and an Arcade end screen offering to buy
  the game; the demo returns by itself to the demo disc menu (idle timer);
- ship parameters are the same; weapon damage is partly different: Flamer `Max` 0.1 (PAL 0.4, US 0.8), Bio Snare `Max` 0.5
  (PAL 1.0) — that is, the flamer was strengthened consistently from the demo to US;
- frame, clock and physics — as in PAL (GEN-1, PHY-1); the Alca Vexus 2F track file in the demo is an earlier variant
  (sections of different size), Florion Height 3F matches the release.

## Documents
| file | about | ID |
|---|---|---|
| [00_glossary.md](00_glossary.md) | terms | — |
| [01_game_flow.md](01_game_flow.md) | modes, race life cycle, start, pause, finish | FLOW |
| [02_ship.md](02_ship.md) | ship parameters, upgrades, shield and damage, states, input, teams and pilots | SHIP |
| [03_physics.md](03_physics.md) | substep, suspension, thrust, turns, surfaces, ramps, lava, collisions | PHY |
| [04_race_rules.md](04_race_rules.md) | laps and progress, places, perfect lap, league, challenges, medals, completion percentage | RACE |
| [05_ai.md](05_ai.md) | AI as a virtual gamepad, pilot character | AI |
| [06_weapons.md](06_weapons.md) | weapons: granting, damage, hit effects | WPN |
| [07_data_formats.md](07_data_formats.md) | game file and save formats | FMT |
| [08_open_questions.md](08_open_questions.md) | what is unknown or unverified | OQ |
| [09_test_cases.md](09_test_cases.md) | reference examples for implementation tests | TC |
| [QUESTIONS.md](QUESTIONS.md) | clean team question log | Q |
| [CHANGELOG.md](CHANGELOG.md) | specification releases and checks | — |

## Recommended implementation order
1. Data loaders: `.TRK` + `.LAP`, `SHIPS.INI`, `WEAPONSTATS.INI`, pilot INI, `GAME.BNI` (07).
2. Random number generator, clock, frame/substeps (GEN-1, GEN-4) — with tests TC-1…TC-3.
3. Ship physics (03) on recorded input.
4. Race flow: start, laps, progress, places, pause, finish (01, 04).
5. AI (05) — it writes the same input as the player, so it is plugged in on top of the finished physics.
6. Weapons (06), modes and player progress (04).
7. Menu, HUD, rendering, sound — your own, following the formats from 07.
