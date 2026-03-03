# Constraint Object Schema

## Structure

``` json
{
  "max_length": integer,
  "tone": string,
  "perspective": "third_person",
  "allowed_emotion_inference": "none | limited",
  "negative_rules": ["string"]
}
```

## Field Definitions

### max_length

-   Type: integer
-   Must be greater than 0
-   Defined strictly by preset registry
-   Must decrease or remain equal with higher preset levels

### tone

-   Type: enum (string)
-   Allowed values:
    -   neutral_descriptive
    -   strict_descriptive
    -   minimal_descriptive
    -   reflective_light
    -   soft_descriptive
    -   expressive_grounded
    -   controlled_expressive
-   Must match preset registry exactly

### perspective

-   Type: fixed string
-   Allowed value: third_person
-   Must not vary across families or levels

### allowed_emotion_inference

-   Type: enum
-   Allowed values: none, limited
-   Must tighten or remain equal at higher levels

### negative_rules

-   Type: array of strings
-   Allowed values:
    -   NO_NEW_ENTITIES
    -   NO_INTERNAL_THOUGHTS
    -   NO_OFF_IMAGE_LOCATIONS
    -   NO_TEMPORAL_JUMPS
    -   NO_REFLECTIVE_LANGUAGE
    -   NO_ADJECTIVAL_EXPANSION
    -   NO_EXTENDED_METAPHOR
-   No duplicates allowed
-   Must only expand (monotonic increase) across levels

## Immutability Rule

Once emitted, the constraint object must be treated as read-only. No
downstream component may modify, merge, or extend it.
