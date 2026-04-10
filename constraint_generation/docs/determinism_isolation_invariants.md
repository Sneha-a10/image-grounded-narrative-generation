# Determinism & Isolation Invariants

Location: system_core/constraint_generation

This document defines the non-negotiable invariants that must hold for
the Constraint Generation component.

------------------------------------------------------------------------

## A. Determinism Invariants

1.  Identical input triplets must always produce identical outputs.

    -   Input triplet = (experiment_mode, retry_count, failure_type)

2.  No randomness is permitted.

    -   No random number generators
    -   No probabilistic selection

3.  No time-based behavior.

    -   Output must not depend on timestamps or execution time.

4.  No hidden cache or mutable global state.

5.  Output must depend strictly on:

    -   experiment_mode
    -   retry_count
    -   failure_type

------------------------------------------------------------------------

## B. Isolation Invariants

Constraint Generation must NOT:

1.  Read image data.
2.  Read caption text.
3.  Read story text.
4.  Read alignment scores.
5.  Read user overrides or user feedback.
6.  Access any external system state.

The component is policy-only and content-agnostic.

------------------------------------------------------------------------

## C. Monotonic Strictness Invariants

For any preset family:

1.  Level N+1 must be equal or stricter than Level N.
2.  negative_rules must not shrink across levels.
3.  max_length must not increase across levels.
4.  allowed_emotion_inference must not loosen across levels.
5.  perspective must remain constant across levels.

No strictness relaxation is allowed.

------------------------------------------------------------------------

## D. Registry Immutability Invariants

1.  preset_registry.json must be treated as read-only at runtime.
2.  No dynamic preset creation is allowed.
3.  No runtime modification of registry values is permitted.
4.  Any change to presets requires version control update and commit.

------------------------------------------------------------------------

## E. Hard Reject Invariants

1.  HARD_REJECT occurs only when retry_count \> MAX_LEVEL.
2.  HARD_REJECT must not emit a constraint object.
3.  HARD_REJECT must include control_metadata.
4.  HARD_REJECT behavior must be deterministic.

------------------------------------------------------------------------

## Enforcement Principle

If any invariant is violated during implementation, the architecture is
considered compromised.

All invariants must be verifiable through code review and testing.
