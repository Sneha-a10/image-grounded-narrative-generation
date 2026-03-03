# Control Metadata Schema

## Structure

``` json
{
  "preset_family": string,
  "preset_level": integer,
  "trigger_reason": "initial | text_failure | image_failure | both"
}
```

## Field Definitions

### preset_family

-   Type: string
-   Must match experiment_mode
-   Must exist in preset_registry.json

### preset_level

-   Type: integer
-   Must equal retry_count (bounded by max level)
-   Valid range: 0 to MAX_LEVEL

### trigger_reason

-   Type: enum
-   Allowed values:
    -   initial
    -   text_failure
    -   image_failure
    -   both

## Mapping Rule

-   If failure_type is null → initial
-   If failure_type is text → text_failure
-   If failure_type is image → image_failure
-   If failure_type is both → both

This field is for traceability only and must not influence constraint
selection.
