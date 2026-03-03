# Hard Reject Output Schema

## Emission Condition

Returned when retry_count exceeds maximum preset level.

## Structure

``` json
{
  "decision": "HARD_REJECT",
  "control_metadata": {
    "preset_family": string,
    "preset_level": integer,
    "trigger_reason": "text_failure | image_failure | both"
  }
}
```

## Rules

-   No constraint object is returned.
-   preset_level must equal MAX_LEVEL.
-   decision must be HARD_REJECT.
-   Output must be deterministic.
-   No partial constraint emission allowed.
