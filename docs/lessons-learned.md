# Engineering Lessons Learned

## 1. Preview state is not broker state

A draggable chart object can move instantly while an external Working order changes asynchronously. The UI should preview locally, submit deliberate changes and then re-synchronize from platform-confirmed state.

## 2. Pre-fill and post-fill protection are different systems

Before fill, Stop/Target values are planning geometry. After fill, protection is actual working order state tied to the real position and fill price. Mixing those states creates fragile behavior.

## 3. Transient UI geometry should not destroy a valid order

Dragging through an invalid risk geometry can momentarily produce impossible values. A safer response is to reject/revert the unsafe change, not cancel a valid pending Entry.

## 4. Flat must be terminal

Any protection-repair routine must respect flattening and final flat state. Otherwise a well-intended self-healing path can become the source of unintended exposure.

## 5. Live enablement deserves a separate version

Keeping a frozen simulation/UAT baseline made live-account changes auditable and preserved a known recovery state.

## 6. Execution infrastructure is not a trading strategy

Robust order handling and risk controls can improve operational discipline, but they do not create market edge or guarantee profitability.
