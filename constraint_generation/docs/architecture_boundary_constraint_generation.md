# Architectural Boundary --- Constraint Generation

## Architectural Position

-   Called only by the Regeneration Controller
-   Feeds constraints to the Story Generator
-   Independent of the vision layer
-   Independent of the validation layer
-   Independent of the user feedback layer

## Isolation Guarantees

-   Does not inspect image features
-   Does not inspect caption text
-   Does not inspect story output
-   Does not inspect validation scores
-   Does not process user overrides
-   Does not influence regeneration logic beyond preset selection

## Critical Rule

Constraint Generation defines policy envelopes only.

If this component expands beyond preset selection and deterministic
constraint emission, the architecture is violated.
