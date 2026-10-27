# Specification releases

Each release is a `spec-rN` tag and an archive (`../process/README.md`, section 4). This file lists what changed in behaviour and rules.
The note "not manually reviewed" means that the change passed the automatic check but has not yet passed manual review.

## r1 — draft, 2026-10-18 (not yet released)

Release (set the `spec-r1` tag) only after manual review by a second person, not the author of the text.
The automatic check (`docs/process/check_spec.py`) has passed.

### 2026-10-26 (not manually reviewed)
- WPN-22 extended from a recording of PAL races (weapon granted on a modified game, hits identified by the drop in the opponent's shield): about 25 shots per second, the charge is used up in under a second, damage to the opponent's shield about 0.2 % per hit, hits up to ~400 units of distance, minor stability damage from some hits; the effect of hits on opponents' speed and line is not confirmed (small sample). OQ-31 narrowed.

### 2026-10-25
- SHIP-14: the ship model in the menu does not differ from the model on the track (player observation); OQ-44 finally closed.
- RACE-19 (Zone) rewritten from a player observation: there is no shrinking zone, throttle is always pressed, ships are destroyed by wall touches, speed grows with level, boosters work, there are no weapons and no pit lane. RACE-20 split into Eliminator and Endurance with the note "no observations". OQ-25 kept only for the Zone, Eliminator and Endurance scoring.
- For the remaining weapons (Shield Drain, Bio Snare, Shield Raider, Turbo Enforcer, Stealth, Global Drain, Control Jammer) there are no observations: behaviour is to be closed by tests on a modified game and by observation, damage and numeric parameters are taken from the game data (WPN-16, OQ-31).
- WPN-19 created and withdrawn on the same day (the description referred to a different weapon; the ID is not reused).
- New rules WPN-18 (Penetrator), WPN-20 (Flamer), WPN-21 (three kinds of projectile flight: along the track geometry, on a free trajectory, with homing), WPN-22 (Proton Cannon: 25 charges on pickup, a fast burst forward along the track geometry, no homing, does not fire backward, small damage but strongly upsets stability), WPN-23 (Shield: an impenetrable shield for a time, absorbs any damage and changes colour from blue to red when it absorbs). WPN-6, WPN-8, WPN-16, WPN-17, OQ-31 updated.
- WPN-11 (Plasma Bolt) extended with observations: one charge, charging 1–2 s, no homing and no splash. The earlier erroneous description of Proton Cannon, which actually referred to Plasma Bolt, corrected.
- Quake follows the track geometry, including the splitting and merging of sections (WPN-13); Rocket, Missile, Super Missiles and Plasma Bolt also follow the geometry (WPN-6, WPN-11, WPN-21); passage of ramps by the Quake wave is open in OQ-31.
- Grenades (3 in a fan, forward or backward with "look back") fly on a free trajectory and can leave the track; a grenade that has left explodes or disappears (WPN-6). Mines stay in place and do not depend on "look back". A ship that has left the edge of the map returns to the track without damage (PHY-22).

### 2026-10-24 (from player observations)
- WPN-6 rewritten to match the game: rockets (3, straight), Missile with homing, Super Missiles with lock on up to three targets, mines at the ship's position, Quake with mesh deformation, Power Swarm with a swarm of drones; WPN-7 — "look back" confirmed for these kinds; WPN-13 extended with the look of the wave; WPN-3 — triggering by area, not by touching with an edge.
- Super Weapon is granted from a common pool with a team-specific type on pickup; in Time Trial the burst is granted to the player at every finish line crossing.
- Weapon pads: granted only by an active pad to a suitable ship, instant extinguishing, different pad cooldown for EU/PAL and US, no recovery during pause, an armed ship does not extinguish the pad. Pickup — over an active pad when the ship has no weapon and shield is above zero. OQ-28 closed for the main conditions.
- Hull damage does not affect weapon use, power, speed, range or time before the next shot; after the nose is destroyed a weapon can be picked up and used at once. Damage locally destroys hull elements and spreads to neighbours; identical ships can be destroyed in a different sequence. Strength shares of the four hull zones refined; `mdamage_decrease%` does not take part in the damage calculation (OQ-5 narrowed).
- WPN-18: Penetrator (Piranha's super weapon) — acceleration and an energy ram on the nose, ram damage not studied.
- RACE-15: ghost — a semi-transparent hazy copy of the player's ship with a trail, with no other effects, a deterministic recording; absent at the start of a session and not carried between sessions (only the time is written to the card). OQ-21 closed.
- Refined AI behaviour after leaving the track, braking before corners, and qualitative physics observations on surfaces, climbs, in flight, on landings and collisions.
- AI-3: the AI uses the `.SPL` layout lines (the link to `.TRI` objects is not confirmed, OQ-27). AI-6: smoothness changes on timers following aggression, concentration does not change. WPN-8: the shield is dropped with a button without throwing away the weapon, in Endurance the button uses the Proton Cannon reserve.

### 2026-10-23 (from game data files and tests on a modified game)
- FMT-26: track model cells and the visibility mask described.
- FMT-27: track sky and clouds (`SKY_*/SKY.MEM` — an ordinary dome model, `CLOUDS.CFI` — cloud layers, partially parsed). They exist only for three tracks (FLORION_HEIGHT, CUBISS_FLOAT, VOHL_SQUARE).
- FMT-25: Florion 1F `.TRI` has 266 objects, not 103 names; the "object → model file" mapping is not stored in the data, it is derived from type and name.
- FMT-18/FMT-19: for models of objects placed through `.TRI`, the texture list items are references to a separately loaded image; all 965 data files are readable.
- FMT-20: `TEXTURES/` folders exist only for three tracks (467 files); track and sky models refer to images by number, not by texture entry, a "number → file" table was not found. Sky: the domes number their faces, one image file per face.
- The full track scene is assembled for 45/45 drivable levels; `.TRI` objects are matched to models 266/266.
- OQ-3: five ship parameters from SHIPS.INI parsed by behaviour (the drag multiplier above the speed limit; the frame counter after a collision; an unused mass field; the threshold and strength of the nose reaction when touching a surface — this is a landing/surface impact, not a nod when braking). Open: angle units, check in the game.

### 2026-10-22
- PHY-11: weak boosters k = 0.008 (also for the AI). PHY-19: triggers are `.TRI` objects, checked against the object's box on its own section. OQ-8 closed.
- WPN-3: a ship that has finished or been eliminated does not pick up weapons; WPN-4: Time Trial set, instance limits; WPN-5: selection order; WPN-9: the force of the fire button press sets damage, speed, push. OQ-29, OQ-30 closed.
- Correction to PHY-18: suspension damping is set by surface subtype, 7 coefficients (the former 16 values were a table-reading error). OQ-10 closed.
- FMT-24: the AI drives along `.SPL` lines; data conventions (the "sideways" vector, piece joints) whose violation breaks AI driving.

### 2026-10-21
- Data: FMT-2 (full contents of the track folder), FMT-3 (`VISI` — the model cell mask; after the polygon references in `TOTS` come light references, then links — verified by reading and writing all 45 `.TRK` files byte for byte; the section field after the bit0 flag is a respawn point, not a pit lane), FMT-4, FMT-24 (AI lines and the starting grid; Time Trial start position), FMT-25 (`.TRI`), FMT-26 (track model cells); OQ-27 — format closed. FMT-3 also on the role of vertex normals at walls.
- Physics: PHY-25 (wall impact: contact points, push-off along the smoothed wall normal); PHY-7 (airbrakes: build-up, limits, "stop" below 100 km/h, jerks with two brakes and throttle); PHY-8 (thrust curve); PHY-9 (longitudinal drag and lateral friction; thrust verified against recordings); PHY-20 (ramps and free flight); PHY-22 (rule for choosing the respawn point, return to the track after a fall with a fade-out, no visible droid). OQ-2, OQ-6 narrowed, OQ-9 closed.
- Ship: SHIP-5 (upgrade screen: prices, displayed values, "% upgrade" — the upgrade share p; rolling back an upgrade returns the price in full); SHIP-6 (destruction threshold 0.9 and shield display); SHIP-7 (order in which components "heal", when parts look intact during repair); SHIP-9 (picture of destruction: break-up, pilot capsule, "RESCUE" droid); SHIP-14 ("ship upgraded" screen); SHIP-15 (not all touches count as 1, debris as particles, view change on the 5th touch, the canopy does not move at the start). OQ-50 closed; OQ-41, OQ-42 closed. Recalculation: 51 · 1 + 20 touches averaging 0.94 = 69.84, remainder 1.16, the 72nd touch gives a shield below 0.9, that is 0; total 71. With "00" on screen the ship may be alive, but not with a shield of exactly 0.
- Race: RACE-24 (credits for a league race, examples agree: 116 350; 36 650; 19 000; 15 750; 15 993); RACE-7, RACE-22 (the "catch-up" menu item: off / low / high); RACE-15 (what the ghost looks like); RACE-9 — the observation about frame-rate drops removed as not relating to game behaviour.
- FLOW-6: the board has exactly 5 screens, start-straight board screens, the pre-start intro of Time Trial (hatch, lift, fly-around). FMT-20: lava is static, pads have no pickup animation, appearance of pads after pickup and of boosters. OQ-39 closed.
- GEN-7: PAL/US file composition — the board is the same, the flying machines of Katmoda 12 are PAL-only; the catapult on Alca Vexus 2R in US is recognised as a US-version bug (not reproduced in the port), did not recur in PAL in 5 repeats.
- OQ-49 withdrawn.
- SHIP-8: the "destroyed" state is tied to the shield threshold 0.9 from SHIP-6 (instead of "shield = 0").
- OQ-13 narrowed to the "mass" number on the ship screen.

### 2026-10-20
- GEN-8: two kinds of shake sources — constant strength (Quake, Seismic, destruction) and a decaying impact of `N` frames with strength equal to the remaining frames (ship 10, ice block 20, track hit 5 × damage, object 30); the falling ice blocks on Cubiss Float are the strongest shake. OQ-47, OQ-48 closed.
- GEN-9: the demo version of the game.
- PHY-13: a wall touch usually takes 1 shield, series of touches; SHIP-7: accumulation of wall damage and its effect on acceleration, speed, sliding; repair time 1.44 s PAL / 1.20 s US (US ×1.2 confirmed; the earlier "1.9 s" was a counting error); the pit lane restores component parameters; SHIP-15: damaged-look threshold, 72 touches (1/71 · 12 = 0.17 per touch; 4 touches — 0.68, 5 — 0.85, 6 — 1).
- FLOW-3: the pit lane is enabled in Time Trial too, disabled in Zone. RACE-9: medal caption in Time Trial.
- GEN-7: league race results on both versions (sliding, weapon pickup rate, softer walls); the unmodified game was used in the recordings for version comparison.
- Evidence labels brought to the accepted ones ([✓] / [code]); line endings in files brought to LF, `.gitattributes` added.

### 2026-10-19
- GEN-7: differences of the American version (frame, clock, physics substeps, AI, data), acceleration US/PAL ×1.2 confirmed by measurement [✓]. Recalculation: 16/16/18 ms → 16.67 ms; 120 · 0.0083 = 0.996; wrong way 140/60 = 2.33 s, 20/60 = 0.33 s. New for PAL: weapon pad lock of 0.5 s after pickup (WPN-3), Quake ban for bots of 5 s (AI-2).
- Observations on the US version are valid only for facts that do not depend on frame rate (rule in the README); the moment of removal "at the 85th second" removed from RACE-21. OQ-46 narrowed.
- FLOW-12 (places of those who did not finish), RACE-21 (elimination of those lapped), RACE-6 (wrong way in Zone), PHY-21 (lava counter), RACE-15. OQ-14, OQ-16, OQ-19, OQ-21, OQ-45 closed.
- RACE-22 (two-player race settings), RACE-23 (resurrection), FMT-14 (menu state machine), FMT-12 (string lookup), TC-34…TC-36. RACE-22 and RACE-23 verified on a modified game: they confirm the formulas, but not the behaviour of the original mode as a whole.
- OQ-33 narrowed (upgrade levels and the pit lane in the event parsed, FMT-8). OQ-40 created together with OQ-38 and OQ-39 (model formats). AI-7 brought in line with SHIP-14 and SHIP-16; test cases TC-31 and TC-35 recalculated.
- SHIP-16 (upgrade levels of opponents; verified on 570 AI ships in 57 race recordings), FMT-8, TC-33; OQ-12 closed.
- RACE-5 (order on equal progress), RACE-7 (rubber band: k, reference, off by default), FLOW-6 (AI start bursts), PHY-11, RACE-21; TC-30…TC-32. OQ-11, OQ-18, OQ-20 closed.
- PHY-24 (pit lane by 4 player passes and 12 AI passes, [code] → [✓]), AI-8 (when the AI enters the pit), FLOW-3, TC-27…TC-29; OQ-17 closed.
- SHIP-14 (upgrade share → ship version and speed class 1–4), SHIP-15 (visible damage, weapon node, start of the canopy animation), WPN-17 (damage to a human ×0.5, active shield); FMT-8, FMT-10, FMT-20, FMT-21 (engine flares) refined; TC-25, TC-26. OQ-38, OQ-43, OQ-44 closed.
- Model formats from game data files: FMT-13, FMT-17 (node tree, ship versions), FMT-18 (mesh and vertex packets), FMT-19 (embedded ship textures), FMT-20 (track peculiarities), FMT-21 (`SFX_TAGGED.GEO`), FMT-22 (part groups: intact and damaged version, debris), FMT-23 (keyframes; canopy animation); TC-23, TC-24. Verified by reading: 100 % of triangles of all 78 models.

### 2026-10-18
- The specification was separated from the research notes; rule IDs introduced (GEN, FLOW, SHIP, PHY, RACE, AI, WPN, FMT, OQ, TC).
- Added the glossary (00), test cases (09), the question log, the specification boundaries (README).
- Open questions numbered (OQ-1…OQ-37), those found during the restructuring added: OQ-11, OQ-15, OQ-16, OQ-23, OQ-29 and others.
- Remnants of the original's internal names removed.
