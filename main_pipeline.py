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

    def run(self, data):

        retry_count = 0

        while True:

            # STEP 1: Validate input
            if not self.validator.validate(data):
                return {"error": "Invalid input"}

            story = data["generation_output"]["story_text"]

            # STEP 2: Preprocess
            processed = self.preprocessor.process(story)

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

            # STEP 7: Decision
            if constraint_result["violation"]:
                decision = "REJECT"
            else:
                decision = self.decision_engine.decide(
                    scores["image_score"],
                    scores["caption_score"],
                    scores["signal_score"],
                    final_score
                )

            # STEP 8: Failure Type
            failure_type = None
            if decision == "REJECT":
                failure_type = self.failure_classifier.classify(
                    scores["image_score"],
                    scores["caption_score"],
                    scores["signal_score"],
                    final_score
                )

            # STEP 9: ACCEPT → EXIT
            if decision == "ACCEPT":
                return {
                    "decision": "ACCEPT",
                    "final_score": final_score,
                    "scores": scores,
                    "attempts": retry_count
                }

            # STEP 10: REJECT → HANDLE REGEN
            regen_result = self.regen.handle_rejection(failure_type)

            print(f"[RETRY] Attempt {retry_count + 1} | Failure: {failure_type}")

            if regen_result["action"] != "RETRY":
                print("[STOP] Controller stopped retries")
                return {
                    "decision": "REJECT",
                    "failure_type": failure_type,
                    "attempts": retry_count
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
                "emotion_hint": sem_sig["attributes"][0] if sem_sig.get("attributes") else None
            }

            regen_input = {
                "image_id": data["image_id"],
                "caption": data["caption_data"]["caption_text"],
                "signals": mapped_signals,
                "constraints": {
                    "max_length": 100,
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
                print("[ERROR] Unknown language layer output format:", new_story_output)
                return {
                    "decision": "REJECT",
                    "reason": "invalid_generator_output",
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
                    "decision": "REJECT",
                    "failure_type": failure_type,
                    "attempts": retry_count
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
                "actions": [signals.get("action_state")] if signals.get("action_state") else [],
                "attributes": [signals.get("emotion_hint")] if signals.get("emotion_hint") else []
            }
        },

        "constraints": {
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }


def run_full_pipeline(image_path: str, mode="real"):
    """
    mode:
    - "debug" → fast (random embedding, skips heavy models)
    - "real"  → full system (CLIP + BLIP + signals)
    """

    import random

    print(f"\n🚀 RUNNING MODE: {mode.upper()}\n")

    # -------------------------
    # 🔴 MODE 1: DEBUG (FAST)
    # -------------------------
    if mode == "debug":

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
        encoder = VisionEncoder()
        embedding = encoder.encode(image_path)
        print("EMBEDDING:", len(embedding))

        # 2. Caption (BLIP)
        captioner = ImageCaptioner()
        caption = captioner.generate_caption(image_path)
        print("CAPTION:", caption)

        # 3. Signals
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
            "max_length": 100,
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

    # 4. Generate story
    story_output = language_layer_pipeline(input_data)

    print("\n🧠 GENERATED STORY:")
    print(story_output)

    if "error" in story_output:
        print("❌ Language layer failed")
        return {"decision": "REJECT", "reason": "generation_failed"}

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
    pipeline = Pipeline("Neutral_Descriptive")
    result = pipeline.run(validation_input)

    print("\n✅ FINAL RESULT:")
    print(result)

    return result

    image_path = "test.png"
    # 1. Vision (embedding)
    encoder = VisionEncoder()
    embedding = encoder.encode(image_path)

    print("EMBEDDING:", embedding.shape)

    # 2. Caption
    captioner = ImageCaptioner()
    caption = captioner.generate_caption(image_path)

    print("CAPTION:", caption)

    # 3. Signals
    extractor = SignalExtractor()
    signals = extractor.extract(caption)

    print("SIGNALS:", signals)

    # 4. Language Layer
    input_data = {
        "image_id": "test_img",
        "caption": caption,
        "signals": signals,
        "constraints": {
            "max_length": 100,
            "tone": "neutral",
            "perspective": "third_person",
            "allowed_emotion_inference": "limited",
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }

    story_output = language_layer_pipeline(input_data)

    print("STORY OUTPUT:", story_output)

    if "error" in story_output:
        print("Language layer failed:", story_output)

        return {
            "decision": "REJECT",
            "reason": "language_layer_failure"
        }

    # 5. Adapt to validation format
    validation_input = adapt_to_validation_format(
        caption,
        embedding,
        signals,
        story_output
    )

    # 6. Run validation pipeline
    pipeline = Pipeline("Neutral_Descriptive")
    result = pipeline.run(validation_input)

    print("FINAL RESULT:", result)

    return result

if __name__ == "__main__":
    result = run_full_pipeline("test.png")
    print("\nFINAL OUTPUT:\n", result)