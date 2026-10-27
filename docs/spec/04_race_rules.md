# 04. Race rules and player progress

## RACE-1. Sections and lap progress values [✓]
The track is divided into sections, and sections into subsections (FMT-3). For each subsection the `.LAP` file (FMT-4) gives
a **lap progress** 0…1. In every substep a ship belongs to one subsection.

## RACE-2. Progress [✓]
`progress = lap − debt + subsection_fraction`, where **debt** is the number of backward crossings of the start line
(compensated by crossing it again forwards). Progress is **stepped**: ships in the same subsection have it identical
to the bit (on florion_height 1F the step is 1/445 of a lap). Recomputed every substep.

## RACE-3. Lap counter [✓]
0 until the first crossing of the start line (the starting grid is in front of the line), then 1, 2, …
The finish is when the counter becomes `number_of_laps + 1` (FLOW-11).

## RACE-4. Lap time [code]
Lap time = race clock at the moment of crossing − lap start time (pauses are not counted, FLOW-9). The following are stored: the time of the
last lap, of the best lap, the times of the first three laps and the track record (by track code).

## RACE-5. Positions [✓]
- Current positions are a sort by progress in descending order; ships that are out of the race go to the end.
- With **equal progress** (RACE-2: ships in the same subsection) [✓ 13,900 cases of equality in two races, 99.8 % matched]:
  1. the one whose **nearest section** of the track has the larger number is ahead;
  2. if the section is the same, the one who is **farther from the entry gate line** of the section is ahead (the distance from the ship's position
     to the line through the first two gate points, FMT-3).
  The rare mismatches in the recording come from positions being recomputed inside the frame while the recording is taken at its end.
- Final positions are the finish table (FLOW-12).

## RACE-6. Wrong way [code]
The "wrong way" counter is set to 140 frames (2.8 s; in Zone, 20 frames, 0.4 s) while progress is not less than the best
reached, and decreases by 1 per frame while it is less. When it reaches 0: "wrong way" is shown, the counter is
again = 140 frames; in Zone, **1 unit of shield** is also taken away (or the remainder, if less than 1). So in Zone when driving backwards
the first loss comes after 0.4 s, then every 2.8 s. [code]

## RACE-7. Rubber band [code; "off by default" and the menu labels — ✓]
The **catch-up** setting has three values — **off / low / high** [✓ settings screen, PAL] — and is set **in the two-player mode menu** (on the same screen as the players' shield handicap and the number
of opponents); by default it is **off**. For each ship:
`multiplier = clamp(1 − (progress − reference_progress)·k, 0.5, 1)`, k = **0.1** for low and **0.3** for
high (in menu order of the values). **The reference is the first player's ship.** The multiplier limits the maximum speed (PHY-4), that is,
it **slows those who are ahead of the reference**. Works in single-player modes and in two-player Arcade (not in the other two-player modes);
while the setting has not been touched, the multiplier is always 1. [✓: in all 15 recorded races — Arcade, league, challenges — the multiplier
of every ship is exactly 1]

## RACE-8. Perfect lap [✓]
A lap on which the ship **never touched the track geometry** (PHY-13). A touch marks the current lap,
crossing the start line clears the mark. If a lap is closed without touches (and it is not the starting crossing, and the lap
is not greater than the number of laps) — the "PERFECT LAP" caption appears, the commentator says a line, and the player's perfect-lap counter grows.
Example — TC-12.

## RACE-9. Messages on lap close [code]
"FINAL LAP" — the last lap has begun (if laps ≥ 2); "NEW LAP RECORD" — the track record was beaten; "PERFECT LAP" — RACE-8.
In Time Trial, when a lap is closed whose time has passed a medal threshold, a medal caption appears (bronze / silver / gold),
three times as long as "FINAL LAP". All these captions are 3D letters made of cubes with lagging copies ("echo").

## RACE-10. League: schedule [✓ two leagues of 3 races]
A league is a schedule of up to 8 events (FMT-9). The first three leagues are called "rhea", "oceanus", "tethys league".
The first league: florion_height 1F, mandrashee 1F, cubiss_float 1F.

## RACE-11. Points per race [✓ 96/96 point values]
For each of the 16 slots: `position_points + 2 × kills`. Position points by final position:
**12, 10, 8, 6, 5, 4, 3, 2, then 1**. A ship that is eliminated gets 0 for position but keeps the points for its kills.
Kills are opponents destroyed by this ship in this race (SHIP-10). The league total is the sum over the races.

## RACE-12. Winning a league [✓]
The player's total is **equal to the maximum** among the slots (a tie is also a win). Winning unlocks the next league
(FMT-9), the tracks of its races, the league's additional bonus (if any) and marks the league as completed (FMT-10).
Examples — TC-10.

## RACE-13. Challenges: general [✓ all 6 Feisar challenges]
Six challenges per team. Medals are bronze/silver/gold by the event's three thresholds (FMT-8);
a higher medal includes the lower ones. Medals are written to the profile (FMT-10).

## RACE-14. Challenge types
| type | condition | thresholds (Feisar example) | evidence |
|---|---|---|---|
| 0 race position | final position ≤ threshold | 5 / 3 / 1 | [✓] |
| 1 lap time | best lap time ≤ threshold, s | 41 / 39 / 37 | [✓] |
| 2 **Elimination** | number of opponents destroyed **by the player** ≥ threshold; the medal is awarded **at the moment** of the kill, in the middle of the race; elimination without a culprit does not count | 1 / 2 / 3 | [✓] |
| 3 **duel** | 2 ships, 1 lap, weapon pads switched off, player's shield 9; gold only — for 1st place | — / — / 1 | [✓] |
| 4 survival | laps completed = threshold | 1 / 2 / 3 | [code] |
| 5 special | bots do not pick up weapons, the player does once; at the start the second ship gets a boost | | [code] |

## RACE-15. Time Trial [code]
Medal thresholds are in seconds, in Arcade events (FLOW-2). **Ghost** [code]:
- every 10 frames (0.2 s) the position and rotation of the player's ship (full matrix) are recorded with the frame number, at most
  900 records (3 minutes of a lap); after that the lap is not recorded;
- two buffers: the current lap is written to one, the ghost is shown from the other; at the end of a lap, if the time is better than the
  ghost's time, the buffers are swapped — the ghost becomes the best lap **of this run**;
- the first crossing of the line (start) only clears the recording; the ghost is not saved to the memory card.
- What it looks like [✓ player observation, PAL, Florion Height 3F]: from the 2nd lap — a **semi-transparent
  smoky ("glass") copy of the player's ship** of this session, trailing an equally smoky trail. There are no other
  effects: no engines, no lights, no team colouring. The ghost passes through the player's ship and through
  walls, does not react to weapons and pads, and is visible far ahead too. On lap 1 there is no ghost.
- The ghost is a **deterministic recording**: it moves along the trajectory and at the speed of the best lap, the environment does not
  affect it [✓ player observation].
- At the start of a session there is no ghost; it is not carried over between sessions — only the **time** of the best
  lap is written to the memory card. The ghost recording is replaced every time a best lap is set in the current session [✓ player observation].

## RACE-16. Arcade results [✓]
For each track the best position among the first three (1st / 2nd / 3rd) is remembered, FMT-10.

## RACE-17. Completion percentage [code; profile check — TC-11]
For each group points are computed as `3·gold + 2·silver + 1·bronze`; for each track/challenge only the
highest medal counts (for Arcade: 1st place = gold, 2nd = silver, 3rd = bronze):
- Arcade (42 tracks): `A`, share `A·100/126`;
- challenges (48): `C`, share `C·100/144`;
- Time Trial (42): `T`, share `T·100/126`;
- leagues: `L = 9·(wins in leagues 1–4) + 15·(5–8) + 21·(9–10) + 3·(extra league marks)`, share `Lp = floor(L·100/153)`;
- one more group of extra marks `Z` (3 points per mark, out of 10; meaning — OQ-22).

`percentage = floor((A + floor(Lp·1.53) + C + T + 3·Z)·0.17271 + 0.99)`; 100 only if all shares equal 100,
otherwise at most 99. Which 42 tracks are included in Arcade and Time Trial — OQ-23.

## RACE-18. What the percentage unlocks [code]
Percentage thresholds unlock weapons (at > 0, 2, 4, 6, 8, 10, 12) and bonuses (at > 29 and > 59). Which exact weapon
at which threshold and which bonuses — OQ-24.

## RACE-19. Zone [✓ behaviour — player observation; points — code]
A survival challenge on one lap of a track. Behaviour according to player observation:
- the player controls a **special ship with unique handling**;
- **the throttle is always pressed**: the ship drives itself, the player only steers;
- there is no shrinking zone: the ship moves along the track until it is **destroyed by repeated wall
  touches** — each touch takes away shield, and after several the ship is destroyed;
- as the level rises, the ship's **maximum speed grows**;
- **booster** pads on the track are active; weapon pads are inactive: **no weapon is given, the pit lane does not
  work**.
From the code only the points scoring is known: a multiplier up to ×99, bonuses for boosters and laps; the growth of thrust, brakes,
turning and `gravityflying` with level is also code. [code]
Driving backwards is punished: the first shield loss after 0.4 s, then every 2.8 s (RACE-6) [code].
The exact scoring numbers — OQ-25.

## RACE-20. Eliminator and Endurance [code; no observations]
- **Eliminator**: the winner is the one who destroys opponents; kills are counted as in a league (RACE-11). The rules and
  victory conditions have not been checked in practice: [?: not observed] (OQ-25).
- **Endurance**: [?: not observed]; the only thing known from the code is that the reset button in this mode fires
  the Proton Cannon from a separate supply (WPN-8). Rules — OQ-25.

## RACE-21. Elimination of ships a lap behind [✓ Arcade; league — code]
When, during the placement of positions (RACE-5), the progress of two adjacent ships differs by **more than 1** (one lap),
the one behind is **eliminated**: its shield becomes 0 and it is removed from the race in the same way as those eliminated at the end of a race (FLOW-12).
Does not apply: on devilia, in two-player modes, to ships already eliminated or finished.
For the player this looks like an ordinary destruction: shield 0, the caption "shield energy critical", the animation (SHIP-9);
there is no separate caption. In Arcade the results show **last place** ("position: 16th", "no medal awarded").
In the finish table it is "eliminated", so in a league it gets only the points for kills (RACE-11). [✓ modified game, US: the player
stood at the start, was removed when the 15th ship went a lap ahead; results — 16th place; the recording was made on the US version —
the time of removal does not carry over to PAL; league points — code]

## RACE-22. Two-player race settings [code; ✓ modified game, PAL]
The two-player mode settings screen sets:
| setting | values | effect |
|---|---|---|
| number of laps | 1–10 | replaces the event's number of laps |
| shield of player 1, player 2, AI | 10 steps of 10 %; 0 steps = 5 % | the shield at the start and on resurrection is multiplied by the percentage; pit lane recharge does not raise the shield above this percentage (PHY-24) |
| number of opponents | 0–10 | ships = opponents + 2 |
| upgrade level | 1–4 | speed class = level; for **all** ships each upgrade group = `⌈(n − 1) · q / 100⌉`, q = 0 / 34 / 67 / 100 (SHIP-16) |
| pit lane | on / off | PHY-24 |
| resurrection | on / off | RACE-23 |
| catch-up (rubber band) | off / low / high | RACE-7 |
| screen split | horizontal / vertical | — |

- The highest available upgrade level = the version (SHIP-14) of the most upgraded ship in the profile: upgrade share
  < 25 → 1 (and the row is skipped by the cursor), < 50 → 2, < 75 → 3, otherwise 4.
- Values are saved in the profile. Defaults: 3 laps, shields 100 %, 6 opponents, level 1, pit lane on,
  resurrection on, rubber band off.
- Weapon pads are always on in two-player.

## RACE-23. Resurrection [code; ✓ 26 resurrections in a row in a recording]
Only in two-player modes and only for **human ships**, if enabled (RACE-22):
- a destroyed ship (SHIP-9) is not eliminated; **8.2 s** after destruction it is restored **in the
  same place**: shield = full × the percentage of that player's shield, node damage reset, destruction stages cleared;
- if resurrection is off — it is eliminated, as in single-player modes (after 7.2 s).
When destroyed, the AI additionally gets a throttle lockout that is never lifted (it is not needed, since the AI is eliminated).

## RACE-24. Credits for a race [code; ✓ 9 league races — 4 PAL, 5 US, all sums matched]
Credits are awarded **only in a league** (single-player and two-player) — after each race, on the results screen (the sum
flows into credits over ~6 s). The sum consists of four parts. The multiplier `k` is the league share in the completion percentage `Lp`
(RACE-17, 0…100; if 0, it is taken as 1): the further the leagues are completed, the more is paid.
| part | amount |
|---|---|
| position | 15,000 in leagues 1–4, 30,000 in leagues 5–8, 50,000 in leagues 9–10; plus for position: 1st +5,000, 2nd +3,000, 3rd +1,000, others +500; plus `1650·k` |
| kills | 15,000 + `k` × (2,000 for each opponent destroyed by the player; with no kills — 1,000) |
| perfect laps | 15,000 + `k` × (1,500 for each perfect lap, RACE-8; with none — 750) |
| time | by the **average lap time** against the Time Trial thresholds of this track (FLOW-2): not slower than gold — 15,000, silver — 12,000, bronze — 10,000, slower — 7,000; plus `0.3·k` credits for each millisecond by which the average lap is faster than the bronze threshold; if it is faster by less than 500 ms or slower altogether — it is counted as 500 ms (that is, not less than `150·k`) |
If the player's ship is not listed in the race at the end — nothing.
Example (PAL, league themis, `k` = 5): 1st place, no kills and no perfect laps → 43,250 + 20,000 + 18,750 + 34,350
(time: gold + 19,350) = 116,350. Example (US, another profile, `k` = 1): 1st place, 2 kills → 36,650 + 19,000 +
15,750 + 15,993.
