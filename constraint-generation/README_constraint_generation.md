# Constraint Generation

Location: `system_core/constraint_generation`

## Overview

Constraint Generation is a deterministic system-core module responsible
for selecting and expanding predefined constraint presets into a fully
explicit, immutable constraint object before story generation begins.

It enforces the narrative policy envelope under which the Story
Generator operates. It does not generate content, validate outputs,
process user feedback, or manage regeneration flow.

## Role Definition

Constraint Generation selects a preset family and strictness level based
strictly on control metadata and expands it into a complete constraint
object. The output is static, deterministic, and content-agnostic.

It defines what is legally allowed during story generation --- nothing
more.

## Responsibilities

-   Select preset family strictly from `experiment_mode`
-   Select preset level strictly from `retry_count`
-   Enforce monotonic strictness
-   Expand presets into explicit constraint objects
-   Emit traceable control metadata
-   Remain fully deterministic and stateless
-   Remain content-agnostic

## Non-Responsibilities

-   Does NOT inspect images, captions, or stories
-   Does NOT perform validation or alignment scoring
-   Does NOT process user feedback or user prompts
-   Does NOT trigger regeneration
-   Does NOT increment or manage `retry_count`
-   Does NOT adapt constraints dynamically
-   Does NOT modify presets at runtime
-   Does NOT generate narrative text
-   Does NOT merge or partially edit previous constraint objects

## Determinism & Isolation Guarantee

-   Identical inputs MUST produce identical outputs
-   Output depends only on `experiment_mode`, `retry_count`, and
    `failure_type`
-   No hidden state or adaptive logic is permitted
-   Presets are static and version-controlled
-   Instance-level overrides are handled outside this module

## Design Philosophy

If this component feels adaptive, intelligent, or content-aware, it is
incorrectly implemented.
