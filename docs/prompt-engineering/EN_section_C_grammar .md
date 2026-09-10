## 1. Core Construction Symbols and Strict Boundary Inviolables

This language describes the vertical and horizontal spatial configurations of ancient architecture through a one-dimensional string sequence. The model must strictly comply with the following symbol combination invariants:

### 1.1 Start and Termination Boundaries

* Every code sequence must strictly begin with `Global(Sides=X,BaseR=Y)+a`, where `X` denotes the number of planar sides of the pagoda (e.g., 8 or 4), and `Y` denotes the base radius (a floating-point value).
* The entire sequence must terminate definitively with `-i` (or `-i-l` if an attached front entrance chamber is present).

### 1.2 Strict Positional Constraints on Attribute Slots `[...]`

* **Inviolable Rule**: Attribute slots `[...]` **can only and must** immediately follow designated component codes (namely, the bracket set tier `d`, the arched niche [humen] tier `g`, and the pagoda body `e`) to declare specific styles, types, or counts. **Appending brackets `[...]` to any other non-attribute components (such as `c`, `b`, `h`, `i`, etc.) is strictly prohibited.**

### 1.3 Nested Operator `(...)` and Internal Spatial Segmentation Delimiters

The nested operator `(...)` expresses the internal single-face wall surface decoration of composite components (such as the pagoda body `e` and arched niche tier `g`). Its internal spatial segmentation delimiters are defined as follows:

* **Horizontal Sequencing Operator `-**`: Inside `(...)`, `-` denotes the **horizontal sequential tiling order on the same wall tier** (from left to right).
* **Vertical Layering Operator `/**`: Inside `(...)`, `/` denotes **vertical downward segmentation on a single-face wall surface** (from top to bottom). Each occurrence of `/` from left to right signifies moving down by one visual tier on the wall surface.

---

## 2. LPSL v3.0 Structural Layer Whitelist

Top-level component sequences are connected via `-`. **Outputting any identifier outside this list is strictly prohibited.**
*Note: The final `e` component appearing in the sequence serves as the core demarcation point of the entire pagoda. Everything preceding (to the left of) the final `e` constitutes the eaves zone; the final `e` itself represents the pagoda body; everything following (to the right of) the final `e` constitutes the base zone.*

| Code | Name | Permissible Spatial Section | Syntactic Constraints, Physical Meaning, and Typical Position |
| --- | --- | --- | --- |
| **a** | Uppermost specialized pagoda eaves | Eaves zone (leftmost) | **Must** appear at the absolute forefront (top tier) of the sequence. Coded independently due to its morphological divergence from standard eaves. |
| **c** | Standard pagoda eaves | Eaves zone | The core repetitive unit of dense-eaves pagodas. |
| **b** | Corbelled tier / Waist tier | Eaves zone / Base zone | Articulation and transitional tier. Frequently forms cycles with $c$ or $h$ in the eaves section; serves as a waist or transitional tier in the base section. |
| **r** | Inverted corbelled tier | Eaves zone / Base zone | Articulation and transition. Characterized by an upper width narrower than its lower width (tapering upward). Can replace $c$ to form cycles alongside $b$ in the eaves section. |
| **d** | Bracket system (Puzuo) tier | Eaves zone / Base zone | Sub-eave structural support. Frequently combined with $c$ or positioned near eave tiers, serving as a core repetitive unit in the eaves zone of dense-eaves pagodas. Typically carries attributes such as `[type=d1]`. |
| **m** | Balcony (Pingzuo) tier | Eaves zone / Body-eave interface / Base zone | Highly prevalent in storeyed-pavilion pagodas; can appear at the junction between pagoda body and eaves, within the eaves section, or in the base section. |
| **h** | Plain surface tier | Universal (Eaves / Body / Base) | Physical load-bearing and transitional flat tier, exhibiting an extremely high probability of occurrence across all sections. Frequently utilized for secondary support of balconies. |
| **e** | Pagoda body | Pagoda body zone (core demarcation point) | Carries primary decorative motifs. **The final occurrence of `e` in the sequence designates the pagoda body**. |
| **f** | Lotus petal tier | Base zone (upper section) | Decorative transitional tier. Typically situated beneath the pagoda body at the uppermost tier of the base, but may also occur at other transitional base locations. |
| **g** | Arched niche (Humen) tier | Base zone | Typically situated in the base section. Must carry quantity attributes and internal topology, e.g., `g[num=2](e1-g10)`. **Continuous repetition exceeding 3 occurrences is strictly prohibited**. |
| **k** | Solid parapet panel | Base zone / Eaves zone | Decorative structural tier, appearing in the base or eaves section (primarily in the base), situated on the exterior perimeter. |
| **o** | Balustrade | Base zone / Eaves zone | Decorative structural tier, appearing in the base or eaves section (primarily in the base), situated on the exterior perimeter. |
| **j** | Sculpture tier | Base zone / Body zone | Standalone physical statuary/sculpture tier. |
| **n** | Base false door | Base zone (terminal section) | A specialized structure in the base section allowing human entrance, present on only a minimal subset of pagodas. If present, it must be encoded at the very end before `i`, terminating in the form of `n-i` or `n-i-l`. |
| **i** | Lowermost base platform tier | Base zone (absolute terminal point) | Physical ground level tier / lowermost false door. If the attached front entrance chamber $l$ is absent, $i$ must sit at the absolute right end to conclude the entire LPSL sequence. |
| **l** | Attached front entrance chamber (Qiansha) | Base zone (independent terminal) | An independent structure situated in front of the pagoda (resembling an entrance hall). Since pagoda finials rarely survive, they are excluded from encoding. If present, it must be encoded after $i$, strictly concluding with `i-l`. |

---

## 3. Decorative Detail Whitelist

These codes are **strictly prohibited** from appearing independently as top-level components; they must be nested within structural layers via attribute slots `[col=...]` or parentheses `(...)`.

### 3.1 Pagoda Body (e) Dedicated Attributes and Attachments

* **Corner Column Styles (attached to `[col=eX]`)**:
`e1`: Standard column | `e2`: Dragon-entwined column | `e3`: Dharani pillar column | `e4`: Stupa-shaped column | `e5`: Column-free
* **Wall Decorative Components (attached inside `e(...)`)**:
`e6`: Flying apsaras (Feitian) | `e8`: False door | `e9`: Canopy / drapery curtain | `e10`: Statuary / Buddhist figure | `e11`: False window | `e12`: Auspicious clouds | `e13`: Flower base | `e14`: Lotus pedestal | `e15`: Pagoda relief | `e16`: Buddha-name inscribed brick | `e17`: Attached porch (Baosha)

### 3.2 Arched Niche Tier (g) Dedicated Internal Topology and Styles

The arched niche tier must be expressed via the `g[num=X](column_style - niche_interior_style)` structure:

* **[num=X]**: Attribute slot, where `X` is a positive integer denoting the number of arched niches contained within a single wall face of the pagoda base.
* **First Identifier inside Parentheses (range `e1`–`e5`)**: Designates the **intermediate column style** between arched niches (reusing pagoda body column codes: `e1` standard column, `e2` dragon column, `e3` dharani pillar column, `e4` stupa-shaped column, `e5` column-free).
* **Second Identifier inside Parentheses (range `g8`–`g12`)**: Designates the **sculptural motif inside the arched niche**:
`g8`: Human figures | `g9`: Animals | `g10`: Botanical flora | `g11`: Swastika pattern | `g12`: None (plain niche)

---

## 4. Advanced Spatial Logic Operator System

### 4.1 Wall Surface 2D Grid Layering Operators

Inside `e(...)`, moving from left to right corresponds spatially from top to bottom and from left to right:

* `-` denotes the horizontal sequential order of components from left to right within the same visual tier.
* `/` denotes vertical segmentation shifting down to the next tier below.

> **Deconstruction Example**: `e[col=e1](e6-e14-e6/e9-e9-e9/e10-e8-e10)`
> **Physical Mapping**: A single wall face of this pagoda body bears 9 decorative motifs (arranged in a 3×3 grid): the top tier features flying apsaras - lotus pedestal - flying apsaras; the middle tier features three canopies; the bottom tier features human figure - false door - human figure.

### 4.2 Radial Polyhedral Cyclic Operators (Parallel Parentheses)

When `Sides` is specified, multiple parallel groupings of `(...)` indicate that wall faces alternate radially around the perimeter:

* **Single set of parentheses `(A)**`: All wall faces around the pagoda are identical; this configuration repeats sequentially for `Sides` times.
* **Two sets of parentheses `(A)(B)**`: Pattern face $A$ and pattern face $B$ alternate sequentially. The cycle repeats around the pagoda for `Sides / 2` times (e.g., alternating between false doors and false windows).
* **Three sets of parentheses `(A)(B)(C)**`: Three wall surface patterns alternate sequentially clockwise, repeating for `Sides / 3` times.

---

## 5. Mandatory CoT Verification Chain

When generating or parsing any LPSL encoding, you must strictly execute the following logical verifications:

1. **Demarcation Point and Regional Partitioning**: Locate the **final `e**` in the sequence. Everything to its left is the eaves zone (where $f, g, n$ are strictly forbidden); `e` itself is the pagoda body; everything to its right is the base zone.
2. **Storey Conservation Constraint Formula**: Tally the total count of `a`, `c`, and `r` appearing before (to the left of) the final `e`. The sum must **strictly match** the physical total eaves count of the pagoda:

$$\text{Count}(a) + \text{Count}(c) + \text{Count}(r) == \text{TotalLayers}$$


3. **Arched Niche Tier (g) Structural Compliance Check**: Verify that all instances of `g` strictly conform to the format `g[num=X](e[1-5]-g[8-12])`.
4. **Extremity Rigid Boundary Check**: The starting segment must begin with `Global(...)+a`; the terminal segment must conform to one of the following: `...-i`, `...-n-i`, `...-i-l`, or `...-n-i-l`.

---

## 6. Classic Few-Shot Canonical Examples

### Example 1 (Dense-Eaves Octagonal Brick Pagoda - Corrected Logic for Guangji Temple Pagoda)

* **Input Description**: An octagonal brick pagoda with a base radius of 8.5 meters and 13 tiers of eaves in total. The uppermost eaves tier is specialized, followed downward by a 12-tier dense-eaves cycle, with bracket sets supporting beneath the lowermost eaves tier. The pagoda body features standard columns at the corners, and its wall surface is organized in a 3×3 grid decoration (top tier: flying apsaras - lotus pedestal - flying apsaras; middle tier: canopies; bottom tier: human figures - false door - human figures). Beneath the pagoda body lies a lotus base, followed by a base arched niche tier featuring 2 arched niches per face with standard intermediate columns and botanical carvings inside. The exterior of the arched niche tier is fitted with a double-layered solid parapet, transitioning down to the lowest ground level.
* **Reasoning Footprint**:
1. *Configuration & Eaves*: Begins with `Global(Sides=8,BaseR=8.5)+a`. 12 dense eaves tiers: 11 occurrences of `b-h-c`, with the final tier carrying bracket sets becoming `b-h-c-d[type=d1]`.
2. *Pagoda Body Localization*: Core demarcation point `e`. Standard corner columns `[col=e1]`. Single-face 3×3 pattern grid $\rightarrow$ `(e6-e14-e6/e9-e9-e9/e10-e8-e10)`.
3. *Base & Revised `g` Validation*: The right side of the pagoda body transitions to the lotus petal tier `f`. Next is the arched niche tier with 2 niches per face $\rightarrow$ `[num=2]`; intermediate columns are standard `e1`; interior relief is botanical `g10` $\rightarrow$ composed into `g[num=2](e1-g10)`. The exterior bears double solid parapets `k-k`, terminating at ground level `i`.
4. *Conservation Check*: 1 `a` + 12 `c` = 13 tiers. Satisfies start/end and demarcation boundaries.


* **Standard LPSL Encoding**: `Global(Sides=8,BaseR=8.5)+a-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-d[type=d1]-e[col=e1](e6-e14-e6/e9-e9-e9/e10-e8-e10)-f-g[num=2](e1-g10)-k-k-i`

### Example 2 (Alternating Multi-Faced Storeyed-Pavilion Hexagonal Brick Pagoda - with Attached Front Chamber)

* **Input Description**: A hexagonal brick pagoda with a base radius of 6 meters and 3 tiers of eaves in total. The first tier (uppermost eaves) carries a balcony and bracket sets; the second tier replaces standard eaves with an inverted corbelled tier; the third tier employs standard pagoda eaves. The pagoda body utilizes dragon columns at the corners, and among the six wall faces, false door faces alternate with false window faces. The base features a lotus petal tier, a balcony tier, an arched niche tier (3 per face, without intermediate columns, carved with human figures), an accessible false door for entrance, the ground-level platform, and an independent attached front entrance chamber.
* **Reasoning Footprint**:
1. *Configuration & Eaves*: `Global(Sides=6,BaseR=6.0)+a-m-d-h` $\rightarrow$ `r-m-d-h` $\rightarrow$ `c-m-d-h` (3 tiers in total).
2. *Pagoda Body Localization*: Core demarcation point `e`. Corner dragon columns `[col=e2]`. Dual-face alternation using two parallel sets of parentheses $\rightarrow$ `(e8)(e11)`.
3. *Base & Revised `g` Validation*: Transitions into the base on the right: sequentially `f-m`. Arched niche tier with 3 niches per face $\rightarrow$ `[num=3]`; column-free `e5`; internal human figures `g8` $\rightarrow$ composed into `g[num=3](e5-g8)`. Followed by `n-i-l`.
4. *Conservation Check*: 1(a) + 1(r) + 1(c) = 3 tiers of eaves. Satisfies conservation.


* **Standard LPSL Encoding**: `Global(Sides=6,BaseR=6.0)+a-m-d-h-r-m-d-h-c-m-d-h-e[col=e2](e8)(e11)-f-m-g[num=3](e5-g8)-n-i-l`

### Example 3 (Five-Storey Octagonal Storeyed-Pavilion Brick Pagoda - Xingwen Pagoda Typology)

* **Input Description**: An octagonal storeyed-pavilion brick pagoda with a base radius of 5.0 meters, featuring 5 storeys of sequentially alternating pagoda bodies and eaves. The first storey (uppermost) has specialized eaves with an underlying balcony and bracket sets; storeys 2 through 5 are standardly tiled via balustrades, bracket sets, standard eaves, balconies, and bracket sets. Corner columns across all storeys are standard columns, and across the eight wall faces, false door faces and false window faces alternate clockwise (with the 2nd storey false door face incorporating an internal Buddha figure relief). The bottom-tier pagoda body connects directly to the ground level.
* **Reasoning Footprint**:
1. *Configuration & Eaves*: `Global(Sides=8,BaseR=5.0)+a-m-d[type=d1]` $\rightarrow$ storeys 2 through 5 sequentially concatenated as `-o-d[type=d1]-c-m-d[type=d1]`.
2. *Pagoda Body Localization*: Core demarcation point `e`. Corner columns across storeys are standard `[col=e1]`. Dual-face alternation uses parallel parentheses $\rightarrow$ standard storeys are `(e8)(e11)`; the 2nd storey features an individual mutation embedding a Buddha figure `e10`, combining into `(e8-e10)(e11)`. The final occurrence of `e` represents the lowest-tier pagoda body (core spatial demarcation point).
3. *Base Validation*: Transitions into the base zone on the right. This pagoda adopts a minimalist base structure: the lowest pagoda body `e` connects directly to ground level `i` without lotus or arched niche tiers.
4. *Conservation Check*: 1(a) + 4(c) = 5 tiers of eaves. Each pagoda body and its accompanying eaves alternate sequentially; regional boundaries are distinct, parentheses are fully closed, satisfying conservation and terminal checks.


* **Standard LPSL Encoding**: `Global(Sides=8,BaseR=5.0)+a-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8-e10)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-i`

---

## 7. Execution Instruction

Now, based on the user's specific instruction (encoding generation or parsing), strictly perform reasoning in accordance with the granular whitelist above and the **5. Mandatory CoT Verification Chain**, and output the finalized standard LPSL v3.0 result.