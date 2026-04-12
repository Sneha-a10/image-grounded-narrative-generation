import os
import sys
import uuid
import json
import traceback
from flask import Flask, request, jsonify, render_template

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# ── Make sure your project root is on the path ──────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from main_pipeline import run_full_pipeline          # your existing function

# ── Flask setup ──────────────────────────────────────────────────────────────
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Constraint label → internal rule mapping ─────────────────────────────────
CONSTRAINT_MAP = {
    "no_new_entities":        "NO_NEW_ENTITIES",
    "no_off_image_locations": "NO_OFF_IMAGE_LOCATIONS",
    "keep_story_short":       "KEEP_STORY_SHORT",   # backend may ignore; UI still sends it
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run():
    # ── 1. Validate image ────────────────────────────────────────────────────
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img_file = request.files["image"]
    if img_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    ext = os.path.splitext(img_file.filename)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png"):
        return jsonify({"error": "Only JPG/PNG images are accepted"}), 400

    # ── 2. Save image temporarily ────────────────────────────────────────────
    unique_name = f"{uuid.uuid4().hex}{ext}"
    image_path  = os.path.join(UPLOAD_FOLDER, unique_name)
    img_file.save(image_path)

    # ── 3. Read form params ──────────────────────────────────────────────────
    mode        = request.form.get("mode", "real")           # "real" | "debug"
    raw_checks  = request.form.getlist("constraints")        # list of checkbox values

    user_constraints = [CONSTRAINT_MAP[c] for c in raw_checks if c in CONSTRAINT_MAP]

    # ── 4. Run pipeline ──────────────────────────────────────────────────────
    try:
        raw_result = run_full_pipeline(image_path, mode=mode)
    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": str(exc)}), 500
    finally:
        # Always clean up temp image
        try:
            os.remove(image_path)
        except OSError:
            pass

    # ── 5. Normalise result to the shape the UI expects ──────────────────────
    #
    # Your Pipeline.run() returns different shapes depending on path:
    #   ACCEPT → { decision, final_score, scores, attempts }
    #   REJECT → { decision, failure_type, attempts }          (no story)
    #   error  → { error, ... }
    #
    # run_full_pipeline() itself may also return:
    #   { decision: "REJECT", reason: "..." }
    #
    # We harmonise everything so the frontend always gets the same contract.
    # ─────────────────────────────────────────────────────────────────────────

    if "error" in raw_result:
        return jsonify({"error": raw_result["error"]}), 500

    decision    = raw_result.get("decision", "REJECT")
    final_score = raw_result.get("final_score", 0.0)
    attempts    = raw_result.get("attempts",    0)
    final_story = raw_result.get("final_story", "")   # present only if caller sets it
    failure     = raw_result.get("failure_type") or raw_result.get("reason") or None
    trace       = raw_result.get("trace", [])         # may be empty; we build a minimal one
    scores      = raw_result.get("scores", {})

    # Build a minimal trace entry from what we know if the pipeline didn't
    # expose a full trace (your current Pipeline.run() doesn't fill "trace").
    # This keeps the UI working even before you wire up trace collection.
    if not trace:
        entry = {
            "attempt":     attempts,
            "story":       final_story or "(no story returned)",
            "score":       final_score,
            "failure":     failure if decision == "REJECT" else None,
            "constraints": user_constraints,
            "scores":      scores,
        }
        trace = [entry]

    response = {
        "decision":    decision,
        "final_score": round(float(final_score), 4),
        "final_story": final_story,
        "attempts":    attempts,
        "failure":     failure,
        "trace":       trace,
        "user_constraints": user_constraints,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)