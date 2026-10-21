# Sanitized Architecture

![Architecture](../assets/architecture.svg)

## Public system view

```text
Analysis instrument / chart
          |
          v
Cross mapping + risk sizing
          |
          v
Review / Confirm + account gate
          |
          v
Entry order lifecycle
          |
          v
Actual filled position
   |              |
   v              v
Protective Stop  Optional Target
        \        /
          native OCO
              |
              v
BE / Trail / manual management
              |
              v
Close All terminal cleanup
```

## Design principles

- Analysis and execution instruments are separate concepts.
- Risk is calculated using execution-instrument economics.
- Pre-fill geometry is intent; post-fill protection is real order state.
- Platform-confirmed state is authoritative over chart preview state.
- Protection may tighten but automation should not loosen it unintentionally.
- Flat/flattening state is a terminal boundary for custom protection.

The diagram intentionally omits private class names, account/provider details, proprietary source and operational identifiers.
