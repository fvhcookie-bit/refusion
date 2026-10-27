# 02. Ship

## SHIP-1. Teams and pilots [✓]
8 teams of 2 pilots each (lead and second), 16 ships in total. Team numbers:
0 Feisar, 1 Van-Uber, 2 G-Tech, 3 Auricom, 4 EG-R, 5 Tigron, 6 Xios, 7 Piranha. Pilot number within the team: lead = 0, second = 1.
Pilots in slot order: djohnson, cbeneto, sgrey, nmishima, rsergio, nturner, prouser, fgonzalez,
pcheung, areece, okhumala, skirovoski, nbelmondo, zwollf, mtsarong, jschlaudecker (names of the pilots' INI files, FMT-6).
In the team challenge the player flies as the second pilot of their team. [✓ Feisar]

## SHIP-2. Slot [✓]
The ship's slot in results tables = `team·2 + pilot`. Slots index the `SHIPS.INI` sections, league points,
the finish table, and kill tracking.

## SHIP-3. Parameters (SHIPS.INI)
Sections `[<team> lead]` / `[<team> second]` for the 16 ships, plus `[zone ship]` and `[escape pod]` (FMT-5).

| group | keys | meaning |
|---|---|---|
| mass | `mass`, `fe_mass` | mass (impulse → the velocity change is divided by it, PHY-10); `fe_mass` — for the menus [code] |
| speed | `maxspeed` | maximum speed, "km/h" [✓] |
| thrust | `maxthrust`, `accelforcemultiplier`, `accelbottomforce`, `accelbottomspeed`, `acceltopzone`, `acceltricklezone`, `acceltricklefactor` | thrust curve over speed; exact formula — OQ-2 [code] |
| suspension | `rideheight`, `noserideheightfactor`, `susdamping`, `bobspeed` | hover height, nose tilt, damping (PHY-5, PHY-6) [code] |
| turning | `turnforce`, `turninc`, `turnmaxangle`, `turndamping` | |
| roll / pitch | `rollforce`, `rollmaxangle`, `pitchforce`, `pitchmaxangle` | |
| brakes | `brakeforce`, `brakehalfinc`, `brakefullinc`, `braketurndamping`, `brakepitchangle`, `brakepitchforce`, `airbrakeslide`, `airbraketurnmin`, `airbraketurnmax` | |
| gravity | `gravityhillup`, `gravityhilldown`, `gravityflying` | uphill, downhill, flight |
| turbo | `turbopower`, `turbotime` | |
| other | `frictionfactor` | drag multiplier for movement above the maximum speed (0.70–0.90) [code] |
| other | `collisionTiming` | frame counter after a collision, decreases by 1 per frame; who sets it — OQ-3 [code/guess] |
| other | `ndmass` | does not affect physics (only copied; 100 for all) [code] |
| other | `ndmaxdegrees` | threshold/magnitude of the nose reaction on touching a surface; on a touch it is recomputed every frame from the angle between the hull and the surface normal, the value from the file applies only until the first touch [code/partly guess] |
| other | `ndturnforce` | strength of the pitch impulse when landing on / hitting a surface at an angle (1000 for all teams, zone ship 3000, escape pod 1) [code] |
| shield | `shield_standard` | shield capacity [✓] |
| weapon | `weapon_standard` | **this ship's weapon damage multiplier** [✓] |
| damage penalties | `mdamage_<component>_<parameter>`, `mdamage_decrease%` | damage penalty parameters; the exact purpose of `mdamage_decrease%` is not established (OQ-5) |
| upgrades | `<GROUP>_<key>_UPG1…6`, `cost_<GROUP>_UPG1…6` | SHIP-5 |
| cameras | `cam1…3_distance/elevation/raiseangle/horizontalStiffy/verticalStiffy` | 3 camera views |

## SHIP-4. Live parameters [✓]
For the duration of a race each ship has **its own copy** of the parameters. It is created when the race is set up (FLOW-4), and then
changed by upgrades (SHIP-5), destruction (SHIP-9), lava (PHY-21), AG Stinger (WPN-14), and Zone mode (RACE-19).
Physics reads only the copy. The original `maxspeed` after upgrades is stored separately and does not change during the race.

## SHIP-5. Upgrades [✓]
Six groups with levels 1–6. A level **replaces** the base parameter value in the live copy:

| group | level key | what it replaces |
|---|---|---|
| TOPSPEED | `TOPSPEED_maxspeed_UPGn`, `TOPSPEED_gravityflying_UPGn` | `maxspeed`, `gravityflying` |
| THRUST | `THRUST_accelforcemultiplier_UPGn` | `accelforcemultiplier` |
| BRAKING | `BRAKING_brakeforce_UPGn`, `BRAKING_brakefullinc_UPGn` | `brakeforce`, `brakefullinc` |
| STABILITY | `STABILITY_turninc_UPGn`, `STABILITY_turndamping_UPGn`, `STABILITY_braketurndamping_UPGn` | `turninc`, `turndamping`, `braketurndamping` |
| WEAPON | `WEAPON_weaponpower_UPGn` | `weapon_standard` |
| SHIELD | `SHIELD_shieldpower_UPGn` | `shield_standard` |

A value of 0 in the INI means "no such level". Example — TC-5. AI opponents get upgrades too
(their `weapon_standard` ranges from 1.0 to 2.1, against 1.1 for the player); how their levels are chosen — SHIP-16.
The player's levels are bought with credits on the upgrade screen.

**Upgrade screen** [✓ player observation, PAL: Xios lead, Natasha Belmondo; values checked against `SHIPS.INI`]:
- for each group — the current value, the next level, and the price; the price of level n is `cost_<GROUP>_UPGn`
  (Xios lead: TOPSPEED 227 790, THRUST 179 865, BRAKING 123 975, STABILITY 138 375, WEAPON 217 080, SHIELD 168 458
  for the first level); a purchase needs confirmation "accept upgrade yes / no", and credits decrease by exactly the price;
- what is shown in place of the internal quantities:
  | row | value on screen | example (base → level 1) |
  |---|---|---|
  | top speed, kph | `maxspeed` | 1114 → 1189 |
  | thrust, gfu | `accelforcemultiplier × 1100` | 7865 → 8690 → 9515 |
  | brake force, gfu | `brakeforce / 4` | 6875 → 7625 |
  | lateral stability, % | `turndamping / 2`, fraction truncated to tenths | 34.3 → 35.8 |
  | weapon power, × | `weapon_standard` | 2.1 → 2.5 |
  | shield power, qsu | `shield_standard` | 71 → 75 |
  | mass, kg | 1177 for this ship; `mass` in `SHIPS.INI` is 2500 for all — where the number comes from, OQ-13 | — |
- "N % upgrade" is the upgrade share `p` from SHIP-14 (Xios lead has 33 levels: 1 level — 3 %, 2 — 6 %). The number of divisions in a group's bar equals the number of its levels for this ship (for Xios lead — 5 or 6; for other ships a group
  may have 3 as well, see the example in SHIP-14; ships have 22…36 levels in total),
  the purchased ones are yellow;
- the selected row blinks: its bar flashes yellow as a whole, so in a screenshot the bar may look full.
  The player found the blinking too frequent — whether it is meant that way has not been checked [?];
- purchased levels can be rolled back: when a level is rolled back, its price is returned **in full** [✓ player observation, PAL] — so
  upgrades can be freely moved to another ship, for example in the middle of a league.

## SHIP-6. Shield [✓]
- The initial value = `shield_standard` (after upgrades). The ship is **destroyed** when after a hit the shield becomes
  **less than 0.9** — it is then zeroed (SHIP-9) [code; ✓ recording: shield 1.16 → hit → 0, destroyed]. On screen the shield
  is shown without the fractional part (2.7 → "02"), so at "00" the ship may still be alive (shield 0.9…1.0).
- Touching a wall takes off about 1 unit, a hard hit 2–5. [✓ duel: shield 9, 1 per touch; formula — OQ-6]
- Weapon damage — WPN-9.

## SHIP-7. Component damage [code; ✓ league recordings PAL and US, many hours of the player's in-game observations]
Besides the shield the ship has component damage: engine, nose, stabilizers, airbrakes (each 0…1). According to the player's observations, the element directly at the point of impact is damaged first; once it is fully destroyed, the damage passes to neighbouring elements. Repeated hits on one area can destroy all the elements of that area. Elements of the same ship type may be destroyed in a different order for the player and for bots. [player observation; no exact comparative measurements were made] How damage is split between components — SHIP-15 (by the hull groups near the point of impact).
The damage reduction on impact depends on the distance to the nearest undamaged group: distant groups receive less, and a group that is too far away may receive no damage. [code; consistent with the touch recording]
Over many hours of play no connection was observed between nose damage and weapon use. After the nose is destroyed a weapon can be picked up and used immediately. No effect of damage to other parts of the hull on weapon use, strength, projectile speed, range, or time before the next shot was observed. [✓ player observation, PAL; no exact comparative measurements were made]
The nose may be visually destroyed faster than the engine or stabilizers if the ship mostly takes damage to the nose. Destruction depends on where the hits land, and after an element is fully destroyed the damage passes to neighbouring elements. [player observation]

**Penalties.** Every frame the component's parameters are recomputed from the originals (with upgrades):
`parameter = original × (1 − component_damage × (1 − k))`, where `k` is the ship's value of `mdamage_<component>_<parameter>`
(`SHIPS.INI`; for `k` < 1 the parameter falls, for `k` > 1 it grows). Damage 0 — the parameter is the same as for an intact ship,
damage 1 — `original × k`. What each component degrades:
| component | parameters | example: the player's ship in the recordings, at full damage |
|---|---|---|
| engine | thrust, top speed | both ×0.9 |
| nose | pitch strength and limit angle | ×0.6 |
| stabilizers | turn strength and limit angle, roll strength and limit angle, turn damping, turn build-up | turn ×0.6, roll ×0.8, build-up ×1.4 |
| airbrakes | brake strength, brake build-up, roll/pitch and turn from the brakes | strength ×0.5 |
Different ships have different `k` (for example, thrust 0.6…0.9, turning 0.6…0.8). The penalty formula is the same in both versions of the game.

**Hull durability.** The four main hull zones have individual durability shares; in each model's data these shares add up to 100 %. A higher share corresponds to a zone's greater resistance to accumulating damage. The total shield capacity is set separately; the exact relation of the shares to the number of hits has not been established. [code; PAL data; not verified by behaviour]

**Repair.** On a pit lane with recharge (PHY-24) damage decreases at the same time as the shield grows, and the parameters
return along with it. The repair rate is 0.7 damage per second (PAL), i.e. from a fully wrecked
state ≈1.4 s [code; ✓ league recordings PAL: 1.0 → 0 in 1.44 s, twice]. In US it is 1.2 times faster, like other per-substep
quantities (GEN-7): 1.0 → 0 in 1.20 s [✓ league recordings US, twice]. (The earlier "1.9 s" was a counting error: it included the
tail of the shield recharge after the repair had ended.) Visible hull damage on the pit lane also disappears [✓ player observation, PAL]: a component's part looks intact again
only when the component is repaired **completely**. All components are repaired simultaneously and at the same rate, so the less wrecked
ones become "whole" earlier: in the recording the stabilizers (0.65) after ~0.9 s of recharge, the nose (1.0) after ~1.3–1.4 s, the engines according to
how wrecked they themselves were [✓ recording]; the canopy and cockpit (they have no component) — **immediately** on entering the recharge [✓ recording, three entries to the
pit lane]. While a component is being repaired, its damage is distributed equally among its parts.
Without a pit lane damage only accumulates: in Time Trial (the pit lane is enabled there, but the player did not enter it) the ship
crashed against the walls until destroyed on lap 10 of Mandrashee 2R [✓ player observation, PAL].

Observation (the same run: walls only, no weapons) [✓]: component damage from walls **accumulates** — the nose is first to
reach the limit (by lap 2), then the stabilizers, the engine (by laps 6–7), the airbrakes (by laps 9–10).
When the engine is fully damaged, acceleration in the 700–1100 km/h range drops by about a third (~150 → ~90–115 km/h
per second), top speed on straights is lower by ~10–15 %, and sideways slide grows by ~10 %. The player felt
that damage affects handling — the observation confirms this.

## SHIP-8. Ship states
| state | how it occurs | what happens |
|---|---|---|
| in the race | start | normal physics |
| autopilot | AUTOPILOT weapon; after the finish | the AI controls, the gamepad is ignored (FLOW-10) [✓] |
| stricken (AI) | hit by a number of weapon kinds | a "stricken" mark for **3.0 s**, speed unchanged (WPN-10) [✓] |
| stricken (human) | same | the speed multiplier drops to **0.24** and recovers, **1.9 s** in total (WPN-10) [✓] |
| AG Stinger / Gravity Bomb | hit | stalls and sags for up to 2 s (WPN-12, WPN-14) [✓] |
| burning (lava) | 0.6 s on lava | speed decays to 50; after 7.0 s — removed (PHY-21) [✓] |
| **destroyed** | after a hit the shield < 0.9 (zeroed, SHIP-6) | SHIP-9 |
| out of the race | finish, elimination | places/points are fixed; a ship that has finished — on autopilot |

## SHIP-9. Destruction [✓ frame-by-frame observations]
1. Shield = 0 → the ship is **destroyed**: every frame the maximum speed (`maxspeed`) is multiplied by 0.985 but does not drop
   below 50 (from ~1450 the minimum is reached in about 4.5 s, TC-7); both airbrakes are forcibly clamped.
2. Intermediate stages at +1.2, +2.4, and +4.4 s from destruction (what changes besides effects — OQ-7).
3. After **7.2 s** (360 frames) — **out of the race**, "eliminated" in the finish table. In two-player modes with respawn
   the human's ship is instead restored after 8.2 s (RACE-23).

What it looks like to the player [✓ player observation, PAL, Time Trial; the second case — the ship was destroyed by force in the open: ✓ modified game, PAL]:
- on the last divisions of the shield — the text "shield energy critical";
- **0 s** (shield 0): sparks and debris fly from the ship, it smokes and burns, crawls with decaying speed, controls
  have no effect;
- **≈ +1.3 s**: the ship **falls apart into large pieces** (wings, hull, canopy fly apart), a blue ring spreads
  over the ground, then a big fireball for ~1 s;
- **≈ +2.6 s**: a small **pilot capsule** (`[escape pod]` in `SHIPS.INI`) remains where the ship was, at first on fire;
  a **rescue droid** fades in smoothly above — a large dark craft with the text "RESCUE", hovering above the track;
  the capsule crawls along the track to it by itself;
- **≈ +5.5 s**: the capsule disappears (picked up), the droid dissolves;
- **7.2 s**: in Time Trial — the text "no medal awarded", then exit to the main menu.
The moments of the stages in the recordings coincided with +1.2, +2.4, +4.4, and 7.2 s.

## SHIP-10. Kill [✓]
A destruction is credited as a **kill** to the ship whose weapon caused it (if there is one). An elimination without
a culprit (walls, lava, etc.) is credited to nobody. Kills are counted separately in each race:
for each slot — the set of slots it destroyed.

## SHIP-11. Input [✓]
Input is a set of actions plus two analog axes; the AI fills the **same** fields (AI-1).

| action | default |
|---|---|
| steer left / right (axis −255…255) | D-pad / stick |
| pitch (axis −255…255) | D-pad / stick |
| throttle | Cross |
| fire (with press strength) | Circle or R1 |
| airbrake left / right | L2 / R2 |
| look back (the weapon fires backwards) | L1 |
| drop / absorb weapon | Square |
| change view | Triangle |
| pause | Start |

Pause, change view, and drop weapon trigger on a **press** (the "released → pressed" transition), the rest while held. [code]
Stick dead zones and sensitivity are up to the implementation.

## SHIP-12. Throttle before the start [code]
Throttle pressed before the start is marked in the input by a separate flag; it is needed for the "stalled" rule (FLOW-6, FLOW-7).

## SHIP-13. Hull dimensions [code]
When the race is set up the ship gets a set of hull reference points (about ±3.0 in width, 0.4 in height,
from −4.0 to 8.06 in length), apparently for collisions. The source is the ship model, not the parameter file; the exact geometric interpretation remains open (OQ-4).

## SHIP-14. Ship version and speed class [✓ two profiles; rule — code]
The player's ship **upgrade share**: `p = floor(100 · Σ(level + 1) / Σ(number_of_levels))` over the six groups of SHIP-5,
where a group's level is 0…(number_of_levels − 1) or −1 ("not purchased"), and the group's **number of levels** is the largest n
for which at least one key `<GROUP>_..._UPGn` of this ship in `SHIPS.INI` is not 0 (checked for all 16 ships;
for Feisar lead — 5, 3, 5, 5, 3, 5).

| p | model version (folder) | speed class |
|---|---|---|
| 0–24 | `VECTOR` | 1 |
| 25–49 | `VENOM` | 2 |
| 50–74 | `RAPIER` | 3 |
| 75–100 | `PROTO` | 4 |

- When a purchase raises `p` across the threshold 25 / 50 / 75, after confirmation the **"ship upgraded"** screen is shown:
  a rotating ship model already of the **new version** and an "accept" button [✓ player observation, PAL].
- In single-player modes the race's speed class = the version number (table). In a challenge the event sets the class (FMT-8).
  In two-player — the class setting in the menu (version = class − 1).
- **All** ships in the race, including the AI, get the same version: the one that corresponds to the race class (the AI is "pulled up"
  to the player's class). There is one model per team and version: the lead and second of the same team fly the same model
  (in the data there is one `SHIPMESH.MEM` file per team and version; FMT-17) [✓ files].
- Zone uses a separate ship `SHIPS/SECRET/`. [code]
- The ship model in the menus (ship selection, hangar, "ship upgraded") is **not different** from the model of the same ship on the track:
  the same shape and the same paint [✓ player observation].
- On hull damage no separate model is substituted: parts of the same model are damaged (SHIP-15).
- Example: Feisar lead with levels 3, 1, 3, 3, −1, 4 → `p = 73` → `RAPIER`, class 3 (that is what happened in the race); a profile with no
  purchases → `p = 0` → class 1 (TC-25).

## SHIP-15. Visible hull damage [✓ observations on 4 ships and a recording of 72 touches; rule — code]
- The model's part groups (FMT-22) are divided into **6 areas** by a keyword in the group name: nose — `NOSE`;
  engine — `ENGINE`; stabilizers — `STABILITY`; airbrakes — `BRAKE`, `RUDDER`,
  `FLAP`; cockpit — `COCKPIT`; canopy — `CANOPY`. These words are sufficient: every group name in all 33 ships
  contains exactly one of them (except `GUN_WEAPON`) [✓ files].
- Damage is shown **for each group separately**. Each group has its own damage scale 0…1; the ship's full shield
  is divided equally among the groups: a hit that took off `x` of shield adds `x / full_shield × number_of_groups` to a group
  (for a ship with 12 groups and shield 71, a wall touch of −1 shield gives a group +0.17). The hit goes to the group **nearest to the point
  of impact** that is not yet fully destroyed; the excess passes to the next nearest. When a group's scale
  reaches **0.75**, the damaged version is shown instead of the intact one — with wall touches that is the **5th touch** of one
  group, and the 6th finishes it off to 1. [✓ video, Time Trial Alca Vexus 2F: the canopy changed its look in the frame of the touch, after the flash
  of the impact] If the nearest undestroyed group is far from the point of impact (farther than ~10 units), the hit on
  it is weakened, and farther still does not reach it at all and the shield loses less [code]. In the recording of 72 touches: 51 took off exactly
  1 each, 20 slightly less (0.82…0.99, the hit went to a distant group); after those 71 touches 1.16 of shield remained, the 72nd
  took it below 0.9 — the shield was zeroed, the ship destroyed (SHIP-6). In total 71 was taken off — the entire shield [✓ recording]. At the moment a group becomes damaged the game emits **debris particles** [code]; in the video
  (rear camera) they cannot be told apart behind the impact flash, and frame-by-frame analysis gave nothing either — the look is not confirmed. Particles
  in the port may differ from the original (the implementer's decision).
- A component's damage (SHIP-7) is the average over its groups: a nose of one group is wrecked in 6 touches, an engine of two in
  12. The cockpit and canopy take hits on a par with the others, but do not affect handling.
- Time Trial PAL recording, Mandrashee 2R, 72 wall touches until destruction, a ship with 12 groups [✓ recording]: nose
  (touches 1–6) → the side stabilizers: touches with the right side went into one, with the left into the other (7–19) → canopy (16–24)
  → cockpit (24–30) → front and rear engines (30–45) → airbrakes and the rear stabilizer (39–72). The last,
  72nd touch took off the last of the shield, and by then all 12 groups were wrecked.
- The weapon part `GUN_WEAPON` is always visible, regardless of whether the ship has a weapon; it is hidden only on a
  destroyed ship at the late stages of destruction (SHIP-9). [✓ 88 observations]
- The canopy animation (FMT-23) does not play while the ship is intact (the canopy is in the position of the first key). It starts after the first
  stage of destruction (SHIP-9) — apparently the pilot ejecting — and then continues; in all observations after
  it starts it is at an intermediate pose [✓ 551 observations]. The canopy animation cannot be made out on screen: about 1.3 s after
  destruction the ship falls apart into pieces (SHIP-9); at the start and during the race the canopy does not move
  [✓ player observation, PAL]. (How to do the canopy in the port is the implementer's decision.)

## SHIP-16. Upgrade levels in a race [code; ✓ race recording: 570 AI ships in 57 races]
Group level: −1 — no upgrade, 0…(n − 1) — level 1…n, where n is the number of levels of the group for this ship (SHIP-14).
Before each race:
1. For all ships all groups are reset to −1.
2. **Demo run** (attract mode): it stays that way — nobody has upgrades.
3. **Single-player modes:** the player gets their purchased levels from the profile. In a challenge all 16
   pilots get levels from the profile.
4. If the event allows pulling opponents up (an event field, FMT-8; so in most events):
   - the reference level L = the player's TOPSPEED group level;
   - in a challenge with a set minimum c ≥ 1 (FMT-8): all the player's groups = `min(c − 1, n − 1)`, and L is that level;
   - in a league `L = max(L, c)`;
   - every **other** ship in every group gets `min(max(min(L, n − 1), player_level_in_the_group), n − 1)` —
     that is, not below L and not below the player, but not above its own maximum.
5. **Two-player modes:** for all ships each group = `⌈(n − 1) · q / 100⌉`, where q = 0 / 34 / 67 / 100 according to the
   "upgrades" setting in the two-player mode menu.

Consequence: opponents are always upgraded at least as much as the player, and their speed class (SHIP-14) is the same.
