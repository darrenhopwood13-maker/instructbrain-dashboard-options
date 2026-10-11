## Variant 1: Control Room

### Design stance
The dashboard is an **instrument**, not a page. If it were a physical object it would be a control
panel, so it is dark, dense, and everything is above the fold.

### Key choices
- **Layout:** three columns that fill the viewport - readings rail, the instrument, the project list.
  Hairline rules instead of card boxes, so nothing is a "card" competing with anything else.
- **Typography:** monospaced numerals at large size. Digits do not shift width as values change,
  which matters on a screen that updates.
- **Colour:** the product's own navy `#24417B` and Laser Green `#57FF00` on a near-black ground.
  The accent is reserved for the number the eye must land on.
- **Interaction:** scope switch (all projects / one), a time window that really rescales the figures,
  hover-to-preview a project, a live clock, hover tooltips on every bar, and an overdue ticker.

### Trade-offs
- **Strong at:** looking like serious equipment on a large screen. Reads instantly to someone who
  already knows their own numbers.
- **Weak at:** phones - there is a lot on screen - and it hides the unassessed items, so it can make
  an account look tidier than it is.

### Best for
A site office or a director's second monitor. The "we take compliance seriously" screen.
