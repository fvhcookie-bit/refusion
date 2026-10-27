# 08. Open questions

What is unknown or known only from the code. The `OQ-N` IDs are stable: rules refer to them. When a question is closed,
its row stays with the note "closed → rule ID" and the release number.

The "how to close" column: **observation** — a recording of the game is needed (a clean team can also make it, if the screen is enough);
**analysis** — work of the dirty team.

## Physics
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-1 | Orientation: steering, pitch, roll, alignment to the track; "vertical speed of the nose"; the suspension mode on a jump ramp | PHY-5, PHY-8, PHY-16, PHY-20 | analysis + observation |
| OQ-2 | Forces (thrust, the `accel*` curve, longitudinal drag — closed, PHY-8/PHY-9): **check lateral friction** on a straight (drift after a short steering input); for the **brakes** — which build-up step applies when (`brakehalfinc`/`brakefullinc`; the limits and "stop" — closed, PHY-7) and for **gravity** on climbs, descents, in flight | PHY-7…PHY-9 | analysis + a series of control runs |
| OQ-3 | The meaning of `frictionfactor`, `collisionTiming`, `ndmass`, `ndmaxdegrees`, `ndturnforce` — worked out by behaviour (SHIP-3): still open — who sets `collisionTiming`, the units of the recalculated angle, a check in the game of landing | SHIP-3 | analysis + observation |
| OQ-4 | Where the hull reference points come from | SHIP-13 | analysis |
| OQ-5 | Partly closed: a link between damage to the nose or other hull parts and the use, strength, speed, range and reload of a weapon has not been noticed; after the nose is destroyed a weapon can be picked up and used immediately [player observation]. Still to establish: the purpose of the `mdamage_decrease%` parameter and to check how the damageable hull elements are chosen: by the place of the hit or in sequence | SHIP-7, SHIP-15 | analysis + observation |
| OQ-6 | Collisions with the track and with other ships: push-out, bounce, wall damage. **Wall hit — the mechanics are worked out (PHY-25)**; remaining: the strength of the bounce and of the turning push in numbers, ship-to-ship collisions | PHY-13, PHY-25, SHIP-6 | analysis + observation |
| OQ-7 | Intermediate destruction stages (+1.2, +2.4, +4.4 s): what changes besides effects | SHIP-9 | analysis |
| OQ-8 | ~~How triggers are defined in the data; which booster is "special"~~ — **closed**: PHY-19 (`.TRI` objects), PHY-11 (weak boosters k = 0.008) | PHY-11, PHY-19 | — |
| OQ-9 | ~~Return to the track and the rescue droid~~ — **closed**: PHY-22 (the return point is the nearest in a straight line among the section points), SHIP-9 (the droid on destruction); attraction to a ship (Bio Snare?) moved to OQ-31 | PHY-12, PHY-22 | — |
| OQ-10 | ~~The damping table: does it index the surface type or subtype~~ — **closed**: subtype, PHY-18 | PHY-18 | — |
| OQ-14 | ~~Lava: is the counter reset on leaving the lava~~ — **closed**: PHY-21 (by code) | PHY-21 | observation for checking |
| OQ-17 | ~~Pit lane: the speed limit value, the shield recharge rate~~ — **closed**: PHY-24, AI-8 | PHY-24 | — |

## Race flow and rules
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-11 | ~~The AI start boost: where B and the AI start mode come from~~ — **closed**: FLOW-6 | FLOW-6 | — |
| OQ-15 | League Challenge: the event number `42 + league` coincides with the Arcade devilia events (42, 44, 46) — a formula error or intended | FLOW-2 | analysis |
| OQ-16 | ~~How positions are assigned to ships that did not reach the finish after the player finishes~~ — **closed**: FLOW-12 | FLOW-12 | — |
| OQ-18 | ~~The order of positions at equal progress~~ — **closed**: RACE-5 | RACE-5 | — |
| OQ-19 | ~~How much shield wrong way takes away in Zone~~ — **closed**: RACE-6 (by code) | RACE-6 | observation for checking |
| OQ-20 | ~~Rubber band: the correspondence of k to settings, who the reference is, the default setting~~ — **closed**: RACE-7 (the menu labels are off / low / high, checked) | RACE-7 | — |
| OQ-21 | ~~Time Trial ghost: what is recorded and shown~~ — **closed**: RACE-15 (by code + ✓ player observations: look, trail, determinism, not carried over between sessions) | RACE-15 | — |
| OQ-22 | The meaning of the group of extra marks Z and of the league extra marks; check the percentage formula on the save screen | RACE-17 | analysis + observation |
| OQ-23 | Which 42 tracks are included in Arcade and Time Trial for the percentage (45 tracks in total) | RACE-17 | analysis |
| OQ-24 | Which weapons and which bonuses are unlocked at each percentage threshold | RACE-18 | analysis + observation |
| OQ-25 | Zone: behaviour is closed by observation (RACE-19), from the code only the points scoring system needs to be found out. **Eliminator** — [?: not observed]; **Endurance** — [?: not observed]; both modes can be closed only by analysis | RACE-19, RACE-20 | analysis |
| OQ-45 | ~~Elimination of ships a lap behind: what it looks like to the player~~ — **closed**: RACE-21 | RACE-21 | — |
| OQ-36 | Cheats: which buttons correspond to the code symbols (8 codes of 5 symbols; the "unlock everything" code unlocks tracks, weapons, leagues, bonuses and credits, but not medals) | — | analysis |

## Ships, AI, weapons
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-12 | ~~Which upgrade levels the AI gets~~ — **closed**: SHIP-16 | SHIP-5 | — |
| OQ-13 | Where the "mass" number on the ship screen comes from (the upgrade screen — SHIP-5; credits for a race — RACE-24) | SHIP-5 | analysis |
| OQ-26 | AI: the influence of the steering coefficients, concentration/smoothness, the changes on the 3rd lap, two rare AI states | AI-2, AI-4, AI-6 | analysis |
| OQ-27 | ~~The `.TRI` and `C*.TRI` format~~ — the file format is described in FMT-25 and FMT-24; remaining: the link between `.TRI` objects and `.SPL` lines, the meaning of the patch fields and of link kind 1, of object types 5 and 10, the object mask; how the AI uses the line boundaries | AI-3, FMT-2 | analysis |
| OQ-28 | ~~Pickup conditions and the pad check mode~~ — closed: an active pad gives a weapon to a suitable ship; after giving it goes out at once, gives to nobody until the cooldown ends and does not recover during pause. If the ship is already armed, the pad does not go out. See WPN-3, WPN-8. | WPN-3, WPN-8 | observation |
| OQ-29 | ~~Instance limits; the Time Trial set; mapping a random number to weights~~ — **closed**: WPN-4, WPN-5 (by code). Behavioural questions remain: which factors change the result of choosing among permitted weapons, including a possible difference between the player and bots, the influence of the position/order of pads and the conditions for repeating one kind; for Time Trial — the behaviour of the boost being given at the finish. | WPN-4, WPN-5 | analysis + observation |
| OQ-30 | ~~The choice between `_Max` and `_Min`~~ — **closed by code**: the pressure of the fire button, WPN-9; check in the game with a pressure-sensitive gamepad | WPN-9 | observation |
| OQ-31 | Weapon behaviour: rockets, Missile, Super Missiles, Grenades, Mines, Quake, Power Swarm, Plasma Bolt (WPN-11), Flamer (WPN-20), Proton Cannon (WPN-22) and Shield (WPN-23) are described by the game; projectile flight kinds — WPN-21. The behaviour of Shield Drain, Bio Snare, Shield Raider, Turbo Enforcer, Stealth, Global Drain and Control Jammer is closed by **tests on the modified game (TC) and observation**, damage and numeric parameters — **from the game data** (`WEAPONSTATS.INI`, FMT-5). Remaining: the flight time of rockets, mines and Missile, the speed of the Quake wave and damage by distance, whether the Quake wave passes jump ramps, the numbers for Power Swarm drones, the exact charging of Plasma Bolt, Flamer's backward shot, Proton Cannon's range and damage by stability, the effect of its hits on speed and line of movement (no confirmation in a recording; pace and shield damage — WPN-22), the duration of Shield; **Penetrator (WPN-18) — ram damage**; Bio Snare: attraction; Gravity Bomb against a target with a protective item; which weapon gives an effect that is passed on by touch and removed by the pit lane (PHY-24) | WPN-6, WPN-10…WPN-23, PHY-24, FMT-5 | in-game tests + game data |

## Formats
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-32 | Unknown `.TRK` fields | FMT-3 | analysis |
| OQ-33 | The arrangement of pilots and the packed team in the event (the fields of upgrade level, pit lane and team composition — closed: FMT-8) | FMT-8 | analysis |
| OQ-34 | The weapon weights type; the bonus/function fields; "time in game", "rating", the rest of the main save file | FMT-10, FMT-11 | analysis |
| OQ-35 | The formats `.TRF`, `.CLT`, `.HUD`, `.IPS/.IPF`, `.INA` — needed only for own data converters (ship models and `.GEO` — closed: FMT-17…FMT-21) | FMT-16 | analysis |
| OQ-38 | ~~Where the track texture pixels are stored~~ — **closed**: FMT-20 | FMT-20 | — |
| OQ-39 | ~~Animation of the scoreboard, lava, pads~~ — **closed**: FMT-20, FLOW-6 (lava is static; pads shimmer and go out without animation; the scoreboard — 5 screens) | FMT-20, FLOW-6 | — |
| OQ-40 | The remaining node and mesh fields; track cell records; when the game switches the simplified ship models (the meaning of the `.GEO` points — closed, FMT-21) | FMT-17…FMT-21 | file analysis + observation |
| OQ-41 | ~~Visible damage: choice of groups, threshold, repair, debris~~ — **closed**: SHIP-15, SHIP-7 (debris — particles at the moment of breakage, by code; a project decision) | FMT-22, SHIP-15 | — |
| OQ-42 | ~~Canopy animation: once or in a loop~~ — **closed**: SHIP-15 (the animation cannot be made out before the ship falls apart; the port — the implementer's decision) | FMT-23 | — |
| OQ-43 | ~~When the weapon node is visible~~ — **closed**: SHIP-15 | FMT-22 | — |
| OQ-44 | ~~Ship version choice~~ — **closed**: SHIP-14 (`SECRET` — the Zone ship); separately confirmed by observation: the ship in the menu does not differ from the ship on the track (SHIP-14) | FMT-17, SHIP-5 | — |

## Screen and effects
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-47 | ~~The source of the shake on Cubiss Float 2R~~ — **closed**: falling ice blocks, GEN-8 | GEN-8 | — |
| OQ-48 | ~~Shake: are the numbers at the sources strength or duration~~ — **closed**: GEN-8 | GEN-8 | — |
| OQ-50 | ~~Clarify the recordings: the repair queue; 72 touches at shield 71~~ — **closed**: SHIP-7 (the less damaged node is repaired earlier), SHIP-6 (destruction at shield < 0.9 after a hit; no fractional part on screen), SHIP-15 (20 touches took off less than 1) | SHIP-6, SHIP-7, SHIP-15 | — |
| OQ-49 | ~~Frame rate drop on the medal caption~~ — **withdrawn**: does not relate to game behaviour (project decision, 2026-10-21) | — | — |

## Game versions
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-46 | Differences of the American version (NTSC-U) from PAL — **mostly worked out, see GEN-7**. Remaining: suspension behaviour (acceleration is measured — GEN-7 [✓]); the meaning of the physics component changed by a factor of 6; what exactly is changed in three tracks; weapon changes that have not been worked out | GEN-7, all rules with durations | observation (PAL + US) + analysis |

## Bit-exact compatibility
| ID | question | affects | how to close |
|---|---|---|---|
| OQ-37 | PS2 floating-point arithmetic differs from IEEE (no denormals/infinities, different rounding). For playing "by feel" ordinary IEEE is enough; for byte-exact comparison with recordings this arithmetic must be emulated | all physics | analysis |


Numbers OQ-51…OQ-59 are not used (reserved).
