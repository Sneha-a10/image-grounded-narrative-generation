# Test Strategy & Case Matrix

Location: system_core/constraint_generation

This document defines the complete test coverage requirements for the
Constraint Generation component.

All tests must pass before production implementation is accepted.

------------------------------------------------------------------------

# 1. Preset Selection Tests

## Test 1.1 --- Neutral_Descriptive Level 0

Input: { experiment_mode: "Neutral_Descriptive", retry_count: 0,
failure_type: null }

Expected: - preset_family = Neutral_Descriptive - preset_level = 0 -
Level 0 constraint object returned - trigger_reason = "initial"

------------------------------------------------------------------------

## Test 1.2 --- Reflective_Light Level 0

Input: { experiment_mode: "Reflective_Light", retry_count: 0,
failure_type: null }

Expected: - preset_family = Reflective_Light - preset_level = 0 - Level
0 constraint object returned

------------------------------------------------------------------------

## Test 1.3 --- Expressive_Grounded Level 0

Input: { experiment_mode: "Expressive_Grounded", retry_count: 0,
failure_type: null }

Expected: - preset_family = Expressive_Grounded - preset_level = 0 -
Level 0 constraint object returned

------------------------------------------------------------------------

# 2. Escalation Tests

## Test 2.1 --- Level Escalation to 1

Input: { experiment_mode: any valid family, retry_count: 1,
failure_type: "image" }

Expected: - preset_level = 1 - Level 1 constraints returned -
trigger_reason = "image_failure"

Verify: - max_length \<= Level 0 max_length - negative_rules length \>=
Level 0 - allowed_emotion_inference not loosened

------------------------------------------------------------------------

## Test 2.2 --- Level Escalation to 2

Input: { experiment_mode: any valid family, retry_count: 2,
failure_type: "text" }

Expected: - preset_level = 2 - Level 2 constraints returned -
trigger_reason = "text_failure"

Verify monotonic strictness properties.

------------------------------------------------------------------------

# 3. MAX_LEVEL Boundary Tests

## Test 3.1 --- At MAX_LEVEL

Input: { experiment_mode: valid family, retry_count: MAX_LEVEL,
failure_type: "image" }

Expected: - Valid constraint object returned - preset_level = MAX_LEVEL

------------------------------------------------------------------------

## Test 3.2 --- Beyond MAX_LEVEL

Input: { experiment_mode: valid family, retry_count: MAX_LEVEL + 1,
failure_type: "image" }

Expected: { decision: "HARD_REJECT", control_metadata: {...} }

No constraint object must be returned.

------------------------------------------------------------------------

# 4. Invalid Input Tests

## Test 4.1 --- Invalid experiment_mode

Input: { experiment_mode: "Invalid_Mode", retry_count: 0, failure_type:
null }

Expected: - Input validation error

------------------------------------------------------------------------

## Test 4.2 --- Negative retry_count

Input: { experiment_mode: valid family, retry_count: -1, failure_type:
null }

Expected: - Input validation error

------------------------------------------------------------------------

## Test 4.3 --- Non-integer retry_count

Input: { experiment_mode: valid family, retry_count: "one",
failure_type: null }

Expected: - Input validation error

------------------------------------------------------------------------

## Test 4.4 --- Invalid failure_type

Input: { experiment_mode: valid family, retry_count: 0, failure_type:
"invalid" }

Expected: - Input validation error

------------------------------------------------------------------------

# 5. Determinism Test

## Test 5.1 --- Repeatability

Call component twice with identical input: { experiment_mode: valid
family, retry_count: 1, failure_type: "image" }

Expected: - Outputs are deeply identical (field-by-field equality)

------------------------------------------------------------------------

# 6. Isolation Tests

## Test 6.1 --- Reject Unexpected Fields

Input includes additional fields: { experiment_mode: valid family,
retry_count: 0, failure_type: null, story_text: "Some story" }

Expected: - Input validation error

------------------------------------------------------------------------

## Test 6.2 --- No Content Dependency

Confirm that: - Story text does not alter output - Image data does not
alter output - User feedback does not alter output

------------------------------------------------------------------------

# Test Coverage Guarantee

Every branch in selection logic must be covered: - Valid family -
Invalid family - Valid levels - Boundary level - Hard reject - Invalid
inputs - Determinism verification - Isolation verification

If any test fails, implementation must be corrected before deployment.
