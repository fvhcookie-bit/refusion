# 00. Glossary

Terms used in the specification. English words are data file keys or on-screen game text.

## Time and simulation
| term | meaning |
|---|---|
| **frame** | one step of game logic, 20 ms of game time (GEN-1) |
| **substep** | half a frame for physics, 0.01 s (PHY-1) |
| **race clock** | game time since the race was set up, without pauses (FLOW-4, FLOW-9) |
| **T** | race start time on the race clock, 4…7 s (FLOW-5) |
| **per-substep impulse** | the "force" in physics formulas: added to velocity without multiplying by time (PHY-10) |

## Track
| term | meaning |
|---|---|
| **track** | a pair of environment + layout; **track code** `env·6 + circuit` (GEN-5) |
| **section / subsection** | stretches of track geometry from the `.TRK` file; a section has entry/exit "gates" (FMT-3) |
| **lap progress** | a number 0…1 for a subsection from the `.LAP` file (FMT-4) |
| **surface** | the type of a track polygon, determined by the material name (PHY-17) |
| **surface subtype** | sound/particles/damping: water, ice, rock, sand, stone, damage (PHY-18) |
| **polygon trigger** | a special polygon: booster, weapon pad, flip, mines (PHY-19) |
| **booster** | a trigger that accelerates the ship (PHY-11) |
| **weapon pad** | a trigger on which the ship receives a weapon (WPN-3) |
| **pit lane** | a stretch with a speed limit and shield recharge (PHY-24) |
| **jump ramp** | the `air1/2/3` surface, launches the ship into the air (PHY-20) |
| **start line** | the `start` surface; crossing it changes the lap counter (RACE-3) |

## Ship
| term | meaning |
|---|---|
| **team** | one of 8 (Feisar … Piranha), number 0–7 (SHIP-1) |
| **pilot lead / second** | the first / second pilot of a team, pilot number within the team 0 / 1 (SHIP-1) |
| **slot** | the ship number in results tables: `team·2 + pilot` (SHIP-2) |
| **ship parameters** | the values of the `SHIPS.INI` section for a slot (SHIP-3) |
| **live parameters** | a copy of the parameters for the duration of a race; changed by upgrades, damage, weapons, Zone (SHIP-4) |
| **upgrade** | level 1–6 of one of 6 groups, replaces a base parameter (SHIP-5) |
| **shield** | the durability reserve; 0 means the ship is destroyed (SHIP-6) |
| **components / component damage** | engine, nose, stabilizers, airbrakes; 0…1 (SHIP-7) |
| **effective maximum speed** | `maxspeed` with all multipliers of this substep applied (PHY-4) |
| **input** | gamepad actions and axes; the AI writes the same fields (SHIP-11, AI-1) |
| **autopilot** | the AI controls the player's ship, the gamepad is ignored (FLOW-10) |
| **throttle before start / stalled** | throttle held down before the start, and the penalty for it (FLOW-6) |
| **burst** | an instant start or turbo acceleration of a given strength (FLOW-6, WPN-6) |

## Race and results
| term | meaning |
|---|---|
| **event** | the description of one race in `GAME.BNI`: type, track, laps, pilots, medal thresholds, weapons (FLOW-2, FMT-8) |
| **progress** | `lap − debt + subsection_fraction`; places are sorted by it (RACE-2) |
| **debt** | the number of backward start-line crossings not yet compensated (RACE-2) |
| **current position** | the place by progress in this frame (RACE-5) |
| **finish table** | the final places: filled in at the moment of finishing or elimination (FLOW-12) |
| **out of the race** | the ship has finished or been eliminated; its result is fixed |
| **destroyed** | the shield has reached 0; after 7.2 s the ship is eliminated (SHIP-9) |
| **eliminated** | out of the race without a place: destroyed, removed from lava, etc. |
| **kill** | destroying an opponent, caused by this ship's weapon (SHIP-10) |
| **stricken** | the state after being hit by a number of weapon kinds (WPN-10) |
| **rescue droid** | returns a ship that has fallen off the track to the track (PHY-22) |
| **rubber band** | a speed limit on leaders to pull up the trailing ships (RACE-7) |
| **perfect lap** | a lap without touching the track geometry (RACE-8) |
| **challenge** | a single-player team task with medals (RACE-13) |
| **medal** | bronze / silver / gold by the event's three thresholds; a higher one includes the lower ones |
| **league** | a series of up to 8 events with points (RACE-10) |
| **completion percentage** | the profile's overall score, 0–100 (RACE-17) |
| **extra marks** | additional profile flags that count towards the percentage; their meaning is not established (OQ) |
| **profile** | the player's saved progress (FMT-10, FMT-11) |
| **super weapon** | a weapon tied to a team (WPN-2) |
| **unlocked weapon** | a weapon unlocked in the profile (FMT-10) |
