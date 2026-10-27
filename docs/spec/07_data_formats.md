# 07. Data formats

## FMT-1. General
All numbers are little-endian; `f32` is an IEEE float; `vec4` is 4 × f32. Paths inside the data are case-insensitive,
the separator is a backslash `\` [code]; an implementation may store the data as an ordinary `DATA/…` tree.

## FMT-2. Track directory `DATA/TRACKS/<NAME>/` [✓]
| file | contents |
|---|---|
| `<NAME><n><F/R>.TRK` | geometry: vertices, polygons with materials, sections and subsections, section links, lighting, visibility (FMT-3) |
| `<NAME><n><F/R>.TRI` | placed objects, splines, short paths, sounds (FMT-25) |
| `<NAME>C<n><F/R>.TRI` | small file of the same format: splines only ("Course1forward" etc.), no objects and no names (FMT-25) |
| `<NAME><n><F/R>.SPL` | named AI lines, pit lane and the **starting grid** (FMT-24) |
| `<NAME>_C<n><F/R>.LAP` | lap progress for each subsection (FMT-4) |
| `DESC.TXT` | 3 pairs of numbers (for layouts 1–3), then the track name and description in 5 languages |
| `VFX_SCRIPT.SPT` | text blocks `[Smoke]` `(name)` with particle parameters (power, time, sizes, colours, acceleration) |
| `CLOUDS.CFI`, `SKY_1…3/` (`SKY.MEM`, `TEXTURES/`) | clouds and sky (per layout) |
| `ANIM_*.MEM`, `SPEEDUP_WIDER.MEM`, `WEAPON_GRIDWIDER.MEM` | models of objects that the `.TRI` refers to by name (FMT-25) |
| `TEXTURES/` | textures of the track model (FMT-20) |
| `*.IPF`, `PHOTO.MUN` | video (`SHORT/MEDIUM/LONG.IPF`) and the track picture |

devilia has only the F layouts.

## FMT-3. .TRK [✓ all 45 files parsed to the last byte]
Header: `'VERS'`, `i32 version` (5), then i32: number of sections (S), polygons (P), vertices (V), SNRM normals (N),
`?` (Y), material names (M), light sources (L), `?`. Then blocks, each starting with a 4-character tag:

| tag | contents |
|---|---|
| `VERT` | V × vec4 — positions |
| `VNRM` | V × 16 bytes — vertex normals (in versions < 5 the colour is in `.w`); **the game pushes a ship away from walls using them** (PHY-25) — the vertex normals of a wall point out of the wall |
| `SNRM` | N × 16 bytes |
| (version < 5) | V × u16 — 15-bit colour |
| `POLY` | P × { u32 v0, v1, v2, u32 normal index, **u32 material index** } |
| `TOTS` | i32 subsections, polygon references, **light references, links** (sizes of the shared pools; order verified on all 45 files) |
| `SECT` | per section: u32 flags (bit0 → followed by 12 bytes: the **track re-entry point** after a fall, PHY-22 (previously mistaken for a pit lane offset)), u32 ?, 0x28 bytes (version > 3), i32 number of subsections, vec4 min, vec4 max (extents), 0x14 bytes centre+radius, **8 × vec4 — entry and exit "gates"** (4 points each: bottom/top × left/right), vec4 "up", 0x30 bytes, i32 number of links, i32 number of light sources |
| `SUBS` | per subsection: i32 number of polygons (K), vec4 min, vec4 max |
| `POLI` | per subsection: K × u16 — polygon indices |
| `CONN` | per section: (number of links) × i32 — neighbouring sections (forks exist) |
| `LITI` | per section: light source indices |
| `SURF` | M × { u8 len, char[len] } — **material names** (surface type — PHY-17) |
| `LIGH` | L × { u32, position vec4, colour vec4, direction vec4, parameters } |
| `VISI` | u32 n, then S rows of n bytes each: for each section — a **bit mask of track model cells** (FMT-26), least significant bit first; n = ⌈cells/128⌉·16 [✓ all 45] |

The "forward" direction of a section = `gate[2] − gate[0]` (PHY-15). [code]
The meaning of the unknown fields (`?`, Y, byte blocks) — OQ-32.

Walls in the original data [✓ all 45 files]: triangle strips with material `wall`
and **their own vertices** (walls sharing an edge with the floor — 0); the wall vertex normals coincide with the face normal
(median 1.0; zero and "foreign" ones — up to ~6 % at corners and joints); under a sloped wall the floor continues (~93–99 % of points).
Example, a straight of Florion Height 1F: a slope ~9.7 high extending outward ~6.9 from the edge of the road surface, the floor continues ~4 further past the top.

## FMT-4. .LAP [✓ all 45 files]
`f32 2.0`, `f32 check number` (= size in bytes of the corresponding `C*.TRI`), then for each subsection of the track
(in section and subsection order) `{ f32 lap_progress 0…1, u32 0 }`. The number of entries = the number of subsections in the TRK.
Lap progress grows linearly with distance along the track axis; **zero is 13–17 units before the far edge of the `start` surface strip**
(strip ~65 long) [✓ Florion 1F, 1R: deviation from a straight line ≤ 0.0012 lap].

## FMT-5. SHIPS.INI, WEAPONSTATS.INI [✓]
Text `key value`; in `SHIPS.INI` — sections `[<team> lead|second]`, `[zone ship]`, `[escape pod]`.
The meaning of the keys — SHIP-3 and WPN-15. `cost_*` are integers, the rest are floating-point numbers.

## FMT-6. PILOTS/SETUPS/<name>.INI [✓ all 16 pilots]
Lines of the form `@studynam::<key> <value>`. **They are read in line order, key names are ignored.** Order:
smoothness, alertness, skillLevel (1–3), gridRating, agression, agressionCalming, flapability, basicSpeed, stall,
flags (1/2), concentration, givenGrudge (−1 or a pilot number), lookAheadFactor, minTurn, airbrakeTurn, brakeTurn,
steeringFactor, slowDown, sharpBend, err_mult.

## FMT-7. GAME.BNI (66 320 bytes) [✓]
`"BNIF"`, `u32 0`, then three blocks in a row (the ~16 KB tail is unused):

| size | block |
|---|---|
| 0xFD8 | **initial progress** (FMT-10) |
| 0xAF00 | **200 events** × 0xE0 (FMT-8) |
| 0x5B0 | **16 leagues** × 0x5B (FMT-9) |

## FMT-8. Event (0xE0)
| offset | field |
|---|---|
| +0x00 | challenge type (RACE-14): 0 position, 1 lap time, 2 Elimination, 3 duel, 4 survival, 5 special [✓ 0–3] |
| +0x04 | track code `env·6 + circuit` [✓] |
| +0x08 | number of laps [✓] |
| +0x0C…+0x48 | arrangement of 16 pilots (OQ-33) |
| +0x4C / +0x50 / +0x54 | **bronze / silver / gold** thresholds (positions, seconds, number of kills) [✓] |
| +0x5C | number of ships |
| +0x60 | i32: weapon pads enabled (FLOW-3) [✓ six Feisar challenges] |
| +0x68 | i8: speed class − 1 for the challenge; −1 — not set (SHIP-14) [✓] |
| +0x69 | i8: minimum upgrade level c (SHIP-16): in a challenge — the player's levels, in a league — the reference level of the opponents [code; values 0…6] |
| +0x6A | i8: player's shield in a challenge, % of normal [code; duel: 15 → shield 9] |
| +0x6C | i32: pit lane enabled (PHY-24) [✓ race recording: disabled in the Elimination challenge] |
| +0x78 | mask of allowed weapons: bit = weapon number (WPN-1); bit31 — "default" |
| +0xB4 | f32: non-0 — boost the opponents' upgrades (SHIP-16) [code; 1.0 in 140 of the 200 events] |

Event number by mode — FLOW-2.

## FMT-9. League (0x5B) [✓]
`[0..7]` event numbers (0xFF — end), `[8]` the league unlocked by a win, `[9]` number of the additional bonus (0xFF — none),
`[10]` ?, `[11..]` name, ASCII with a terminating zero.

## FMT-10. Progress (0xFD8) — the same in the save profile
| offset | field |
|---|---|
| +0x000 | u64 mask of unlocked tracks (bit = track code) |
| +0x010 | u32 mask of unlocked weapons (bit = weapon number, WPN-1) |
| +0x014 | u32 mask of unlocked leagues |
| +0x01C | u32 mask of league bonuses |
| +0x020 | weapon weights, 27 values (WPN-5); value type — OQ-34 |
| +0x08C | u32 — probably upgrade credits (OQ-13) |
| +0x090 | 16 slots × 6 × i32: **purchased upgrade levels** (−1 — none) in the order TOPSPEED, THRUST, BRAKING, STABILITY, WEAPON, SHIELD (SHIP-5, SHIP-14) [✓] |
| +0xEF8 / +0xF00 / +0xF08 | u64 Arcade: 1st / 2nd / 3rd place (bit = track code) [✓] |
| +0xF10 / +0xF18 / +0xF20 | u64 Time Trial: gold / silver / bronze |
| +0xF28 / +0xF30 / +0xF38 | u64 challenges: gold / silver / bronze (bit `team·6 + number`) [✓] |
| +0xF40 | u32 completed leagues (bit = league) [✓] |
| +0xF44, +0xF48 | extra marks for the completion percentage (RACE-17) |
| +0xF58, +0xF60, +0xF68, +0xF6C | unlocked bonuses/features (OQ-34) |

## FMT-11. Save (PS2 memory card) [✓]
Folder `BESCES-50005`: icons (`icon.sys`, `*.icn`), the main file `BESCES-50005` (21 968 bytes) and the profiles
`BESCES-50005-00…04` (4258 bytes each).
- **Profile**: a 0x22-byte header (`u32 3`, file name in ASCII with zeros), then the progress block (FMT-10).
- The **main file** starts with a **profile directory**, entries of 0x48 bytes:
  `+0x00` name (ASCII), `+0x1F` save time UTC in BCD (sec, min, hour, —, day, month, year),
  `+0x2C…+0x39` summary for the selection screen (bytes): Arcade 1st / 2nd / 3rd places, league wins, challenge
  medals (g/s/b), Time Trial medals (g/s/b), extra marks, ?, rating (?), share of leagues for the percentage (`Lp`, RACE-17);
  `+0x40` u32 — probably play time, ms. The rest of the file — OQ-34.
- No checksum was found.
Reading the original's saves is optional; an implementation may store progress in its own format.

## FMT-12. Texts `TEXT/TEXT0..4.DAT`
Languages: a table of u32 offsets, then strings. String numbers needed by the rules: 0x26F "new lap record", 0x270 "final lap",
0x271 "perfect lap", 0x366 — the elimination caption, 0x368–0x36D — medals. A string by number = table start +
offset; a number above 65536 gives an empty string, there are no other checks. Menu string labels are stored as 16-bit
numbers (looked up at draw time), switch values — as 32-bit. [code; ✓ modified game, PAL]

## FMT-13. .MEM [✓ all 78 model files]
Images of structures: `u32 1, u32 nReloc, u32 0, u32 0`, then nReloc records, then data.
- A record without bits 31/30 is the offset of a 32-bit **pointer**; the pointer itself holds an offset from the start of the file
  (the load address is added to it after loading). Only the table tells a pointer from data.
- A record with bit 31 or 30 points (the low 30 bits are the offset) to a texture description field that
  is patched at load time; it is not a pointer.
Inside — models (FMT-17…FMT-20), fonts, animations. For your own implementation they have to be **converted** to your own
format; game logic does not depend on them.

## FMT-14. FRONTEND/PDSA_DATA [✓ modified game, PAL]
The menu screen state machine: `u32 0x2BF1`, `u32 number_of_states (160)`, per state
`{u32 first_transition, u32 number_of_transitions, u32 screen}`, then transitions `{u32 event, u32 kind, u32 state}`.
- The **event** is stored with an offset: 0x3A is added to it when read. Events: 0x3A "accept" (✕),
  0x3B "back" (△), 0x3C, 0x3D, … — menu items in order, 0x45 — an additional button (for example, ship
  details), 0x46 / 0x47 — "yes" / "no" in dialogs.
- **Kind**: 1 — open on top of the current one (with return), 2 — go to, 3 — return to the previous one.
- **Screen**: in the file it is a placeholder number; at startup the game itself puts here which screen to show in this
  state (several states may show the same screen).
- A screen sends an event, the state machine looks for a transition with this event in the current state; if there is no transition, the event
  does nothing.
- Some states: 7 — main menu, 8 → 22 → 23 → 25 → 26 — Arcade (ship selection 22, track 23),
  26 — race, 13 — two-player mode, 56 — its settings, 57 — two-player race settings. States 50, 53, 36,
  107 and others are not reachable from any transition. [✓ modified game, PAL: current state number 7, 26]

## FMT-15. FE_POSITION.TXT
`NAME value [rem comment]`: coordinates, colours, sizes of menu elements.

## FMT-16. Other files
`.TRF` — meshes (`TRFF` chunks, LOD), `.CLT` — textures, `.GEO` — points (weapon pylons, effects), `.HUD` — HUD
layouts, `.IPS/.IPF` — MPEG-2 video and animated billboards, `.INA` — sound config, `.VAG/.WAV` — sound.
Detailed formats are not needed for the logic (OQ-35).

## FMT-17. Model in .MEM: node tree [✓ all 33 ships and 45 tracks]
Offsets are from the start of the data (after the pointer table):
- `+0x000` u32 size, then the source file name (256 bytes);
- `+0x104` u32 number of top-level objects; `+0x118` pointer to an array of pointers to their nodes.

Node (0x140 bytes):

| offset | field |
|---|---|
| +0x00 | 4×4 f32 matrix: rows are axes, the last row is the translation; a point is transformed as a row vector `[x y z 1] · M` |
| +0x40 | bounding sphere (centre, radius) |
| +0x58 | pointer to a mesh (FMT-18) or 0 |
| +0x60 / +0x64 | number of child nodes / pointer to an array of pointers to them |
| +0x68 | name, ASCII with a terminating zero (up to 0x28 bytes): for top-level objects `LOD0…` / `TRACK`, for ship parts see FMT-22; meaningless names — `AA_`, `AAA_` |
| +0x90 | bounding box, 8 corners × vec4 |
| +0x110 | keyframe track (FMT-23) |

The world position of a part = the product of the matrices from it up to the root. Occasionally a matrix contains a reflection or a shear.

**Ship** (`SHIPS/<team>/<ship>/SHIPMESH.MEM`, for the secret one — `SHIPS/SECRET/`): usually 3 top-level
objects — the full model, a simplified one and a flat shadow. After applying the matrices: **Y is up, the nose is toward +Z** (engines at −Z),
length ~12.5 units. [✓ render of all 33 ships]
**Ship versions:** each team has 4 folders: `VECTOR`, `VENOM`, `RAPIER` — three tiers of one design in the team's colours
(different models and their own texture sets, partly shared), `PROTO` — a separate prototype ship with its own
livery; plus one ship in `SHIPS/SECRET/`. Which version is used when (upgrade level? speed
class? prototype unlocks?) — OQ-44. [✓ composition; selection — ?]
**Track** (`TRACKS/<TRACK>/<TRACK><n><F/R>.MEM`): one `TRACK` object with an identity matrix and one mesh;
the coordinates match the `.TRK` (FMT-3) exactly. [✓]

## FMT-18. Mesh and vertex packets [✓]
Mesh: `+0x00` u32 number of textures, `+0x04` pointer to a list of pointers to texture records (FMT-19),
`+0xA0` pointer to the packet chain. The chain is consecutive packets: a 16-byte header (the low 16 bits are the
data length in 16-byte words, bits 28–30 = 6 "return"), then the data. The end of the chain is the first header with a different
value of bits 28–30. Inside is a stream of graphics commands packed for the console's video chip (publicly available
platform documentation); the following is needed for parsing:
- The **texture setup command** is a list of pairs "parameter number + 64-bit value". For ships the texture
  parameter value is replaced by a stub: the upper 4 bytes hold the marker `0x12345678`, the lower 4 hold the **texture index in the
  mesh's list**. For tracks a real texture description is stored (FMT-20). The setup applies to all following
  chunks, including those in the following packets.
- A **vertex chunk** starts with a command that loads one 16-byte word into cell 0 (this is the primitive header:
  the low 15 bits are the number of vertices N; the primitive type is in bits 15–25 of the second 32-bit word), then the commands that load
  attributes, then the kick command. Primitive type: the low 3 bits — 4 triangle strip, 3 triangle list;
  bit 0x10 — textured. Attributes are distinguished by the destination cell:

| cell | attribute | format |
|---|---|---|
| 1 | position | 3 × f32 |
| 2 | colour RGBA | 4 × u8; 128 means 1.0 (values up to 255 are "overbright") |
| 3 | texture coordinates | 2 × f32, origin at the top-left corner |
| 4 | normal | 3 × f32 (tracks have none) |

A strip of N vertices gives N−2 triangles, the winding order alternates. It is more reliable to determine the front-face orientation
from the normals; materials should be made double-sided.

## FMT-19. Textures embedded in a model (ships) [✓ all textures of the 33 ships]
Texture record: `+0x000` pointer to the next one, `+0x004` `.clt` file name (256 bytes), `+0x1C0` description:
`+0x00` pointer to the list of levels (0 — there are no pixels in the file), `+0x14` width, `+0x18` height, `+0x24` bits per pixel
(8), `+0x40` texture description for the video chip (u64). Level (the first in the list is full size): `+0x10` image upload
packet, `+0x14` pixels, `+0x18` palette upload packet, `+0x1C` palette.
- The palette is 256 RGBA8 colours (16×16); alpha 0…128 means 0…1. The order of entries is permuted: in the colour index
  bits 3 and 4 are swapped.
- Pixels are 8-bit. If the upload packet uploads them as a 32-bit image of half the width and half the height, the bytes
  lie in the console's scrambled video-memory layout for 8-bit paletted textures (pixels are permuted; the
  inverse of this well-known permutation is needed); otherwise — row by row.

## FMT-20. Features of track models [✓ all 45 tracks]
- **Textures are not embedded:** texture records exist (name, size, description), but the list of levels is empty. The pixels are in
  `TRACKS/<TRACK>/TEXTURES/<name>.MEM` — file name = the `.clt` name from the record, without path and extension, in upper case.
  This is a `.MEM` image (FMT-13) with **one texture record** in the FMT-19 format (with pixels, palette and
  detail levels). [✓ files found for all 5979 texture references in all 45 tracks]
- The texture setup in the packets is a real 64-bit texture description (image and palette addresses in video memory,
  size and format). In the track and sky models the chunks refer to exactly this description, not to the texture
  record; the descriptions are rebuilt when a level loads, so their low 32 bits differ between
  levels and do not form a continuous table.
- **The texture load list is in the level file itself**: records of ~640 bytes, each holding its own path
  (`//data//tracks//<track>//textures//<name>.clt`) — Florion 1F has 181 of them, the pointer table is at the end of the file.
  The picture file name is taken from this path (`<name>.MEM` in `TEXTURES/`), not from the texture description.
  The earlier claim "all 5979 references found files via the mesh records" is wrong for track models: the texture records
  in the models are false positives (empty/garbage names), and the binding is given by the level's load list. Records with a zero description are textures
  whose place in video memory is assigned during the game (they are loaded on demand); **this is not a sign of animation**:
  ordinary permanent pictures are arranged the same way. For the converter the file from `TEXTURES/` is enough. [code; ?]
- **Moving pictures on tracks** are video: billboards and screens are `.IPF` clips from `DATA/BILLBOARDS/<team>/`,
  shown on the rectangles of the track's `ANIM_ANITEX_*` objects; the water on Mandrashee and Alca Vexus is
  the clips `BILLBOARDS/WATER/WATER.IPF` and `AWATER.IPF`. How the start board, lava and pads are animated — OQ-39. [code]
  Appearance [✓ player observation, PAL]:
  - an (active) **weapon pad** glows like a booster, but with a solid fill that shifts through colours
    (like RGB backlighting): fast enough that neighbouring pads are of different colours, and slow enough that
    the change is not noticeable before your eyes — the player sees "patches of different colours" (the shift is fast enough); the exact
    period does not matter;
  - **after pickup** the pad immediately turns **black**, with no animation; it lights up again also without animation
    [✓ player observation, PAL, 4 laps]; in modes where the pads are disabled,
    they are present on the track but are also black;
  - a **booster** glows steadily, blue; the player judges its strength by the length of the blue stripe, not by the number of arrows;
  - **lava** (Florion Height 2F/2R) is a static texture, no animation [✓ player observation, PAL]; it is barely visible in normal driving.
- Vertex colours contain "baked" lighting; there are no normals.
- **Second set of packets:** besides the main chain, the mesh has an area between the pointers `+0xB0` and `+0xB4` with
  many short command streams (without 16-byte packet headers). Each stream starts where some pointer from the track cell
  records points and runs to the start of the next one. Judging by the blending settings, these are the
  transparent and semi-transparent parts, drawn in a separate pass (2–14% of the track's triangles). [✓ composition; purpose — ?]

## FMT-21. SFX_TAGGED.GEO (ships) [✓ all 33]
`u32 N`, 12 bytes of padding, then N entries of 32 bytes: `{u32 tag, 3 × f32 direction, vec4 position}`.
Coordinates are in the ship model space (FMT-17). Ships have 8 points: 4 each with tag 0 and 1 at the right and left
engine at the stern, direction (0, 0, 1). These are the **engine flame** locations (the game takes them from here for the
flame effect). [code]

## FMT-22. Ship damage in models [✓ all 33 ships; when it is switched on — OQ-41]
Every top-level object except the shadow has child nodes that are **part groups**, one per area of the ship
(8–14 groups in the full model, 4–8 in the simplified one). A group has:
- **its own mesh — the intact version** of the area;
- **a single child node — the damaged version** of the same area (torn plating, ripped-off panels, protruding
  elements, cracks on the glass) in the same coordinates; almost all groups have it;
- the damaged version of the full model has 0–10 child **debris pieces** (separate pieces of plating and ragged edges).
The mesh of the top-level object itself (the hull) does not change. [✓ render of the intact and damaged versions]

The group name names the area and the damage zone (names are from the files, different artists wrote them differently):

| in the name | zone | example group names |
|---|---|---|
| `ENGINE` | engine (`mdamage_engine_*`, SHIP-7) | `DAMAGE_ENGINE`, `DAMAGE_ENGINE_LEFT_OFF` |
| `NOSE` | nose (`mdamage_nosecone_*`) | `DAMAGE_NOSE`, `DAMAGE_NOSE_OFF` |
| `STAB` | stabilizers (`mdamage_stability_*`) | `DAMAGE_STABILITY`, `DAMAGE_STABILITY_RIGHT_OFF` |
| `BRAKE`, `FLAP`, `RUDDER` | airbrakes (`mdamage_airbrakes_*`) | `DAMAGE_LFLAPA_BRAKE`, `DAMAGE_RBRAKE`, `DAMAGE_LRUDDER_BRAKE` |
| `CANOPY`, `COCKPIT` | canopy and cockpit (no zone of its own in `SHIPS.INI`) | `DAMAGE_CANOPY`, `DAMAGE_COCKPIT` |
| `GUN` | weapon unit, no damaged version (EG-R, Xios) | `GUN_WEAPON` |

Damaged versions are called `<area>_ON` (`NO_ON`, `ENG_LEFT_ON`, `STAB_RIGHT_ON`) or `AA_`; the suffix
`_OFF` on a group means "damage switched off". Debris pieces are `<area>_PART_nn`, `_PRT_nn`, `_EDGE_nn` or `AAA_`.
So the visible damage is switched **per area independently**: the intact version is replaced by the damaged one.
When exactly this happens and whether debris pieces fly off — OQ-41.

## FMT-23. Node keyframe track [✓]
`+0x110` u32: the upper 16 bits are the number of keys K, the lower ones are 1; `+0x114` u32 — length in frames (160–239);
`+0x118` — pointer to K keys of 0x38 bytes: `{u32 frame, 3×3 f32 rotation (rows), 3 f32 translation, u32 flags}`.
A key defines the node's whole local matrix (like the node matrix in FMT-17). A node without animation: K = 0 or 2 identical keys (frames 0
and the last). Only the **cockpit canopy** (`DAMAGE_CANOPY…`) of 22 ships moves: on some it swings open on a hinge
(rotation up to 60°), on others it lifts up (shift ~1.2). Frames are game frames (50 per second): a cycle of 3.2–4.8 s.
When the game plays this animation (ejection on destruction?) — OQ-42. [?]

## FMT-24. .SPL — AI lines and the starting grid [✓ all 18 files: Florion Height, Vohl Square, Cubiss Float]
`u32 100`, `u32` number of lines L, then L lines:
| field | size |
|---|---|
| number of points N | u32 |
| name (`AI_pitlane,0-40`, `AI_starting_grid_right,0-36`, `AI_1F_main_route,24-218`, `AI_1F_split10,0-35`…) | 40 bytes, tail filled with 0xCC |
| `u16 0xFFFF`, `u32 N−1`, `u32` link kind (3 — one next line, 2 — fork, 1 — ?), `i32` next line, `i32` second next (−1 — none) | 18 bytes |
| 12 bytes: zeros or flags (on forks) | 12 |
| N × `{f32 x, y, z, f32 left boundary}` — points (step ~21.5) and the offset to the left of the line (negative) | 16·N |
| N × `{f32 dx, 0, dz, f32 right boundary}` — unit sideways vector and the offset to the right | 16·N |
The main line is split into pieces with point ranges in the name (`…,0-10`, `…,10-18`); "next line" links join the
pieces, the branches (`split`), the pit lane and the two starting-grid lines into a network.
**The AI drives ships along the `.SPL` lines of the layout** [✓ modified game, PAL: the AI drives tracks with such lines without touching walls]. Data conventions that the AI does not forgive breaking
[✓ modified game, PAL]:
- **the "sideways" vector points right along the direction of travel**: (dx, dz) = (dir.z, −dir.x), where dir is the direction to the next point
  (so for 22040 of the 22339 points of the originals); with a reversed vector the AI picks a trajectory on the wrong side and hits the wall;
- **the joint between pieces**: the first point of the next line lies about one step (~21) **ahead** of the last point of the previous one
  (median over the 608 joints of the originals 21.4); if the next line starts behind, or far ahead, the AI
  turns around on the spot.
**The ship's place in Time Trial is at the start of the `AI_starting_grid_right` line** (~9 units along the direction of travel from its first point)
[✓ observation: Florion 1F, spawn place (−189.5, 3, −20.7), first point of the line (−181.0, 3, −18.3)].

## FMT-25. .TRI — objects, splines, paths, sounds [✓ all 36 files (large and small) are read to the last byte]
`'VERS'`, `i32 4`, then i32: objects, splines, paths, sounds, names. Then:
- `'NAME'` and the names `{u8 length with the zero, characters}` (model names: `anim_loop3000_gore3`, `speedup_wider`, `weapon_gridwider`…;
  small files have no names and no `NAME` tag);
- objects of 588 bytes: 4×4 matrix (rows, translation in the last row), `u32` name number, `u32` type, `u32` mask,
  `u16`, `u16`, 508 bytes (0xCC if the type does not use them). Types [files; purpose — ?]: **4** — the 16 places of the starting
  grid (`u16` = place 1…16, pairs of places ~53 across, ~61 along); **5** — places with extra data; **6** — booster
  model; **7** — weapon pad model; **10** — rare; **11** — animated scenery and service animations
  `anim_control*` (flyover cameras, `pd1…16`, `sp1…16` — 16 each, apparently for the ships at the start);
- splines: `{u8 length, name, u32 points N, N × 40 bytes (x, y, z, —, sideways vector x, y, z, —, f32 left, f32 right),
  u32 M, M × 7 i32 (split into pieces and links)}` — the same AI line networks as in `.SPL` (`.SPL` is their split into
  pieces);
- paths: `{u32 N, N × vec4}` — short polylines (4–8 points; one is a vertical rise of ~15, apparently the start lift);
- `'SNDS'` and sounds of 32 bytes: `{vec4 position, u32 sound, f32 near boundary, f32 far boundary, f32 1.0}`.
The small `C*.TRI` is the same format: 0 objects, 2–5 splines, 0 paths and sounds.

## FMT-26. Track model cells and visibility [✓ Florion Height 1F; cell count and `VISI` size — all 45 tracks]
Track model mesh (FMT-18, FMT-20): `+0xBC` — number of cells C, `+0xC0` — pointer to an array of cells of 0xD0 bytes:
| offset | field |
|---|---|
| +0x00 | 8 corners of the cell box (vec4, w = 1): the upper ones first (y max), then the lower ones |
| +0x80 | `u32` number of opaque lists (0/1), `+0x8C` — pointer to the list (a sequence of draw commands, ending with an end marker), `+0x90` — its size in bytes |
| +0x9C | `u32` number of semi-transparent lists, `+0xA0` — pointer, `+0xA4` — size (the area between `+0xB0` and `+0xB4` of the mesh) |
| +0xA8… | for some cells — a number, 4 f32 and 4 pointers (purpose — OQ-40) |
Cells are squares in plan (~230 × 220 at Florion 1F). A cell's list: a header of draw settings (texture selection, transparency
and blending mode), then batches of 3–12 vertices: primitive type (strip or triangle list), colours (4 × u8),
UV (2 × f32), positions (3 × f32). Which cells to draw is decided by the `VISI` row of the current section (FMT-3): **bit i — cell i**
[✓ for 96 % of the sections of Florion 1F all 10 nearest cells are marked visible]. The triangle winding order in the original
is mixed (~53/47) — there is no back-face culling.


## FMT-27. Track sky and clouds [code]

A track folder may contain (not for all tracks):

* `SKY_*` / `SKY` — directories, inside them `SKY.MEM` (an ordinary sky dome/panorama model, read as FMT-18) and `TEXTURES/` with texture `.MEM` files. Florion Height has three layers (`SKY_1..SKY_3`), CUBISS_FLOAT has four, VOHL_SQUARE has `SKY` (+`SKY.TRF`) and `SKY_1`/`SKY_2`.
* `CLOUDS.CFI` — Florion Height only (1396 bytes): the first 32-bit word = number of layers (3), then N blocks of 0x140 bytes (80 f32) and a tail of cloud vertices.

Layer block (80 f32): the first 16 are a 4×4 matrix (scale ~6400 units, i.e. the far view limit), then ~60 f32 (probably parameters of individual clouds: heights/sizes/speeds), the last 4 f32 are the final quadruple of parameters (purpose not deciphered, looks like speed/scale/texture repeat).

The tail is a pool of cloud vertices: groups of 4 vertices `{x,y,z,u,v}` (v is always 1.0), 20 vertices = 5 quads + 1 extra vertex (purpose unclear). Which quads belong to which layer and the meaning of the middle 60 f32 of the block could not be deciphered — an open item.
