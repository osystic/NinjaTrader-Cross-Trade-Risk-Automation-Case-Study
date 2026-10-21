# Technical Overview

## Cross-instrument workflow

A mapping layer lets the operator analyze one futures instrument and route execution to a related micro contract. The order-management state machine then works against the execution instrument and selected account.

## Risk sizing

The default quantity is computed from initial Stop distance, execution-instrument point value and a maximum dollar-risk budget. This avoids using the analysis contract's value when a micro contract is actually being traded.

## Order lifecycle

The panel distinguishes:

1. setup/review;
2. submitted-but-unfilled Entry;
3. filled live position;
4. managed protection/automation;
5. flatten/closeout;
6. reset/recovery.

This distinction is important because protective orders should be tied to the actual filled position rather than assumed from the preview.

## Automation

Breakeven and trailing are stateful controls. Auto modes wait for configured triggers; manual controls let the operator change behavior mid-trade. An exact trail-trigger price can override the R-based trigger when explicitly configured.

## Failure containment

Unsupported live-account paths fail closed. During flattening, protective-order repair is disabled and active custom protection is cancelled defensively so flat state cannot be converted into unintended exposure by stale protection.
