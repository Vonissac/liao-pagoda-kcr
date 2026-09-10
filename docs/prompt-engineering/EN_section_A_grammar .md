# Architectural Structural Description Language for Liao-Jin Masonry Pagodas: LPSL v3.0 Specification (Section A)

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

## 2. Top-Level Component Sequence Whitelist

Top-level components are connected sequentially from left to right using `-` (physically corresponding to the orientation from the pagoda apex down to the ground level). **Outputting any top-level ID not included in this whitelist is strictly prohibited.**

| Code | Name | Syntactic Attachment Constraints and Physical Meaning |
| --- | --- | --- |
| **a** | Uppermost specialized pagoda eaves | Must and can only appear at the absolute beginning of the entire sequence (immediately following `Global`). |
| **c** | Standard pagoda eaves | Core unit of the eaves section; appending `[...]` behind it is strictly prohibited. |
| **b** | Corbelled tier / Waist tier | Articulation and transitional tier. |
| **r** | Inverted corbelled tier | Transitional tier tapering from bottom to top (narrow top, wide base). |
| **d** | Bracket system (Puzuo) tier | Structural support beneath eaves. **Must be immediately followed by an attribute slot**, e.g., `d[type=d1]`. |
| **m** | Balcony (Pingzuo) tier | Storeyed-pavilion exterior gallery/balcony tier. |
| **h** | Plain surface tier | Physical flat transitional tier. |
| **e** | Pagoda body core | Critical boundary point of the entire pagoda. **Must be attached with both attributes and nesting**, formatted as `e[col=eX](internal_decorations)`. For the last `e` in the sequence, everything to its left belongs to the eaves zone, and everything to its right belongs to the base zone. |
| **f** | Lotus petal tier | Upright or inverted lotus base, typically situated directly beneath the pagoda body. |
| **g** | Arched niche (Humen) tier | Core tier of the pagoda base. **Must be attached with both attributes and nesting**, formatted as `g[num=X](internal_decorations)`. |
| **k** | Solid parapet panel | Protective/decorative solid parapet of the pagoda base. |
| **o** | Balustrade | Protective/decorative balustrade of the pagoda base. |
| **j** | Sculpture tier | Standalone physical statuary/sculpture tier. |
| **n** | Base false door | Carved false door located in the pagoda base section. |
| **i** | Lowermost base platform tier | Physical ground level tier, serving as the absolute terminal point of the entire pagoda. |
| **l** | Attached front entrance chamber (Qiansha) | Independent structure attached in front of the pagoda; if present, the entire sequence terminates with `-i-l`. |

---

## 3. Whitelist for Nested Decorative Tiers and Detail Component Codes

Inside the nested parentheses `(...)` of composite components, and only there, the following detail decoration codes may be assembled using `-` or `/`.

### 3.1 Permissible Codes Inside Pagoda Body Nesting `e[col=eX](...)`

* **Corner Column Style Whitelist (exclusively for attribute slot `col=`)**: `e1` (standard column), `e2` (octagonal column), `e3` (cylindrical column), `e4` (bundled bamboo column), `e5` (plum blossom column).
* **Wall Surface Decorative Component Whitelist (exclusively for use inside parentheses `(...)`)**:
* `e6` : Mullioned window with diamond-section bars (Poziling window)
* `e7` : Lattice window (Geshan window)
* `e8` : Arched niche panel (Humen panel)
* `e9` : Engaged wall column / intermediate column
* `e10` : Brick-carved canopy / drapery curtain
* `e11` : Carved false door (double-leaf opened)
* `e12` : Carved false window
* `e13` : Carved flying apsaras (Feitian)
* `e14` : Buddha niche
* `e15` : Bodhisattva / Heavenly Guardian sculpture
* `e16` : Brick-masonry false window (blind/closed)
* `e17` : Solid plain wall surface



### 3.2 Permissible Codes Inside Arched Niche Tier Nesting `g[num=X](...)`

* **Quantity Attribute (exclusively for attribute slot `num=`)**: `X` must be a specific positive integer (e.g., `1`, `2`, `4`).
* **Internal Unit Code Whitelist (exclusively for use inside parentheses `(...)`)**:
* Intermediate column components directly reuse: column codes `e1` through `e5`.
* `g8` : Carved lion inside arched niche
* `g9` : Carved musician inside arched niche
* `g10` : Carved botanical floral relief inside arched niche
* `g11` : Carved transformed child (Huasheng boy) inside arched niche
* `g12` : Empty arched niche (unadorned / without relief)



---

## 4. Strict Generation Guidelines

1. Translation must strictly reflect the actual physical structure documented in historical literature.
2. Attribute slots `[...]` must never be used arbitrarily; they are permitted exclusively following the component codes `Global`, `d`, `e`, and `g`.
3. The horizontal hyphen `-` and vertical slash `/` inside parentheses `(...)` must conform to architectural logic, and all parentheses must strictly close in matched pairs.
4. **No explanations allowed**: The model is strictly restricted to outputting only the single-line, finalized, standard LPSL v3.0 string derived from the derivation.