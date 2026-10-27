# 06. Weapons

## WPN-1. Weapon types and their numbers [✓]
The type number is fixed: it is used as the bit number in the unlocked-weapons mask and as the weight index in the profile (FMT-10)
and in the event weapon mask (FMT-8).

| # | weapon | # | weapon | # | weapon |
|---|---|---|---|---|---|
| 0 | Turbo | 9 | Power Swarm | 18 | AG Stinger |
| 1 | Autopilot | 10 | Shield Drain | 19 | Proton Cannon (25 shots) |
| 2 | Rocket | 11 | Nitro Rocket | 20 | Shield Raider |
| 3 | Mines (5 pieces) | 12 | Penetrator | 21 | Hunter Missile |
| 4 | Missile | 13 | Flamer (99 units of fuel) | 22 | Turbo Enforcer |
| 5 | Quake | 14 | Plasma Bolt | 23 | Stealth |
| 6 | Gravity Bomb | 15 | Seismic Field | 24 | Global Drain |
| 7 | Super Missiles | 16 | Grenades | 25 | Shield |
| 8 | Orbital Laser | 17 | Bio Snare | 26 | Control Jammer |

The implementation does not require any other weapon types. [✓]

## WPN-2. Team super weapons [code]
Feisar — Super Missiles, Van-Uber — Seismic Field, G-Tech — Bio Snare, Auricom — Orbital Laser,
EG-R — Power Swarm, Tigron — Nitro Rocket, Xios — Shield Drain, Piranha — Penetrator.

## WPN-3. Pickup conditions on a weapon pad [code; ✓ player observation]
A weapon is given to a ship that has driven over a weapon pad (PHY-19) if pads are enabled in this race
(FLOW-3), the ship has no weapon, its shield is > 0, and the ship has not finished or been eliminated from the race (for a finished or
eliminated ship the current weapon is lost and no new one is given).
- What triggers it is **driving over the pad** (the area of effect), not touching its edge; after giving out a weapon the pad goes dark immediately
  [✓ player observation].
- After a weapon is given out, the pad gives **no weapon to anyone for 0.5 s in the EU version (50 substeps) and 1 s in the US version** (the pad cooldown); the countdown runs
  in substeps and stands still during pause [code; GEN-7].
- A ship that already has a weapon does not turn the pad off and does not receive a weapon [✓ player observation].
- In Time Trial pads do not work; the Turbo burst triggers on every crossing of the finish line
  [✓ player observation].

## WPN-4. Candidates [code]
1. Candidates are the weapons unlocked in the player's profile (FMT-10). The team super weapons of all teams are removed from them; if the player
   has unlocked the super weapon of **their own** team, then every ship gets the super weapon of **that ship's team** added.
2. Single-player modes: Hunter Missile, Turbo Enforcer, Stealth, Global Drain, Control Jammer are removed.
   Two-player modes: these 5 types are, on the contrary, added for humans; bots never get Global Drain;
   after that the multiplayer settings filter applies. Shield is not removed.
3. The event weapon mask (FMT-8), if set; **in Time Trial Autopilot, Mines, Bio Snare and
   AG Stinger are additionally removed** [code]; types whose limit of simultaneously existing instances is exhausted are removed [code]:

   | limit | types |
   |---|---|
   | 1 | Quake |
   | 2 | Super Missiles, Orbital Laser, Power Swarm, Shield Drain, Nitro Rocket, Penetrator, Flamer, Seismic Field, Bio Snare, Stealth, Global Drain |
   | 5 | Gravity Bomb, Shield |
   | 10 | Plasma Bolt, Grenades, AG Stinger, Hunter Missile, Turbo Enforcer, Control Jammer |
   | 50 | Turbo, Autopilot, Rocket, Mines, Missile |
   | 1000 | Proton Cannon (effectively no limit) |
   | 0 | Shield Raider — never drops as an item |

## WPN-5. Weighted selection [code]
A random choice among the candidates with the weights from the profile (27 weights, FMT-10), generator GEN-4.
If the same weapon comes up that this ship received last time, and there are at least two candidates — re-roll.
The selection [code]: the sum of the weights of the remaining candidates × a random number from [0, 1) is the threshold; the types are iterated in order of
number (0…26), the weights are accumulated, and the first type at which the sum reaches the threshold is taken.

## WPN-6. Firing: what each type does [code; ✓ player observation]
- Turbo, Autopilot — take effect immediately (WPN-16).
- **Rockets** (3 pieces) — fired one after another along the ship's longitudinal axis, without homing, but following the track
  geometry (WPN-21). Forward or backward — depending on "look back" (WPN-7) [✓ player observation].
- **Missile** (1 piece) — homing: locks onto a target and follows it; the lock range is limited; the
  projectile follows the track geometry (WPN-21). Forward or backward — depending on "look back" [✓ player observation].
  Flight time — OQ-31.
- **Super Missiles** (Feisar, 3 pieces) — like Missile, including flight along the track geometry (WPN-21), but they lock
  up to 3 targets: with one locked target all three missiles go for it, with three — one each to its own target [✓ player observation, PAL].
- **Mines** (5 pieces) — laid at the ship's position while the fire button is held; they do not depend on "look back";
  they detonate the same way on the player and on bots [✓ player observation]. Mine lifetime — OQ-31.
- **Quake** — a wave travelling along the track geometry (height changes, twisting, splitting and merging of sections),
  forward or backward depending on "look back"; along the way it temporarily deforms the track mesh, and sparks fly at the edges [✓ player observation, PAL]. Passing over jumps where there is no track — OQ-31.
- **Grenades** (3 pieces) — thrown simultaneously in a small fan; forward or backward — depending on "look back"
  [✓ player observation]. They fly on a free trajectory (WPN-21), not along the track geometry, and can fly out
  beyond its bounds: a grenade that has flown out explodes or disappears [✓ player observation].
- **Power Swarm** — team super weapon (WPN-2): releases a swarm of 1–5 drones that fly to the opponent's ship
  and gradually reduce its shield [✓ player observation].
- **Proton Cannon** (25 charges) — a rapid-fire "machine gun": a salvo forward, along the track geometry, without
  homing; it does not fire backward (WPN-22) [✓ player observation].
- Mines and Proton Cannon use up a stock; the other weapons disappear after firing.

## WPN-7. Look back [code; ✓ player observation]
While "look back" is held, projectiles fly backward. This has been verified for rockets, Super Missiles and Quake [✓ player observation, PAL]. Mines do not depend on look back: they stay in place (WPN-6).

## WPN-8. Drop / absorb [code; ✓ player observation]
An ordinary weapon is thrown away when the button is pressed, and the ship is left without a weapon. The only special item is **Shield**: pressing
ends its effect without discarding the weapon; the shield absorbs any incoming damage and changes colour while doing so
(WPN-23).
In Endurance mode this button, instead of dropping, fires Proton Cannon
from the stock, if the stock is not empty.

## WPN-9. Damage [✓ for Gravity Bomb; dependence on press strength — code, not verified in the game]
`damage = value_from_WEAPONSTATS (between Dam_<weapon>_Max and _Min) × weapon_standard of the firing ship` (SHIP-3, SHIP-5).
**The position between Max and Min is set by the pressure of the fire button** at the moment of firing (gamepad buttons are
pressure-sensitive; 0…255 → p = 0…1): `value = Min + (Max − Min) × (1 − p)` — **a light press gives more, a full press gives less**
[code]. Projectile speed (`Spd_*`) and knockback (`Force_*`) are computed the same way, but without the weapon_standard multiplier.
For Proton Cannon the pressure is stored separately (a special case). With a digital button (pressure always full) the result is always
Min — this must be taken into account in observations.
Default values from the file: Rocket 6/2, Mines 3, Missile 5/2, Quake 13, Gravity Bomb 14, Super Missiles 20/15,
Orbital Laser 30, Penetrator 25/15, Plasma Bolt 100, Seismic Field 30, Grenades 5/3, AG Stinger 7, Hunter Missile 15
(the full list is in `WEAPONSTATS.INI`, FMT-5).

## WPN-10. Hit effect [✓ frame-by-frame observations: 241 hits on AI, 10 on the player]
For Rocket, Mines, Missile, Quake, Super Missiles, Orbital Laser, Penetrator, Seismic Field, Grenades,
Hunter Missile, Global Drain:
- **AI**: is marked **stricken** for exactly **3.0 s**; this does not affect speed.
- **Human**: a timer of 100 frames; while more than 25 frames remain until the end, the maximum-speed multiplier decreases
  by 0.01 per frame, then grows by 0.04 per frame; limits [0.1, 1]. In practice: a dip to **0.24** and back,
  **1.9 s** in total (TC-8). The multiplier enters into PHY-4.
- Penetrator has an additional effect: see WPN-18.
Plasma Bolt, Gravity Bomb, AG Stinger and some others have their own effects (below).

## WPN-11. Plasma Bolt [✓ recording; ✓ player observation]
The most powerful weapon in the game: a damage of 100 exceeds the shield of any ship, and a hit **destroys with one shot**.
- On pickup — **only one charge** [✓ player observation].
- Before firing there is a **charge-up** (on the order of 1–2 s), then a beam of plasma flies out [✓ player observation].
- The beam flies along the ship's longitudinal axis and **follows the track geometry**, without homing; no splash
  [✓ player observation].
- The projectile flies for ~2 s (in the recording: shot at 16.06 s, hit at 18.02 s, shield 77 → 0 in one frame).
- Not established: the exact charge-up duration, the beam range, whether it fires backward with "look back" — OQ-31.

## WPN-12. Gravity Bomb [✓]
After detonation a sphere expands from the point of the blast. The timer c runs from 50 to 0 (in frames); every **4th** frame
the ships are checked:
- a ship is hit if `distance² < (50 − c)·2000` (the radius grows up to ≈ 316);
- the strength is `k = c / 50` — the later the wave reaches the ship, the weaker it is;
- **at most one** ship is hit per check, and each ship only once;
- ships eliminated from the race are not hit [code];
- damage = `14 × weapon_standard_of_shooter × k`, knockback × k, plus the AG Stinger effect (WPN-14) lasting `125·k` frames
  (integer part).
Verification — TC-9. If the target has a protective item active, the effect is different (OQ-31). [?]

## WPN-13. Quake [✓ partly]
The wave travels along the track geometry (along the splines): it follows height changes and twisting, passes through the splitting and
merging of sections; it hits several ships. In the recording: −14.3 to one and 3.3 + 3.05 to another; both receive the
hit effect (WPN-10). Appearance: the wave runs along the track forward or backward (depending on "look back"), temporarily deforming the track
mesh; sparks fly at the edges [✓ player observation]. Passing over jumps where there is no track is not established
(OQ-31).

## WPN-14. AG Stinger [✓ 12 hits, full cycle 2.0 s]
A hit remembers the current live `maxspeed` and `rollmaxangle` and starts an effect of 100 frames in three phases:
- **compression, frames 1–20**: `rollmaxangle` is linearly compressed toward 100 — the fraction of the difference between the original value and 100
  decreases by 0.05 per frame (from 1 on the first frame to 0.05 on the twentieth): `rollmaxangle = 100 + (original − 100)·(1 − 0.05·k)`, k = 0…19 — the frame number within the phase, counting from zero;
- **hold, frames 21–80 (60 frames)**: every frame the maximum speed (`maxspeed`) is multiplied by 0.5 (the ship stalls); the height correction (PHY-5)
  decreases by 0.3 per frame down to −2.5 (the ship sags); the ship sways to a random side, and the side
  changes every 40–79 frames (GEN-4);
- **recovery, frames 81–100 (20 frames)**: the fraction of the `rollmaxangle` difference grows by 0.05 per frame (from 0 on the first frame to 0.95 on the twentieth):
  `rollmaxangle = 100 + (original − 100)·0.05·k`, k = 0…19 — the frame number within the phase, counting from zero; the height correction is multiplied by 0.8 per frame;
- after the last frame the original `rollmaxangle` and `maxspeed` are restored, and the height correction = 0.
In addition, one drag component is multiplied by `(1 − t/100)·10` (PHY-9). [code]

## WPN-18. Penetrator [✓ player observation]
A special weapon of team Piranha (WPN-2). When used:
- it gives the ship an **acceleration**;
- an **energy ram** appears on the ship's nose — a visible growth on the front part.
The effect of the ram on opponents' ships and its damage are **not studied** (OQ-31); the hit of Penetrator itself is part of the
general hit effect (WPN-10).

## WPN-19. Removed
The ID is not reused.

## WPN-20. Flamer [✓ player observation]
A flamethrower: a short-range weapon with low range and low damage.
- Emits a jet of flame forward; backward with "look back" — not verified (OQ-31).
- The jet flies **on a free trajectory** (see WPN-21): neither along the track geometry nor toward a target; therefore in
  corners it does not curve with the track, and it ignores height changes and twisting of the track altogether.
- A hit puts a **visible "on fire" effect** on the ship, but the effect itself **does not deal damage over time**:
  the damage comes only from the jet's hits.
- It uses up a stock (in the list — 99 units of fuel); when the stock runs out, the weapon disappears (WPN-6).
- Not established: firing backward, the exact range, the fuel consumption per shot — OQ-31.

## WPN-21. Projectile flight types [✓ player observation]
Projectiles differ in whether they take the track geometry into account (height changes, twisting, loops,
splitting and merging of sections):
- **along the track geometry** — the projectile follows the track and repeats its shape, including the splitting and merging of sections;
  without homing it will not make a corner, but it will not get lost on a loop or a descent: Quake (WPN-13); Rocket, Missile,
  Super Missiles (WPN-6); Plasma Bolt (WPN-11); Proton Cannon (WPN-22);
- **on a free trajectory** — the projectile takes into account neither the track geometry nor targets: it flies straight along the ship's longitudinal axis
  or along its own trajectory, so it leaves the track at height changes and can fly beyond its bounds:
  Grenades, Flamer (WPN-6, WPN-20);
- **homing** — the projectile goes to the chosen target: Missile, Super Missiles (WPN-6).
Homing and following the geometry do not exclude each other.
Following the geometry does not mean homing: Proton Cannon follows the track, but does not home in on a target (WPN-22).
Not established: whether the Quake wave passes over jumps where there is no track (OQ-31).
The flight type of a particular weapon is given in the "what is described" column of the WPN-16 table.

## WPN-22. Proton Cannon [✓ player observation, PAL; numbers — ✓ modified game, PAL]
A rapid-fire weapon of the game, the game's own "machine gun".
- **On pickup, several charges — 25**; it fires until the stock runs out, then the weapon disappears (WPN-6).
- **Fires fast**: shots come as a salvo, not one per press. With the button held — **about 25 shots
  per second** (typically an interval of 0.04 s), so a charge of 25 shots is used up in less than a second
  [✓ modified game, PAL; the weapon was given forcibly, 25 matches the stock at pickup according to the recording].
- The projectiles fly **along the track geometry** (WPN-21), without homing.
- **It does not fire backward** [✓ player observation].
- Hits **strongly upset the stability** of the ship (hit effect WPN-10) — the player's description, not confirmed by the
  race recording.

Measured in a race recording (Arcade, 16 ships, the weapon was given forcibly; hits determined by the drop of the opponent's shield,
projectiles are not visible in the recording; sample — 89 hits in about a quarter of the shots, when the target was ahead,
concentrated on a few ships) [✓ modified game, PAL, estimate by heuristic]:
- **Damage to the shield**: one hit on an opponent's ship removes a small fraction of the shield — on the order of 0.2 % of its stock (within
  0.05–0.5 %); it differs between ships, and decreases only weakly with distance.
- **Hit range**: mostly up to ~100 game distance units, up to ~400 in the recording (for comparison: a track lap is
  about 14 900 such units) [?: the scale is not defined in the spec].
- Some hits add a small amount of damage related to the stability of the ship (on the order of 0.3–1.3 % of the scale per
  hit, not every hit) [?; modified game, PAL].
- **The effect of hits on the speed and line of opponents is not confirmed**: in the recording (bots, 36 series of hits) the
  change in speed over the second after a series lay within the spread of the control moments, and the lateral shift was slightly
  larger than the control. This does not prove the absence of an effect: the sample is small and concentrated on a few bots, the effect on
  the player's ship and the visual effect were not studied [?; modified game, PAL].
- Not established: the exact projectile range, the stability damage as a number, the effect on speed and line — OQ-31.

## WPN-23. Shield [✓ player observation]
A special protective item (WPN-8):
- the ship is surrounded by an **impenetrable shield** that absorbs **any incoming damage** — from any weapon and explosions;
- it works for a **certain time**, then disappears;
- when absorbing damage the shield **visually changes colour from blue to red**: the more damage absorbed, the stronger the
  colouring [✓ player observation];
- the shield is a special item: pressing it ends its effect rather than discarding it (WPN-8);
- damage is absorbed but not accumulated for a counter-attack: the attacker gets nothing (WPN-17).
Not established: the duration of the effect, how much damage it withstands and how fast it changes colour, whether it works against
the Penetrator ram and in what order it is consumed against Gravity Bomb (OQ-31).

## WPN-15. WEAPONSTATS.INI [✓ format]
133 parameters: `Dam_*` (damage), `Spd_*` (projectile speed), `Force_*` (knockback), `LockDist_*` (lock range),
Proton Cannon and mine delays; nearly all in `_Max` / `_Min` pairs. Keys and values are in the file itself (FMT-5).

## WPN-16. What is known about each type [✓ player observation, where indicated]
| weapon | what is described | what is missing (OQ-31) |
|---|---|---|
| Turbo | a burst | burst strength |
| Autopilot | AI drives | duration |
| Rocket | 3 pieces in a row, forward/backward, without homing, follow the track geometry (WPN-6, WPN-21) | range and flight time |
| Missile | homing with limited lock range, follows the track geometry (WPN-6, WPN-21) | flight time, conditions for losing the lock |
| Super Missiles | up to 3 targets; with one target all three go for it; follow the track geometry (WPN-6, WPN-21) | flight time, order of target selection |
| Mines | 5 pieces, laid at the ship's position, do not depend on "look back", detonation is the same on the player and bots (WPN-6) | lifetime, detonation radius |
| Quake | the wave follows the track geometry, forward/backward, deforms the mesh, sparks at the edges (WPN-13) | passing over jumps, wave speed, damage by distance |
| Power Swarm | a swarm of 1–5 drones to the opponent, gradually reduces the shield (WPN-6) | rate of reduction, drone lifetime, what happens with several targets |
| Gravity Bomb, AG Stinger | fully | — |
| Plasma Bolt | one charge on pickup; charge-up 1–2 s; a beam without homing and without splash, follows the track geometry, lethal on hit (WPN-11, WPN-21) | exact charge-up, range, firing backward |
| Penetrator | acceleration and a ram on the nose (WPN-18) | ram damage, effect on opponents |
| Proton Cannon | 25 charges, rapid salvo, forward, along the track geometry, without homing; low damage, strongly upsets stability (WPN-22) | rate, range, damage per shot |
| Orbital Laser, Seismic Field | damage, effect | hit geometry |
| Grenades | 3 pieces in a fan, forward/backward by "look back"; fly on a free trajectory, can fly outside the track and explode or disappear there (WPN-6, WPN-21) | fan geometry, explosion radius |
| Flamer | flamethrower: short range, low damage, free trajectory of the jet, "on fire" effect without damage over time (WPN-20, WPN-21) | range, fuel consumption, firing backward |
| Shield | an impenetrable shield for a certain time: absorbs any incoming damage, changes colour from blue to red when absorbing (WPN-23) | duration, how much damage it withstands |
| Shield Drain, Bio Snare, Shield Raider, Turbo Enforcer, Stealth, Global Drain, Control Jammer | only the name (and the stock) | behaviour — tests on the modified game (TC) and observation in the game, damage — from the game data (WPN-15, FMT-5); no player observation yet |

The remaining types are covered as follows: behaviour — by tests on the modified game (TC) and observation in the game, numeric parameters (damage,
speed, knockback) — from the game data (`WEAPONSTATS.INI`, FMT-5): hits by eye do not give numbers.

## WPN-17. Damage to a human and an active shield [code]
- Damage from a direct weapon hit on a **human's** ship is halved (WPN-9 × 0.5). Explosions and knockbacks
  (for example, Gravity Bomb) are not reduced.
- While the ship has a picked-up shield active (Shield, WPN-23), any incoming damage is absorbed: the ship's shield does not
  decrease, and the shield item itself changes colour from blue to red while absorbing [✓ player observation].
