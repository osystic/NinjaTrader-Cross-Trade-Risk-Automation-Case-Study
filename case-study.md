# NinjaTrader 8 Cross-Instrument Execution & Risk Automation

Anonymous engineering case study | Futures execution tooling | NinjaTrader 8 / NinjaScript C#

| Field | Value | Field | Value |
|---|---|---|---|
| Domain | Futures execution & risk management | Platform | NinjaTrader 8 |
| Delivery | Custom chart panel + operating setup | Status | Completed & handed over |
| Final accepted build | v0.4.25 | Multi-account copier | Deferred future scope |

## Executive summary

A discretionary futures trader required a workflow that could analyze one instrument while executing a mapped micro contract, calculate quantity from a fixed dollar-risk ceiling, manage Entry/Stop/Target geometry from the chart and progressively protect profitable trades through breakeven and trailing automation.

The work evolved from simulation-safe order management into controlled live execution. That transition exposed real-world state and timing defects that are difficult to prove in static code or simple simulation alone. The final delivery therefore emphasizes lifecycle correctness: broker-confirmed working prices, fill-aware protection, OCO behavior, post-fill modifications and a closeout path that cannot accidentally resurrect protection after the position is flat.

## P — Problem & constraints

The operational goals were straightforward to describe but coupled in implementation:

- analyze a full-size futures contract while executing a micro contract;
- size the position from Stop distance and a maximum dollar-risk budget;
- let the trader select/adjust Entry, Stop and optional Target directly on chart;
- require a deliberate review/confirm step before order submission;
- support both fixed-target and runner/trailing workflows;
- move protection to breakeven after a configurable favourable move;
- arm or immediately start trailing when the trader changes the plan mid-trade;
- keep order state synchronized with what the execution platform actually accepted;
- prevent unsupported live-account paths from executing;
- provide a reliable Close All that also removes protection;
- retain a recovery baseline and handover package.

The design also had to distinguish **planned protection before fill** from **actual broker-side protection after fill**. Treating those states as equivalent can create false confidence or invalid change requests.

## A — Architecture & decisions

### Analysis/execution separation

The chart remains the analysis surface. A mapping layer chooses the actual execution instrument. The risk engine uses execution-contract economics, not the analysis contract, so quantity reflects the instrument that will actually be traded.

### Fixed-dollar risk sizing

Risk is derived from:

```text
risk per contract = initial stop distance × execution instrument point value
quantity = floor(max dollar risk / risk per contract)
```

The panel preserves a manual quantity override, but the fixed-dollar calculation provides the default safety geometry.

### Explicit review and restricted live path

The trader reviews the prepared setup before Confirm. The final live version only permits simulation plus the explicitly supported live-provider path; unsupported/unknown provider paths fail closed.

### Pre-fill versus post-fill protection

Before fill, Stop/Target lines are setup intent. Once the Entry fills, actual protection is generated against the real position and actual average fill. When a fixed target is enabled, Stop and Target share an OCO relationship.

### Breakeven and trailing state machine

Automatic and manual controls are intentionally distinct:

- **Auto Breakeven** waits for the configured R trigger.
- **Move to BE** requests protection immediately using the configured offset.
- **Auto Trail** waits for the configured R or exact-price trigger.
- **Arm Trail** creates a one-off future trigger for the current trade.
- **Trail Now** begins trailing immediately.

Trailing only ratchets in the favourable direction and respects already-tighter protection.

### Terminal flatten boundary

A live-UAT regression showed that normal protection-maintenance logic could race with a flatten and recreate a protective order after the position had closed. The final design marks flattening/flat state as a hard boundary: protection maintenance is blocked, active custom protection is cancelled and any protection that appears while flat is cancelled defensively.

## C — Contribution & delivery

OSYSTIC's delivery covered:

- NinjaScript/C# panel architecture and implementation;
- chart-control and draggable order-geometry integration;
- cross-instrument mapping and quantity/risk calculation;
- account/provider safety gating;
- Entry and protection lifecycle management;
- native OCO protection after fill;
- breakeven/trailing automation and manual overrides;
- partial close and Close All behavior;
- simulation UAT and controlled live UAT;
- live-regression diagnosis and corrective versions;
- saved workspace/recovery discipline;
- full platform backup, separate NinjaScript export and operational handover guide.

A frozen UAT baseline was preserved independently from the final live build so future enhancements can start from a proven closeout point.

## E — Evidence & outcomes

The final controlled acceptance verified the end-to-end lifecycle:

1. supported live account path selected;
2. unsupported live provider path remained blocked;
3. Entry submitted and became Working;
4. chart Entry movement synchronized to the actual Working order;
5. pending Stop/Target setup remained editable;
6. Entry filled;
7. actual protective Stop and optional Target were created;
8. fixed-target protection shared a native OCO identifier;
9. post-fill Stop/Target changes updated the platform order state;
10. Close All flattened the position;
11. protection cancelled;
12. no orphan/replacement protection reappeared;
13. final position state was flat.

### Defects resolved through UAT

**Transient-risk cancellation.** A temporary invalid geometry during Stop dragging could cancel an otherwise valid pending Entry. The fix rejected/reverted unsafe transient geometry instead of cancelling the Entry.

**Entry-drag synchronization.** A chart line could move ahead of the broker-confirmed Working price. The fix made dragging a local preview, sent a single modification on release and re-synced from confirmed platform state.

**Close All race.** Protection could be recreated after flattening. The final version added a flatten gate, flat-position checks and account-wide defensive cancellation for custom protective orders.

## Outcome boundary

The completed system is **execution and risk-management infrastructure**. It does not forecast markets, create alpha or guarantee a profitable outcome. Live fills, slippage and provider behavior remain external realities.

The requested master/follower copier was discussed at closeout and intentionally left for a future separate project when multi-account execution becomes a priority.

## Confidentiality

This case study is independently written from verified delivery facts. It contains no confidential source, client identity, account identifiers, private screenshots, private conversations, commercial information or native recovery archives.
