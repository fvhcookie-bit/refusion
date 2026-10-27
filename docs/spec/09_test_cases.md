# 09. Test cases

Examples by which an implementation can be checked with automated tests without running the original game.
The "source" column: **observation** — the number was seen in the game; **calculation** — a direct consequence of the rule
(the test checks that the rule is implemented as written).

| ID | rule | input | expected result | source |
|---|---|---|---|---|
| TC-1 | GEN-4 | seed = 1, three calls | 1103527590, 377401575, 662824084 | calculation |
| TC-2 | GEN-4, FLOW-5 | Time Trial: T = 4.0 → seeding `floor(4.0·64)` = 256; two calls | 1179557177, 1987477374 | calculation |
| TC-3 | FLOW-5 | 11 starts in ordinary modes | all T in [4, 7); 4.06…6.97 were observed | observation |
| TC-4 | GEN-3 | `|v|` = 258.45 units/s | speed 930.4 "km/h" (the screen showed 926 at that moment) | observation |
| TC-5 | SHIP-5 | Feisar lead: `maxspeed` 1062, upgrade TOPSPEED 4; `shield_standard` 53, SHIELD 5 | live `maxspeed` 1432; shield at start 98 | observation |
| TC-6 | PHY-21 | burning ship, `maxspeed` 1062, substeps | after 3 substeps ≈ 544; after 13 ≈ 58; then 50 | observation |
| TC-7 | SHIP-9 | destroyed at `maxspeed` 1450, frames | after 60 frames (1.2 s) ≈ 0.40 of the original; 50 is reached at about frame 223 (~4.5 s); eliminated at frame 360 | observation + calculation |
| TC-8 | WPN-10 | Rocket hit on a human, frames | speed multiplier: minimum 0.24 after 76 frames of decline, return to 1.0 after another 19 frames, ~1.9 s in total | observation |
| TC-9 | WPN-12 | Gravity Bomb, shooter with `weapon_standard` 1.1; target hit at c = 41 | k = 0.82; damage 12.628 (−12.63 in the game); AG Stinger effect lasting 102 frames; the target was at a distance of 100…134 from the blast (at the check at c = 45 it was not hit) | observation |
| TC-10a | RACE-11, RACE-12 | league: player 14 + 14 + 10 = 38, best opponent 34 | win | observation |
| TC-10b | RACE-11, RACE-12 | league: player eliminated (kills 0) → 0; 1st place + 1 kill → 14; eliminated with 1 kill → 2; total 16, leader has 26 | not a win | observation |
| TC-11 | RACE-17 | Arcade: one 1st and one 2nd place (A = 5); 1 league win in 1–4 (L = 9 → Lp = 5); challenges: gold 3, silver 1, bronze 2 (C = 13); the rest 0 | percentage 5 | observation (save summary) + calculation |
| TC-11b | RACE-17 | all groups at maximum (A = 126, L = 153, C = 144, T = 126, Z = 10) | percentage 100 | calculation |
| TC-12 | RACE-8 | florion_height 2F, 3 laps: contacts on the 1st and 3rd, 2nd clean | perfect-lap counter 0 → 1 after the 2nd lap, does not grow further | observation |
| TC-13 | SHIP-6, RACE-14 | duel: player's shield 9, wall contacts | −1 per contact | observation |
| TC-14 | WPN-11 | Plasma Bolt on a ship with shield 77 | shield 0 in one frame, ship destroyed, kill to the shooter | observation |
| TC-15 | WPN-14 | AG Stinger, original `rollmaxangle` 6000 | over the last 20 frames the roll grows by 295 per frame; full cycle 100 frames (2.0 s) | observation |
| TC-16 | RACE-2 | florion_height 1F | all lap progress values are multiples of 1/445; ships in the same subsection have equal progress | observation |
| TC-17 | FLOW-12 | the player finished 2nd, 4 more seconds of race | the finish table has 2; the current position may show 3 | observation |
| TC-18 | PHY-17 | material names of all 45 tracks | surface types per the PHY-17 table (lava only on florion_height 2F/2R, loop only on florion_height) | observation |
| TC-19 | FMT-3, FMT-4 | all 45 `.TRK` and `.LAP` files | are read to the last byte; the number of `.LAP` records = the number of subsections; the check number = the size of `C*.TRI` | observation |
| TC-20 | FMT-17…FMT-19 | `SHIPS/FEISAR/VENOM/SHIPMESH.MEM` | 3 top-level objects (69, 13 and 1 nodes); 3101 + 483 + 78 = 3662 triangles; the full model has 5 textures 128×128, 8 bit | observation |
| TC-21 | FMT-18, FMT-20 | all 78 models (`.MEM` of ships and tracks) | the number of triangles gathered by walking the node tree and the second set of packets equals the number of triangles in all vertex chunks of the file | observation |
| TC-22 | FMT-20, FMT-3 | `FLORION_HEIGHT1F.MEM` and `.TRK` | the `.TRK` vertices lie on the vertices of the visible model (median distance 0) | observation |
| TC-23 | FMT-22 | `SHIPS/FEISAR/VENOM/SHIPMESH.MEM`, full model | 12 groups in order: ENGINE, STABILITY, NOSE, STABILITY, ENGINE, STABILITY, CANOPY, COCKPIT and 4 brake flaps; each has one damaged version; debris pieces 6, 7, 6, 7, 5, 5, 4, 4, 0, 0, 0, 0 | observation |
| TC-24 | FMT-23 | the same ship, CANOPY group | 8 keys, length 180 frames; rotation grows to ~60° by frame 179, translation constant | observation |
| TC-25 | SHIP-14 | Feisar lead, levels 3, 1, 3, 3, −1, 4 | `p = 73` → `RAPIER`, class 3; all levels −1 → `p = 0` → `VECTOR`, class 1 | observation |
| TC-26 | FMT-20 | all 45 tracks | for each of the 5979 texture entries there is a file `TEXTURES/<name>.MEM` with one texture | observation |
| TC-27 | PHY-24 | pit lane enabled; full shield 53, shield 6.0 on entering `piteffect` | +0.371 per frame (2 substeps); full shield 53 after ~127 frames; effective maximum speed = 0.5 of normal | observation |
| TC-28 | PHY-24 | pit lane disabled in the event; shield 17.2 of 51 | on `piteffect` the shield does not change, no speed limit | observation |
| TC-29 | AI-8 | level-2 pilot, shield 30 of 60 | `p = (100 − 50) × 0.8 = 40` % | calculation |
| TC-30 | RACE-5 | two ships with equal progress in the same section, one 3 from the entry gate line, the other 7 | the second is ahead | calculation |
| TC-31 | FLOW-6 | Arcade, AI at the 3rd start position (s = 2); level-1 AI at position 13 | burst 0.14; no burst, throttle released from T + 0.5 to T + 1.0 | calculation |
| TC-32 | RACE-7 | the setting is the third value, the reference at progress 2.0, the ship at 2.5 | multiplier 0.85 | calculation |
| TC-33 | SHIP-16 | single race; player levels 3, 1, 3, 3, −1, 4; the opponent has n = 5, 3, 5, 5, 3, 3 | opponent levels 3, 2, 3, 3, 2, 2 | observation |
| TC-34 | RACE-22 | player's shield 2 notches (20 %), full ship shield 71; AI shield 7 notches (70 %), full 82 | at the start 14.2 and 57.4 | observation |
| TC-35 | RACE-22, SHIP-16 | upgrade level 3 (q = 67); the ship has n = 5, 3, 5, 5, 3, 5 | levels 3, 2, 3, 3, 2, 3; class 3 | observation |
| TC-36 | RACE-23 | a human's ship is destroyed, resurrection on | after 8.2 s back in the race at the same place, shield full × percentage | observation |
| TC-37 | PHY-8 | a ship without upgrades, Time Trial, standing start, full throttle, no steering | time to 100 / 300 / 500 / 800 / 930 km/h: 0.5 / 1.8 / 2.6 / 4.1 / 7.0 s (±0.1) | observation |
| TC-38 | PHY-9 | same, release the throttle at 930 km/h, do not brake | exponential decay, `k` = 0.0763 /s: 934 → 622 km/h in ≈ 5.3 s | observation |
| TC-39 | PHY-9 | a straight, no brakes, a short steering input | the lateral velocity decays with `D` = 54.7 ± 0.3 at any speed from 30 to 1048 km/h | observation |
