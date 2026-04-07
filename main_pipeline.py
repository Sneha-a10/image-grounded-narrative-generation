from validation_layer.input_validator.validator import InputValidator
from validation_layer.preprocessing.preprocessor import StoryPreprocessor

from validation_layer.scorers.caption_scorer import CaptionStoryScorer
from validation_layer.scorers.image_scorer import ImageStoryScorer
from validation_layer.scorers.signal_scorer import SignalConsistencyEvaluator

from validation_layer.scoring_pipeline.normalizer import ScoreNormalizer
from validation_layer.scoring_pipeline.aggregator import ScoreAggregator
from validation_layer.scoring_pipeline.decision_engine import DecisionEngine

from validation_layer.constraint_check.constraint_checker import ConstraintChecker
from validation_layer.failure.failure_classifier import FailureClassifier

from regeneration_controller.controller import RegenerationController


class Pipeline:

    def __init__(self, preset_family, user_negative_prompts=None):
        self.validator = InputValidator()
        self.preprocessor = StoryPreprocessor()

        self.caption_scorer = CaptionStoryScorer()
        self.image_scorer = ImageStoryScorer()
        self.signal_scorer = SignalConsistencyEvaluator()

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
            story
        )

        signal_score = self.signal_scorer.evaluate(
            data["signal_extraction"]["semantic_signals"],
            data["signal_extraction"]["semantic_signals"]  # TEMP (same for now)
        )

        # STEP 4: Normalize
        scores = self.normalizer.normalize(
            image_score,
            caption_score,
            signal_score
        )

        # STEP 5: Aggregate
        final_score = self.aggregator.aggregate(scores)

        # STEP 6: Constraint Check
        constraint_result = self.constraint_checker.check(
            story,
            data["signal_extraction"]["semantic_signals"]["subjects"],
            data["signal_extraction"]["semantic_signals"]["subjects"],
            data["constraints"]["negative_rules"]
        )

        # STEP 7: Decision
        if constraint_result["violation"]:
            decision = "REJECT"
        else:
            decision = self.decision_engine.decide(final_score, scores)

        # STEP 8: Failure Type
        failure_type = None
        if decision == "REJECT":
            failure_type = self.failure_classifier.classify(
                scores,
                constraint_result["violation"]
            )

        # STEP 9: Route
        if decision == "ACCEPT":
            return {
                "decision": "ACCEPT",
                "final_score": final_score,
                "scores": scores
            }

        # STEP 10: Regeneration
        regen_result = self.regen.handle_rejection(failure_type)

        return {
            "decision": "REJECT",
            "failure_type": failure_type,
            "regen": regen_result
        }
