# Multimodal AI Pipeline — UI

## File Structure

```
your_project/
├── app.py                  ← Flask backend (NEW)
├── main_pipeline.py        ← your existing pipeline (unchanged)
├── templates/
│   └── index.html          ← UI template (NEW)
├── static/
│   └── style.css           ← Styles (NEW)
├── uploads/                ← auto-created, temp image storage
└── ... (rest of your project)
```

## Setup & Run

```bash
# 1. Install Flask (if not already installed)
pip install flask

# 2. Place app.py in the same directory as main_pipeline.py
# 3. Create templates/ and static/ folders alongside app.py
# 4. Copy index.html into templates/, style.css into static/

# 5. Run the server
python app.py
```

Then open: **http://localhost:5000**

---

## How the UI maps to your pipeline

| UI Section | What it shows |
|---|---|
| Section 1 — Input Preview | Uploaded image, selected mode, active constraints |
| Section 2 — Generation Process | Each attempt card: story text, score bar, failure type, constraints |
| Section 3 — Final Result | ACCEPT / REJECT badge, final score, total attempts, last failure reason |

---

## Extending the trace

Your current `Pipeline.run()` doesn't populate a `trace` list in its return value.
The UI handles this gracefully — it builds a single-entry trace from the top-level
result keys (`final_score`, `failure_type`, `attempts`).

To get full per-attempt trace cards, add this to `Pipeline.run()`:

```python
# At the top of run():
trace = []

# After STEP 8 (failure_type is known), before STEP 9:
trace.append({
    "attempt": retry_count,
    "story":   story,
    "score":   final_score,
    "failure": failure_type,
    "constraints": data["constraints"]["negative_rules"],
    "scores":  scores,
})

# In the ACCEPT return:
return {
    "decision":    "ACCEPT",
    "final_score": final_score,
    "final_story": story,        # ← add this too
    "scores":      scores,
    "attempts":    retry_count,
    "trace":       trace,        # ← add this
}

# In all REJECT returns:
return {
    "decision":    "REJECT",
    "failure_type": failure_type,
    "attempts":    retry_count,
    "trace":       trace,        # ← add this
}
```

---

## Constraint checkbox → backend mapping

| Checkbox | Sent to backend as |
|---|---|
| No New Entities | `NO_NEW_ENTITIES` |
| No Off-Image Locations | `NO_OFF_IMAGE_LOCATIONS` |
| Keep Story Short | `KEEP_STORY_SHORT` |

These are collected in `app.py` and available via `user_constraints` in the
response JSON. Wire them into `input_data["constraints"]["negative_rules"]`
inside `run_full_pipeline()` when you're ready.

---

## Debug Mode

Select **Debug Mode** in the dropdown to skip CLIP + BLIP and run with a
random embedding and a hardcoded caption. Useful for testing the UI and
validation logic without GPU.
