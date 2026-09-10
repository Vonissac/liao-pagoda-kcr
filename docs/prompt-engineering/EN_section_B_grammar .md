# LPSL v3.0 Specification for Architectural Structural Description of Liao-Jin Masonry Pagodas

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

## 2. Structural Layer Whitelist

Top-level components are connected via `-`. The final `e` component appearing in the sequence serves as the core spatial demarcation point of the entire pagoda (everything to the left of `e` strictly constitutes the eaves zone, `e` itself represents the pagoda body, and everything to the right of `e` strictly constitutes the base zone).

| Code | Name | Permissible Spatial Section | Syntactic Constraints, Physical Meaning, and Typical Position |
| --- | --- | --- | --- |
| **a** | Uppermost specialized pagoda eaves | Eaves zone (leftmost) | **Must** appear at the absolute forefront (top tier) of the sequence. Coded independently due to its morphological divergence from standard eaves. |
| **c** | Standard pagoda eaves | Eaves zone | The core repetitive unit of dense-eaves pagodas. Some pagodas with fewer storeys lack standard eaves, using bracket sets instead to count storeys. |
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

## 3. Comprehensive Dictionary of Nested Decorative Tiers and Detail Components

### 3.1 Permissible Codes Inside Pagoda Body Nesting `e[col=eX](...)`

* **Corner Column Styles (Attribute slot `col=`)**: `e1` (standard column), `e2` (octagonal column), `e3` (cylindrical column), `e4` (bundled bamboo column), `e5` (plum blossom column).
* **Wall Surface Decorative Component Codes (Inside parentheses `(...)`)**:
* `e6`: Mullioned window with diamond-section bars (Poziling window) | `e7`: Lattice window (Geshan window) | `e8`: Arched niche panel (Humen panel) | `e9`: Engaged column / intermediate column | `e10`: Brick-carved canopy / drapery curtain
* `e11`: Carved false door (double-leaf opened) | `e12`: Carved false window | `e13`: Carved flying apsaras (Feitian) | `e14`: Buddha niche
* `e15`: Bodhisattva / Heavenly Guardian sculpture | `e16`: Brick-masonry false window (blind/closed) | `e17`: Solid plain wall surface



### 3.2 Permissible Codes Inside Arched Niche Tier Nesting `g[num=X](...)`

* **Quantity Attributes (Attribute slot `num=`)**: `X` must be a specific positive integer (e.g., `1`, `2`, `4`).
* **Internal Unit Codes (Inside parentheses `(...)`)**:
* Intermediate column components directly reuse column codes `e1` through `e5`.
* `g8`: Carved lion inside arched niche | `g9`: Carved musician inside arched niche | `g10`: Carved botanical floral relief inside arched niche | `g11`: Carved transformed child (Huasheng boy) inside arched niche | `g12`: Empty arched niche (unadorned / without relief)



---

## 4. Specification for Radial Polyhedral Cyclic Representation

When `Sides` is specified, multiple parallel groupings of `(...)` following a top-level component indicate that the pagoda faces alternate radially along its perimeter:

* Single set of parentheses `(A)`: All wall faces around the perimeter are completely identical; this structure repeats consecutively for `Sides` times.
* Two sets of parentheses `(A)(B)`: Pattern face $A$ and pattern face $B$ alternate sequentially. The cycle repeats around the pagoda for `Sides / 2` times (e.g., alternating between false door faces and false window faces).
* Dense-eaves pagodas predominantly possess an odd, relatively high number of storeys; storeyed-pavilion pagodas possess fewer storeys and may feature an even number. The storey count of a dense-eaves pagoda equals the sum of occurrences of `a` and `c`, whereas for a storeyed-pavilion pagoda it equals the number of occurrences of `e`.

---

## 5. Few-Shot Static Standard Long-String Encoding Examples (Without Reasoning Process)

*Note: The following examples serve solely to demonstrate the syntax and morphology of the finalized standard LPSL v3.0 strings generated under this knowledge base, functioning as formatting benchmarks.*

* **Input Description 1**: An octagonal brick pagoda with a base radius of 8.5 meters and 13 tiers of eaves in total. The uppermost eaves tier is specialized, followed downward by a 12-tier dense-eaves cycle, with bracket sets supporting beneath the lowermost eaves tier. The pagoda body features standard columns at the corners; its wall surface comprises flying apsaras - lotus pedestal - flying apsaras on the top tier, three canopies in the middle tier, and human figures - false door - human figures on the bottom tier. Beneath the pagoda body lies a lotus petal base, followed by a base arched niche tier featuring 2 arched niches per face with standard intermediate columns and botanical relief carvings inside. The exterior of the arched niche tier is fitted with a double-layered solid parapet, transitioning down to the lowest ground level.
* **Standard LPSL Encoding 1**: `Global(Sides=8,BaseR=8.5)+a-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-b-h-c-d[type=d1]-e[col=e1](e6-e14-e6/e9-e9-e9/e10-e8-e10)-f-g[num=2](e1-g10)-k-k-i`
* **Input Description 2**: A hexagonal brick pagoda with a base radius of 6 meters and 3 tiers of eaves in total. The first tier (uppermost eaves) carries a balcony and bracket sets; the second tier replaces standard eaves with an inverted corbelled tier; the third tier employs standard pagoda eaves. The pagoda body utilizes dragon-entwined corner columns, and among the six wall faces, false door faces alternate with false window faces. The base features a lotus petal tier, a balcony tier, an arched niche tier (3 per face, without intermediate columns, carved with human figures), an accessible false door for entrance, a ground-level platform, and an independent attached front entrance chamber.
* **Standard LPSL Encoding 2**: `Global(Sides=6,BaseR=6.0)+a-m-d-h-r-m-d-h-c-m-d-h-e[col=e2](e8)(e11)-f-m-g[num=3](e5-g8)-n-i-l`
* **Input Description 3**: An octagonal brick pagoda with a base radius of 5.0 meters, featuring 3 storeys of sequentially alternating pagoda bodies and eaves. The first storey (uppermost) has specialized eaves with a balcony and bracket sets beneath; the second-tier eaves exhibit physical mutation, using an inverted corbelled tier (narrow top, wide base) in place of standard eaves, also with a balcony and bracket sets beneath; the third storey (lowest) adopts standard eaves with an underlying balcony and bracket sets. The pagoda body adopts dragon columns at the corners, with false door faces and false window faces alternating clockwise across the eight wall faces. From top to bottom, the base sequentially comprises a lotus petal tier, a balcony tier, an arched niche tier (3 per face, without intermediate columns, carved with human figures), followed by a passageway false door, the ground-level platform, and an independent physical attached front entrance chamber on the outermost perimeter.
* **Standard LPSL Encoding 3**: `Global(Sides=8,BaseR=5.0)+a-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8-e10)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-o-d[type=d1]-c-m-d[type=d1]-e[col=e1](e8)(e11)-i`

---

## 6. Generation Guidelines

1. Directly map the historical textual input to its corresponding structural encoding strictly based on the rules and component whitelist provided in this knowledge base.
2. The horizontal hyphens `-` and vertical slashes `/` inside parentheses `(...)` must strictly conform to spatial division principles, and all parentheses must close in fully matched pairs.
3. **Strictly refrain from outputting any form of thought process, step-by-step reasoning, validation logic, or intermediate commentary.** The model must and can only output a single line containing the finalized, standard LPSL v3.0 string.