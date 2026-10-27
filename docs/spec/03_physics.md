# 03. Ship physics

## PHY-1. Time step [✓]
Frame = 20 ms = **2 substeps of 0.01 s each**. Confirmed by a frame-by-frame recording: the ship's displacement per frame
divided by `0.02·|v|` gives 0.9997 (median, ~25,000 frames, 6 tracks). The implementation must keep exactly 100 Hz:
the "forces" below are an **impulse per substep**, not a force in newtons; with a different step the handling will change.
For a display with a different refresh rate: the simulation stays at 100 Hz, and rendering is interpolated between frames.

A "by feel" reference for PAL is the player's impressions after races on both versions (GEN-7, "Races on both
versions"): sliding handling, a heavy craft, entering a corner early, frequent airbrake use, hard walls.

## PHY-2. Ship state (minimum for physics)
Position, velocity (vector), orientation (quaternion), live parameters (SHIP-4), part damage, shield, current
weapon, suspension/flight state, the nearest track section and the polygon under the ship.

## PHY-3. Order of effects in a substep
The order affects the result (especially the match with recordings), so it is fixed. [code; individual items — ✓]
1. Effective maximum speed (PHY-4).
2. Weapon input: reset, fire (WPN-6, WPN-8).
3. Target height (PHY-5) and suspension (PHY-6).
4. Brakes, gravity (PHY-7).
5. Steering, thrust, turbo (PHY-8).
6. Lateral friction and drag (PHY-9).
7. Velocity change by the sum of impulses (PHY-10).
8. Booster (PHY-11), external motion control (PHY-12).
9. Displacement `d = v · 0.01`. [✓]
10. Only in the **first** substep of a frame — collision with the track (PHY-13).
11. Movement (PHY-14), speed magnitude and direction of motion (PHY-15).
12. Orientation (PHY-16).
13. Lap progress (RACE-2), triggers and surface types (PHY-17…PHY-24), weapon pickup (WPN-3).

## PHY-4. Effective maximum speed [code; the "stricken" multiplier — ✓]
`maxspeed` (live) × pit lane limit (if the ship is on the pit lane, PHY-24) × "stricken" multiplier
(human only, WPN-10) × rubber band multiplier (RACE-7).

## PHY-5. Target height [code]
`h_target = rideheight − (nose_vertical_speed / max_pitch_angle) × noserideheightfactor`
plus a temporary height correction (on the ground; changed by AG Stinger and Gravity Bomb, WPN-14).
"Nose vertical speed" is the rate of change of the pitch angle; the exact order of the orientation computation remains open (OQ-1).

## PHY-6. Suspension [code]
A spring-damper along the normal `n` of the polygon under the ship. Height error `err = h_target − (position − point_under_ship)·n`:
- `err < 2.5`: `F = 3·mass·err·n − (n·v)·susdamping·k·n`, where k is the surface damping coefficient (PHY-18);
- `2.5 ≤ err < 4`: the same, but with constant damping: `F = 3·mass·err·n − (n·v)·2500·n`;
- `err ≥ 4`: spring only, amplified ×3: `F = 3·(3·mass·err)·n`;
- on a ramp — a separate mode (PHY-20); with no support under the ship `F = 0`.

## PHY-7. Brakes and gravity [code; behaviour at the start — ✓ player observation, PAL]
Gravity on uphill and downhill sections (`gravityhillup`/`gravityhilldown`), in flight — `gravityflying`; formulas — OQ-2.

**Airbrakes.** Each one (left, right) has its own braking force:
- while the brake is held, the force grows by a step per substep (the step depends on `brakehalfinc` / `brakefullinc` and `brakeforce`;
  which of the two is used when — OQ-2); when released — immediately 0;
- limit: if **one** brake is held — `brakeforce / 8`; if **both** — `brakeforce / 2` each (`brakeforce` together);
- the force is directed against the motion (in the ship's plane); in addition, with the brakes applied the lateral friction is replaced by
  `braketurndamping` (PHY-9) — the ship slides more easily in a turn;
- **"stop" below 100 km/h**: if both brakes are held, or one without throttle, the brake forces are zeroed, and the longitudinal
  drag (PHY-9) becomes **10 times** stronger — the ship stops quickly.
Consequences [✓ player observation, PAL; explanation — calculation]:
- **one brake + throttle from a standstill** — the ship does not move off: the brake (`brakeforce/8`, 3437 for Xios lead) is stronger than the thrust at
  low speed (`maxthrust · accelbottomforce` = 1667, PHY-8);
- **both brakes + throttle** — below 100 km/h the brakes are off and the ship accelerates; above 100 the brakes build up again and
  kill the speed; and so on in a cycle — the ship moves in **jerks**, the speed jumping roughly between 100 and ~200 km/h.

## PHY-8. Steering, thrust, turbo [code; thrust — ✓ Time Trial and League recordings, PAL, 100–900 km/h, discrepancy up to ~10 %]
Notation (in a 0.01 s substep): `s` — speed, km/h; `V` — live maximum speed (PHY-4, with upgrades,
damage and pit lane), km/h; `v_f` — projection of velocity onto the "forward" axis, units/s; `M` — live `maxthrust`
(with damage, SHIP-7); `m` — ship `mass`. Velocity changes by `ΣF / m` per substep (PHY-10).
- Steering — the `turn*` parameters; formula — OQ-1.
- **Throttle.** While the throttle is pressed (or turbo is active), the "requested thrust" = `M`, otherwise 0.
- **Thrust force `T`** along the "forward" axis (by the ship's `accel*` keys):
  | condition | `T` |
  |---|---|
  | no throttle | 0 |
  | `s < accelbottomspeed` | `M · accelbottomforce` |
  | `accelbottomspeed ≤ s ≤ V · acceltopzone`, the ship is accelerating (speed higher than in the previous substep) | `s · accelforcemultiplier` |
  | the same, but speed is not rising (climb, impact) | `M` |
  | `s > V · acceltopzone` | `min(M, M · acceltricklezone + reserve)`; `reserve` grows by `s / acceltricklefactor · 0.01` per substep while the speed is not falling, and is reset to zero below this zone |
  Example Xios lead (`accelbottomspeed` 90, `accelbottomforce` 0.15, `accelforcemultiplier` 7.15, `acceltopzone` 0.9,
  `acceltricklezone` 0.7, `acceltricklefactor` 1, `maxthrust` 11 111, `mass` 2500). `accelforcemultiplier` is the very
  number that the upgrade screen shows as thrust (×1100, SHIP-5).
- **Turbo** adds `M · turbopower · turbo_coefficient` while it lasts (`turbotime`).

## PHY-9. Drag and lateral friction [code; longitudinal — ✓ together with PHY-8; lateral — player observation and OQ-2 check]
- **Longitudinal drag** — only along the "forward" axis: `−k · v_f`, where `k = T / (V / 3.6)`. Therefore at any thrust
  the acceleration along the axis = `T · (1 − v_f / (V/3.6)) / m` and the speed tends to `V` by itself. When there is no thrust, `k` is computed
  from `M` and multiplied by **0.05** (while `s < V`) — when coasting the ship barely slows down. Above `V + 1` km/h on the ground `k`
  is computed from `M` and multiplied by `frictionfactor` (0.9 for Xios lead) — excess speed (booster, downhill) dies off quickly.
  Check: at 600–800 km/h Xios lead accelerates by ~350–380 km/h per second, and the calculation gives the same.
- **Lateral friction** — along the "right" axis: `−D · v_r`, where `v_r` is the lateral velocity: `D = turndamping` (live, with
  damage), at `s < 100` — 10; with the airbrakes pressed — `braketurndamping`. Plus a weak force turning the
  velocity toward the nose: `(nose·|v| − v) / (airbrakeslide + (L + R)·0.25)`, where L, R = 256 with the left / right
  brake pressed. How well the lateral friction matches the recording has not been verified yet — on the track it is masked by banked turns (OQ-2).
- Under the effect of AG Stinger the longitudinal drag is multiplied by `(1 − t/100)·10` (t — frames since the hit, WPN-14).
- **Nose reaction to touching a surface** (parameters `ndmaxdegrees`, `ndturnforce`, SHIP-3): while the ship is in the air, the threshold is the value
  from the file (300 for all teams, 1 for the escape pod); on contact with a surface it is recomputed every frame from the angle between
  the hull and the surface normal (below the threshold — zeroed). With an angle not below the threshold, an impulse of strength `ndturnforce`
  is applied to the pitch (1000 for the teams, 3000 for the zone ship, 1 for the escape pod) — after landing the ship "pecks" with its nose
  the harder, the larger `ndturnforce` and the steeper the impact. Landing after a flight additionally produces sparks and a sound depending on speed.
  Units of the recomputed angle — OQ-3; in-game check — the Florion 3F ramp and steps F1–F3.

## PHY-10. Velocity change [✓ in form]
`v += ΣF / mass` — **without** multiplying by the substep duration.

## PHY-11. Booster [code; k for the human — ✓ consistent]
On a booster trigger: `v += forward · |v| · k`, k = 0.03 for the human, 0.006 for the AI. Boosters are of two kinds
(a flag in the booster object in the `.TRI`, FMT-25): **normal** (k as above) and **weak** — k = 0.008 **for both the human
and the AI** [code]. Weak ones exist only on Florion Height (all 6 layouts) and Cubiss Float 3F, normal ones — on all tracks
of the three examined [✓ data from 18 `.TRI`]. Boosters are polygon triggers, not the `speed` surface type (PHY-17).
The addition applies **every substep** while the ship is on the booster: for the human the speed grows by 5–6 % per frame
for several frames in a row (1.03² ≈ 1.061 minus ordinary drag) [✓ all 15 recordings].

## PHY-12. External motion control [?]
There are two modes in which the ship's motion is set not by physics:
- position and velocity are set externally — probably when a rescue droid carries the ship (PHY-22);
- the ship is pulled toward another ship with force ×3 — probably the Bio Snare effect.
Details — OQ-9.

## PHY-13. Collision with the track [✓ fact; mechanics — OQ-6; wall impact — PHY-25]
Only in the first substep of a frame: collision with the geometry of the current section. On crossing — push-out along the normal
(except the `wall` surface type on the ground, PHY-17), impact sound, sparks at speed > 100.
Any touch of the geometry marks the current lap as "not perfect" (RACE-8).
Observation (Time Trial, Mandrashee 2R, 9 laps with frequent wall touches) [✓]: **an ordinary wall touch takes
1 unit of shield** (median; hard impacts — more, SHIP-6); at a speed of ~1000–1400 km/h a touch costs on average ~26 km/h of speed. Touches come in series:
17 series of 2–4 touches with an interval < 1.5 s, in 16 cases the next touch is against the opposite wall
("ping-pong" on narrow sections, noted by the player). The strength and shape of the rebound — OQ-6.

## PHY-14. Movement [code]
`position += d`, limited by a downward ray so that the ship does not fall through the track surface.

## PHY-15. Speed magnitude and direction of motion [✓]
After movement, `|v|` and the unit direction of motion are computed. On the frame of an impact the direction is computed **before**
the velocity correction by the impact, so it may differ from `v/|v|` by up to 0.014. This matters only for bit-exact comparison.
The "moving forward along the section" flag = `(Δposition · section_forward) > 0` (FMT-3); needed for laps and wrong way.

## PHY-16. Orientation [✓ fact; formulas — OQ-1]
Steering, pitch, roll, alignment to the track. The quaternion is **not strictly normalised** at every step: its length in a race
reaches 1.001. For bit-exact compatibility this matters; for a game "by feel" it does not.

## PHY-17. Surface types [✓]
The surface type is determined **by the material name** of the polygon (`SURF`, FMT-3): the name is checked for the presence of keywords
in table order, the **last** match wins. Verified on 15 tracks.

| type | key in the name | effect | where present |
|---|---|---|---|
| 0 | (none) | ordinary | everywhere |
| 1 | `flip` | flip (PHY-23) [code] | nowhere |
| 2 / 3 / 4 | `air1` / `air2` / `air3` | ramp (PHY-20) | air3 nowhere |
| 5 | `wall` | wall (does not push out on the ground) | everywhere |
| 6 | `speed` | booster [code] | nowhere (boosters are triggers, PHY-19) |
| 7 | `start` | start/finish line (RACE-3) | everywhere |
| 8 / 9 | `pitlane` / `piteffect` | pit lane (PHY-24); 9 — also recharges the shield | all except devilia |
| 10 | `invisible` | invisible wall | cubiss_float, vohl_square 2F, alca_vexus and others |
| 11 | `loop` | loop | **only florion_height** |
| 12 | `barrier` | barrier | everywhere |
| 13 / 14 | `L_DUST` / `N_DUST` | dusty surface, particles of the colour `_R_G_B` from the name | florion; cubiss, mandrashee, temtesh 2–3; vohl 3 |
| 15 | `lava` | lava (PHY-21) | **only florion_height 2F/2R** |

## PHY-18. Surface subtype and damping [code]
The subtype (sound, particles, suspension damping) by a key in the name: `water` 1, `ice` 2, `rock` 3, `sand` 4, `stone` 5, `damage` 6.
The suspension damping coefficient k (PHY-6) is chosen **by the subtype** of the surface under the ship [code, OQ-10 closed]:

| subtype | none | `water` | `ice` | `rock` | `sand` | `stone` | `damage` |
|---|---|---|---|---|---|---|---|
| k | 1.0 | 2.4 | 1.2 | 0.1 | 0.1 | 0.4 | 1.9 |

The smaller k is, the less the ship's oscillation on its suspension is damped: on rock and sand the ship visibly "bounces",
on water and the "damaging" surface the oscillation is damped more strongly than usual. (The earlier note "16 coefficients in a row"
was an error in reading the table.) Not verified in the game.

## PHY-19. Polygon triggers [code]
Separately from surface types there are special polygons: booster (PHY-11), weapon pad (WPN-3), flip (PHY-23),
mines/traps. **In the data they are `.TRI` objects** (object type: 6 — booster, 7 — weapon pad, 8 — flip,
10 — mines/traps; FMT-25), not `.TRK` polygons [code]. When the track is loaded the objects are distributed among sections; the ship
checks only the objects of its own section: a hit is the ship's point inside the object's box (in its own
coordinates, with a margin in height) [code]. The object's mask sets in which layouts it is active [code].

## PHY-20. Ramps [code; ✓ Time Trial Florion Height 3F recording, PAL, 2 laps — 4 jumps from ramps]
`air1` / `air2` / `air3`: jump height 160 / 70 / 150, hang time `400 / speed` s. Details of the suspension mode on a ramp —
OQ-1. Ramps exist **only on Florion Height 3F** (one `air1` and one `air2`), `air3` — nowhere.
What it looks like at ~950–1050 km/h [✓]:
- on a ramp the ship gets a sharp **upward kick**; the speedometer shows the full speed including the vertical component,
  so at the moment of the kick it jumps to ~2050–2400 km/h and returns to the previous value in ~0.35 s — the speed along the track
  barely changes;
- `air1`: rise of ~160 above the point before the ramp, ~0.6 s in the air; `air2`: ~75–80, ~0.4 s; at the apex the ship
  nearly hangs (vertical speed drops slowly) and lands softly on the track surface further on — no impact and no shield loss.

Free flight (a track break, Florion Height 3F, progress ≈ .825 lap; twice) [✓]: a fall of ~1100 units downward
takes ~3.9 s; the ship accelerates downward slowly (vertical speed by the end ~330–460 units/s), while the **speed along the
track in the air dies off** — from ~1050 to ~500 km/h; the speedometer meanwhile shows a growing full speed (up to 1400–1700).
Landing — without shield loss: the vertical speed vanishes, the speed along the track is immediately ~750–800 km/h.

## PHY-21. Lava [✓ frame-by-frame observations: player falling on florion_height 2F]
Lava is a flat lake at height 75 under two sections of florion_height 2F/2R, 30–170 below the track surface. One can get there
only by falling off the track.
- The ship **hovers over lava as over an ordinary surface** and **does not lose shield**.
- The lava time counter grows by 1 per substep (100 per second):
  - up to 0.6 s nothing happens;
  - from 0.6 s the ship **burns**: every substep the maximum speed (`maxspeed`) is multiplied by 0.8, but does not drop below 50; it crawls at ~175 km/h and cannot get out;
  - at 1.4 s — a commentator line and an on-screen message;
  - **at 7.0 s the ship is removed from the race** ("dropped out"); the player gets last place, the race is over for them.
- The counter is **not reset** on leaving the lava: it grows only on lava and accumulates between visits until the ship
  is fully reset (restart, respawn). [code]

## PHY-22. Falling off the track, returning to the track [✓ video and recording, Time Trial Alca Vexus 2F, PAL; ✓ player observation; the rest — code]
What it looks like for a player who has fallen off the track into the abyss [✓]:
1. the ship falls for ~0.5 s, the screen **fades to black** during that time;
2. ~0.6 s of black screen;
3. the screen fades back in, the ship is already **standing on the track** near the place of the fall, nose along the direction of travel, and is held
   in place for ~0.5 s; then it is released — acceleration **from zero**;
4. the shield does not change, the lap time keeps running throughout; in total ~1.5 s is lost plus the acceleration.
Both falls in the same place put the ship back at **the same point** of the track.
**Where it places** [code; ✓ race recording]: some track sections have a **return point** (in the `.TRK` — 12 bytes after
the section flag, FMT-3; on Alca Vexus 2F — 29 sections out of 224, roughly every fifth to eighth). About 0.5 s after
the fall the game takes the one of these points that is **closest in a straight line** to the ship at that moment (not the nearest along the
direction of the track — it may be behind as well as ahead), places the ship slightly above it (~30 units), nose along this section, and
releases it with zero velocity. In the recording: the ship fell 200–300 units from the point of section 49 — both times it was placed on it.
No droid is visible on screen (camera behind) — the "rescue droid" exists only in the game's design: no more than 4 ships can
be rescued at once; if all 4 slots are taken, the human's ship takes the slot from an AI ship, and the others are
put back on the track immediately [code]. The return starts only while the ship is in the air [code].

A ship that has flown off the edge of the map returns to the track **without taking damage** [✓ player observation].

## PHY-23. Flip [code]
Flip: the ship is pushed along the normal until a timer expires. There is no `flip` surface in the tracks; a flip may be triggered by a polygon trigger (PHY-19, OQ-8).

## PHY-24. Pit lane [✓ frame-by-frame: 4 player passes and 12 AI passes on three tracks; weapon effect — code]
The pit lane works only if it is **enabled in the event** (a race parameter, FLOW-3). If disabled, the `pitlane` and
`piteffect` surfaces behave as ordinary ones: there is neither a limit nor recharging (verified in the Elimination challenge).

If enabled:
- **Speed limit.** On both surfaces the effective maximum speed (PHY-4) is multiplied by **0.5** — identically for all
  ships. The speed is not cut instantly: a ship that enters fast slows down by ordinary physics.
- **Recharging** — only on `piteffect` and only if the shield is above 0.9 (a ship being destroyed is not repaired). Every substep:
  - the shield grows by 0.0035 of the full shield (0.35 of the full shield per second; from zero to full ≈ 2.9 s), but not above full;
  - part damage (SHIP-7) decreases by 0.007, not below 0; when the shield reaches full, it is zeroed;
  - in two-player modes the shield is additionally capped by the player's handicap (a percentage of full) [code].
- Weapon hits on the pit lane deal damage as usual; recharging catches up with it.
- Recharging removes a long-lasting weapon effect that is passed on by touching ships (which weapon this is — OQ-31) [code].

The AI's decision to enter the pit lane — AI-8.

## PHY-25. Wall impact [code; ✓ modified game, PAL (test races); ✓ player observation, PAL (Florion Height 1F)]
Walls and barriers (the `wall` and `barrier` surfaces, PHY-17) are separate surfaces on top of the track: the suspension **does not see them**
(they are not a floor), only the wall impact check examines them. The check is once per frame (PHY-3), for each ship, against the walls of the
**current section** (PHY-13).
- **Contact points.** Segments are drawn from the ship's centre to three hull points: the left and right sides (slightly below the
  centre) and the nose; the dimensions are specific to each ship (for Xios about 3 sideways, about 1.9 down, the nose about 7.5–8 forward).
  A fourth segment is the ship's path from the previous position to the current one, so that a fast ship does not skip past a wall between
  frames. A touch counts if a segment crosses a wall triangle, approaching it from the front side.
- **Response.** The push-back direction is the **smoothed wall normal at the point of impact**: a blend of the normals of the three vertices
  of the triangle in proportion to the point's closeness to each. Along this direction the ship is pushed out by the part of the
  segment that went past the wall; the velocity component into the wall is killed; the ship gets a turning kick; sound,
  sparks at speed > 100, damage (SHIP-6), shake (GEN-8).
- **Consequence for track data (FMT-3).** The wall vertex normals must point out of the wall, like its surface.
  Zero normals — no push-back, the ship passes through the wall; "up" normals (vertices shared with the road) —
  the ship is lifted at every touch and climbs over the wall. In the original tracks the walls are separate strips
  of triangles with their own vertices (almost nothing shared with the floor), and the floor continues under the wall.
- The strength of the rebound and turn in numbers — OQ-6.
