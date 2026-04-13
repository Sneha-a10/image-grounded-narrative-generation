import os
import sys

# Ensure all layer modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validation_layer.input_validator.validator import InputValidator
from validation_layer.preprocessing.preprocessor import StoryPreprocessor

from validation_layer.scorers.caption_scorer import CaptionStoryScorer
from validation_layer.scorers.image_scorer import ImageStoryScorer
from validation_layer.scorers.signal_scorer import SignalConsistencyScorer

from validation_layer.scoring_pipeline.normalizer import ScoreNormalizer
from validation_layer.scoring_pipeline.aggregator import ScoreAggregator
from validation_layer.scoring_pipeline.decision_engine import DecisionEngine

from validation_layer.constraint_check.constraint_checker import ConstraintChecker
from validation_layer.failure.failure_classifier import FailureClassifier
 
from regeneration_controller.controller import RegenerationController

from vision_layer.encoder import VisionEncoder
from vision_layer.captioner import ImageCaptioner
from signal_extraction.extractor import SignalExtractor
from language_layer.language_layer_main import language_layer_pipeline

from constraint_generation.constraint_generation import generate_constraints
from tts import generate_audio

# ---- GLOBAL SINGLETONS ----
_SHARED_ENCODER = None
_SHARED_CAPTIONER = None

class Pipeline:

    def __init__(self, preset_family, user_negative_prompts=None):
        self.validator = InputValidator()
        self.preprocessor = StoryPreprocessor()

        self.caption_scorer = CaptionStoryScorer()
        self.image_scorer = ImageStoryScorer()
        self.signal_scorer = SignalConsistencyScorer()

        self.normalizer = ScoreNormalizer()
        self.aggregator = ScoreAggregator()
        self.decision_engine = DecisionEngine()

        self.constraint_checker = ConstraintChecker()
        self.failure_classifier = FailureClassifier()

        self.regen = RegenerationController(
            preset_family,
            user_negative_prompts
        )

    def run(self, data, status_cb=None, abort_check_cb=None):

        retry_count = 0
        best_score = -1.0
        best_story = ""

        while True:
            if abort_check_cb and abort_check_cb():
                print("🛑 [ABORT] Pipeline stopped by user.")
                return {"decision": "ABORTED", "reason": "user_aborted", "best_score_overall": best_score, "best_story_overall": best_story}

            if status_cb: status_cb(4, f"Validating · Attempt {retry_count}")
            print(f"\n{'='*50}")
            print(f"🔄 STARTING EVALUATION LOOP | ATTEMPT {retry_count}")
            print(f"{'='*50}")

            caption_text = data["caption_data"]["caption_text"]
            signals = data["signal_extraction"]["semantic_signals"]
            print(f"\n📝 INITIAL CAPTION: {caption_text}")
            
            print("🎯 DETECTED ELEMENTS:")
            print(f"   - Subjects:    {', '.join(signals.get('subjects', [])) or 'none'}")
            print(f"   - Objects:     {', '.join(signals.get('objects', [])) or 'none'}")
            print(f"   - Environment: {', '.join(signals.get('environment', [])) or 'none'}")
            print(f"   - Actions:     {', '.join(signals.get('actions', [])) or 'none'}")
            print(f"   - Attributes:  {', '.join(signals.get('attributes', [])) or 'none'}")

            print("\n⏳ [STEP 1] Validating input structure...")
            # STEP 1: Validate input
            if not self.validator.validate(data):
                print("❌ Invalid input data structure!")
                return {"error": "Invalid input"}

            story = data["generation_output"]["story_text"]
            print(f"\n📖 CURRENT STORY TO EVALUATE:\n{story}\n")

            # STEP 2: Preprocess
            processed = self.preprocessor.process(story)

            print("⏳ [STEP 3] Running Scorers (Caption, Image, Signal)...")
            # STEP 3: Scores
            caption_score = self.caption_scorer.score(
                data["caption_data"]["caption_text"],
                story
            )

            image_score = self.image_scorer.score(
                data["visual_features"]["embedding_vector"],
                story,
                data["signal_extraction"]["semantic_signals"]
            )

            signal_score = self.signal_scorer.score(
                data["signal_extraction"]["semantic_signals"],
                story
            )

            # STEP 4: Normalize
            scores = self.normalizer.normalize(
                image_score,
                caption_score,
                signal_score
            )

            # STEP 5: Aggregate
            final_score = self.aggregator.aggregate(
                scores["image_score"],
                scores["caption_score"],
                scores["signal_score"]
            )

            if final_score > best_score:
                best_score = final_score
                best_story = story

            print("\n📊 EVALUATION SCORES:")
            print(f"   - Caption alignment: {scores['caption_score']:.4f}")
            print(f"   - Image alignment:   {scores['image_score']:.4f}")
            print(f"   - Signal alignment:  {scores['signal_score']:.4f}")
            print(f"   => FINAL AGGREGATE SCORE: {final_score:.4f}\n")

            print("⏳ [STEP 6] Checking Structural Constraints...")
            # STEP 6: Constraint Check
            expected_subjects = data["signal_extraction"]["semantic_signals"]["subjects"]

            # 🔴 EXTRACT SUBJECTS FROM STORY (simple version)
            story_words = story.lower().split()
            actual_subjects = [word for word in story_words if word in expected_subjects]

            constraint_result = self.constraint_checker.check(
                story,
                expected_subjects,
                actual_subjects,
                data["constraints"]["negative_rules"]
            )
            if constraint_result['violation']:
                print(f"   - ⚠️  Constraint violation detected: {constraint_result['violation']}")

            # STEP 7: Decision
            if constraint_result["violation"]:
                decision = "NOT_ALIGNED"
            else:
                raw_decision = self.decision_engine.decide(
                    scores["image_score"],
                    scores["caption_score"],
                    scores["signal_score"],
                    final_score
                )
                decision = "ACCEPT" if raw_decision == "ACCEPT" else "NOT_ALIGNED"

            print(f"\n⚖️  FINAL PIPELINE DECISION: {decision}")
            if status_cb: status_cb(5, f"Decision: {decision}")

            # STEP 8: Mismatch Type
            failure_type = None
            if decision == "NOT_ALIGNED":
                failure_type = self.failure_classifier.classify(
                    scores["image_score"],
                    scores["caption_score"],
                    scores["signal_score"],
                    final_score
                )
                print(f"⚠️  VALIDATION MISMATCH: {failure_type}\n")

            # STEP 9: ACCEPT → EXIT
            if decision == "ACCEPT":
                print(f"🎉 SUCCESS! Story accepted on attempt {retry_count}.")
                return {
                    "decision": "ACCEPT",
                    "final_score": final_score,
                    "final_story": story,
                    "scores": scores,
                    "attempts": retry_count,
                    "best_score_overall": best_score,
                    "best_story_overall": best_story
                }

            # STEP 10: NOT_ALIGNED → HANDLE REGEN
            if abort_check_cb and abort_check_cb():
                return {"decision": "ABORTED", "reason": "user_aborted", "best_score_overall": best_score, "best_story_overall": best_story}
            
            # Map NOT_ALIGNED back to REJECT for internal controller logic if needed, 
            # but keep it clean here.
            regen_result = self.regen.handle_rejection(failure_type)

            print(f"🔄 PREPARING FOR RETRY {retry_count + 1}...")

            if regen_result["action"] != "RETRY":
                print("🛑 [STOP] Controller stopped retries (Threshold reached)")
                return {
                    "decision": "NOT_ALIGNED",
                    "failure_type": failure_type,
                    "attempts": retry_count,
                    "best_score_overall": best_score,
                    "best_story_overall": best_story
                }

            retry_count = regen_result["constraint_input"]["retry_count"]

            constraint_input = regen_result["constraint_input"]
            raw_fail = constraint_input["failure_type"]
            mapped_fail = None
            if raw_fail == "image_misalignment":
                mapped_fail = "image"
            elif raw_fail in ["caption_misalignment", "signal_violation"]:
                mapped_fail = "text"
            elif raw_fail == "multi_failure":
                mapped_fail = "both"

            payload = {
                "experiment_mode": constraint_input["experiment_mode"],
                "retry_count": constraint_input["retry_count"],
                "failure_type": mapped_fail
            }
            constraint_output = generate_constraints(payload)
            
            allowed_rules = {
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS",
                "NO_TEMPORAL_JUMPS",
                "NO_REFLECTIVE_LANGUAGE"
            }

            filtered_rules = [
                rule for rule in constraint_output["constraints"]["negative_rules"]
                if rule in allowed_rules
            ]

            data["constraints"]["negative_rules"] = filtered_rules

            # -------------------------
            # 🚨 CRITICAL PART (MISSING)
            # -------------------------
            # 🔴 ADD THIS EXACTLY HERE

            sem_sig = data["signal_extraction"]["semantic_signals"]
            mapped_signals = {
                "subject": sem_sig["subjects"][0] if sem_sig.get("subjects") else None,
                "objects": sem_sig.get("objects", []),
                "environment": sem_sig.get("environment", []),
                "action_state": sem_sig["actions"][0] if sem_sig.get("actions") else None,
                "emotion_hint": sem_sig.get("emotion_hint"),
                "attributes": sem_sig.get("attributes", [])
            }

            regen_input = {
                "image_id": data["image_id"],
                "caption": data["caption_data"]["caption_text"],
                "signals": mapped_signals,
                "constraints": {
                    "max_length": 120,
                    "tone": "neutral",
                    "perspective": "third_person",
                    "allowed_emotion_inference": "limited",
                    "negative_rules": data["constraints"]["negative_rules"]
                }
            }

            new_story_output = language_layer_pipeline(regen_input)

            # ---- SAFE EXTRACTION ----
            if "story_text" in new_story_output:
                story_text = new_story_output["story_text"]
            elif "text" in new_story_output:
                story_text = new_story_output["text"]
            elif "story" in new_story_output:
                story_text = new_story_output["story"]
            else:
                print("[CONSTRAINT VIOLATION] Unknown language layer output format:", new_story_output)
                return {
                    "decision": "NOT_ALIGNED",
                    "reason": "generation_failed",
                    "attempts": retry_count
                }

            print(f"[NEW STORY - Attempt {retry_count}] {story_text}")

            # ---- UPDATE DATA FOR NEXT LOOP ----
            data["generation_output"]["story_text"] = story_text
            data["generation_output"]["sentences"] = [story_text]
            data["generation_output"]["word_count"] = len(story_text.split())

            # -------------------------
            # LOOP CONTINUES
            # -------------------------

            if retry_count > 2:
                print("[STOP] Max retries reached")
                return {
                    "decision": "NOT_ALIGNED",
                    "failure_type": failure_type,
                    "attempts": retry_count,
                    "best_score_overall": best_score,
                    "best_story_overall": best_story
                }

def adapt_to_validation_format(caption, embedding, signals, story_output):
    return {
        "image_id": "test_img",

        "caption_data": {
            "caption_text": caption
        },

        "visual_features": {
            "embedding_vector": embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        },

        "generation_output": {
            "story_text": story_output["story_text"],
            "sentences": [story_output["story_text"]],
            "word_count": len(story_output["story_text"].split())
        },

        "signal_extraction": {
            "semantic_signals": {
                "subjects": [signals.get("subject")] if signals.get("subject") else [],
                "objects": signals.get("objects", []),
                "environment": signals.get("environment", []),
                "actions": signals.get("actions", []),
                "attributes": signals.get("attributes", []),
                "emotion_hint": signals.get("emotion_hint")
            }
        },

        "constraints": {
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }


def run_full_pipeline(image_path: str, mode="real", preset="Neutral_Descriptive", user_caption=None, status_cb=None, abort_check_cb=None):
    """
    mode:
    - "debug" → fast (random embedding, skips heavy models)
    - "real"  → full system (CLIP + BLIP + signals)
    """
    def notify(step_idx, text):
        if status_cb: status_cb(step_idx, text)
        print(text)
        
    def check_abort():
        if abort_check_cb and abort_check_cb():
            print("🛑 [ABORT] Pipeline stopped by user.")
            return True
        return False

    import random

    notify(0, f"\n🚀 RUNNING MODE: {mode.upper()}\n")

    # -------------------------
    # 🔴 MODE 1: DEBUG (FAST)
    # -------------------------
    if mode == "debug":

        if user_caption:
            caption = user_caption
        else:
            caption = "A dog playing with a ball in a park"

        signals = {
            "subject": "dog",
            "objects": ["ball"],
            "environment": ["park"],
            "action_state": "playing",
            "emotion_hint": "happy"
        }

        embedding = [random.uniform(-1, 1) for _ in range(512)]

        print("DEBUG CAPTION:", caption)
        print("DEBUG SIGNALS:", signals)

    # -------------------------
    # 🟢 MODE 2: REAL SYSTEM
    # -------------------------
    else:
        # 1. Vision (CLIP)
        global _SHARED_ENCODER, _SHARED_CAPTIONER

        if _SHARED_ENCODER is None:
            _SHARED_ENCODER = VisionEncoder()

        if _SHARED_CAPTIONER is None:
            _SHARED_CAPTIONER = ImageCaptioner()

        encoder = _SHARED_ENCODER
        captioner = _SHARED_CAPTIONER 

        notify(0, "Encoding image...")
        embedding = encoder.encode(image_path)
        print("EMBEDDING:", len(embedding))

        if check_abort(): return {"decision": "ABORTED", "reason": "user_aborted"}

        # 2. Caption (BLIP)
        notify(1, "Generating/Fetching caption...")
        if user_caption:
            caption = user_caption
        else:
            caption = captioner.generate_caption(image_path)
        print("CAPTION:", caption)

        if check_abort(): return {"decision": "ABORTED", "reason": "user_aborted"}

        # 3. Signals
        notify(2, "Extracting semantic signals...")
        extractor = SignalExtractor()
        signals = extractor.extract(caption)
        print("SIGNALS:", signals)

    # -------------------------
    # 🔴 LANGUAGE LAYER INPUT
    # -------------------------
    input_data = {
        "image_id": "test_img",
        "caption": caption,
        "signals": signals,
        "constraints": {
            "max_length": 120,
            "tone": "neutral",
            "perspective": "third_person",
            "allowed_emotion_inference": "limited",
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }

    # Free memory before calling Ollama
    if "encoder" in locals():
        del encoder
    if "captioner" in locals():
        del captioner
    import gc
    gc.collect()
    import torch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if check_abort(): return {"decision": "ABORTED", "reason": "user_aborted", "caption": caption}

    # 4. Generate story
    notify(3, "Weaving narrative...")
    story_output = language_layer_pipeline(input_data)

    print("\n🧠 GENERATED STORY:")
    print(story_output)

    if "error" in story_output:
        print("❌ Language layer encountered a constraint violation")
        return {"decision": "NOT_ALIGNED", "reason": "generation_failed"}

    # -------------------------
    # 🔴 ADAPT FOR VALIDATION
    # -------------------------
    validation_input = adapt_to_validation_format(
        caption,
        embedding,
        signals,
        story_output
    )

    # -------------------------
    # 🔴 RUN PIPELINE
    # -------------------------
    if check_abort(): return {"decision": "ABORTED", "reason": "user_aborted", "caption": caption}

    pipeline = Pipeline(preset)
    result = pipeline.run(validation_input, status_cb=status_cb, abort_check_cb=abort_check_cb)
    result["caption"] = caption
    result["raw_signals"] = signals

    # ---- GENERATE FINAL AUDIO ----
    story_to_read = result.get("final_story") or result.get("best_story_overall")
    if story_to_read:
        notify(4, "Generating audio from the final story...")
        try:
            audio_path = generate_audio(story_to_read)
            result["audio_path"] = audio_path
            notify(5, f"Audio saved to: {audio_path}")
        except Exception as e:
            notify(5, f"Warning: Could not generate audio - {e}")

    print("\n✅ FINAL RESULT:")
    print(result)

    return result


if __name__ == "__main__":
    result = run_full_pipeline("test.png")
    print("\nFINAL OUTPUT:\n", result)