# Interface Contract --- Constraint Generation

## Input Contract

``` json
{
  "experiment_mode": "string",
  "retry_count": "integer",
  "failure_type": "null | text | image | both"
}
```

### Input Rules

-   `experiment_mode` must match a predefined preset family
-   `retry_count` must be non-negative
-   `failure_type` used only for metadata logging
-   No image, caption, story, validation, or user prompt inputs allowed
-   Identical inputs must produce identical outputs

## Output Contract

``` json
{
  "constraints": {
    "max_length": "integer",
    "tone": "enum",
    "perspective": "third_person",
    "allowed_emotion_inference": "none | limited",
    "negative_rules": ["string"]
  },
  "control_metadata": {
    "preset_family": "string",
    "preset_level": "integer",
    "trigger_reason": "initial | text_failure | image_failure | both"
  }
}
```

### Output Rules

-   `constraints` must be fully explicit
-   `preset_family` must equal `experiment_mode`
-   `preset_level` must equal `retry_count` (bounded by max level)
-   `trigger_reason` derived from `failure_type`
-   Constraint object must be immutable
-   No runtime-generated fields allowed
