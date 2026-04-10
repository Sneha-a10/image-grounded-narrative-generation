# Selection & Escalation Logic Specification

Location: system_core/constraint_generation

------------------------------------------------------------------------

## 1. Family Selection Rule

-   preset_family = experiment_mode
-   experiment_mode must exist in preset_registry.json
-   Allowed values:
    -   Neutral_Descriptive
    -   Reflective_Light
    -   Expressive_Grounded
-   If experiment_mode is invalid → return input validation error
-   User may select preset family only

------------------------------------------------------------------------

## 2. Level Selection Rule

-   preset_level = retry_count

Rules: - retry_count must be ≥ 0 - retry_count starts at 0 - retry_count
increments only after validation rejection - User cannot directly set
preset_level - No level skipping allowed - No level decrement allowed

------------------------------------------------------------------------

## 3. MAX_LEVEL Rule

-   MAX_LEVEL must be derived dynamically from preset_registry.json
-   MAX_LEVEL = highest defined level for selected preset_family
-   Must not be hardcoded blindly
-   Currently MAX_LEVEL = 2

------------------------------------------------------------------------

## 4. Hard Reject Rule

If:

    retry_count > MAX_LEVEL

Then return:

``` json
{
  "decision": "HARD_REJECT",
  "control_metadata": {
    "preset_family": "string",
    "preset_level": MAX_LEVEL,
    "trigger_reason": "initial | text_failure | image_failure | both"
  }
}
```

Rules: - No constraint object is returned - preset_level must equal
MAX_LEVEL - Output must be deterministic

------------------------------------------------------------------------

## 5. Trigger Reason Mapping

Mapping table:

  failure_type   trigger_reason
  -------------- ----------------
  null           initial
  text           text_failure
  image          image_failure
  both           both

-   Used only for metadata
-   Does NOT influence preset selection

------------------------------------------------------------------------

## 6. Determinism Guarantee

Output depends strictly on: - experiment_mode - retry_count -
failure_type

The component must NOT: - Inspect story content - Inspect image data -
Inspect user feedback - Use randomness - Modify preset registry at
runtime

Identical inputs must always produce identical outputs.
