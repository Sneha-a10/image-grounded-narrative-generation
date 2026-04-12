# GenAI Report: Controlled Multimodal Story Generation with Alignment Validation

## 2. Abstract
The project "Controlled Multimodal Story Generation with Alignment Validation" presents an academic demonstration and flexible pipeline that integrates computer vision models and large language models (LLMs) to automatically generate narratives grounded in visual inputs. To address common failure modes in Generative AI—such as hallucination, incoherence, and a lack of visual grounding—this system employs a rigid alignment validation architecture. Using vision-language models like CLIP and BLIP alongside NLP toolkits like spaCy, the system extracts semantic signals from input images and uses them to guide a local LLM (Mistral via Ollama). Furthermore, the pipeline utilizes post-generation gatekeeping to dynamically score and regenerate narratives that drift from the source visual truth. Finally, the validated and accepted story string passes into a Text-to-Speech generation layer to output a spoken audio file. The result is a highly modular system capable of ensuring structural and semantic fidelity in automated story generation and multimedia expansion.

## 3. Keywords
Generative AI, Multimodal Story Generation, Alignment Validation, Vision-Language Models, Hallucination Mitigation, Prompt Engineering.

## 4. Introduction
The rapid advancement of Generative AI has enabled the production of highly coherent text, but combining multi-modal inputs—such as image-to-story generation—remains a complex challenge. A significant issue in modern LLM applications is their tendency to "hallucinate" or generate details that contradict the source data. When given an image, language models often fail to structurally ground their narrative to the exact factual subjects and actions depicted, leading to incoherence or stylistic drift. This project is motivated by the need to enforce factual and semantic grounding within multimodal story generation. By integrating proactive constraint generation, feature extraction, and mathematical alignment validation, this system seeks to strictly control the generative capabilities of an LLM, ensuring that every produced narrative remains faithfully rooted to its visual origin.

## 5. Problem Statement
Existing multimodal generative systems frequently suffer from unconstrained hallucination and a lack of grounding, whereby the generated text drifts from the actual subjects, environments, and semantics presented in the source image. This project aims to solve this alignment issue by developing a controlled, closed-loop pipeline that not only guides story generation using extracted visual data but also formally validates the final output against those visual signals, systematically rejecting and regenerating outputs that violate structural or semantic constraints.

## 6. Objectives
- Extract accurate, robust semantic signals and feature embeddings from raw image data.
- Translate visual realities into structured prompts used to strictly control narrative generation.
- Implement a rigid alignment validation system that scores texts on global similarity, semantic matching, and hallucination rates.
- Establish a "Regeneration Controller" that proactively modifies generation constraints upon detecting validation failures, autonomously reprompting the LLM until thresholds are met.
- Provide a highly modular, extendable architecture separating the vision extraction layer from the local text generation and scoring layers.
- Synthesize an audio reading of the final accepted story using a fully integrated Text-to-Speech (Voice) generation layer.

## 8. System Architecture / Design
The system features a highly modular architecture segmented into discrete processing layers that execute sequentially. The primary orchestrator is the `Pipeline` class residing in the main event script.

**Major Components:**
- **Vision Layer:** Processes raw images to extract structured embeddings and textual descriptions.
- **Signal Extraction Layer:** Parses textual descriptions into discrete semantic signals (e.g., subjects, objects, environment, action state).
- **Language Layer:** Utilizes the extracted signals to formulate constraint-bound prompts, feeding them to a local LLM to generate the initial narrative.
- **Validation Layer:** Performs strict validation and scoring operations. It encompasses:
  - Input Validator and Story Preprocessor.
  - Image, Caption, and Signal Scorers.
  - Constraint Checkers to verify token/entity presence.
  - Score Normalizer and Aggregator.
- **Regeneration Controller / Decision Engine:** Evaluates the aggregated scores against fixed thresholds. If the narrative fails, it determines a `failure_type` and instructs the system to dynamically adjust the constraints and regenerate the text.
- **Voice Generation Layer:** Triggers upon final acceptance of a story, translating the final verified text string into a synthesized speech audio file.

**Data Flow Sequence Block Diagram Pattern:**
`[Input Image] -> [Vision Layer (CLIP & BLIP)] -> (Embeddings & Captions) -> [Signal Extraction (spaCy)] -> [Language Layer (Mistral LLM)] -> [Initial Generated Story] -> [Validation & Scoring Layer] -> (Accept / Reject) -> [Regeneration Controller] (Feedback loop back to Language Layer) -> [Voice Layer (TTS)] -> (Final Audio File)`

## 9. Tools, Technologies, and Data Sources
- **Programming Language:** Python (v3.11.9)
- **Deep Learning & Vision:** PyTorch, HuggingFace Transformers (`openai/clip-vit-base-patch32` for image embedding, `Salesforce/blip-image-captioning-base` for captioning).
- **Natural Language Processing (NLP):** `spaCy` (en_core_web_sm), `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Language Model Inference:** Local inference engine via `ollama` utilizing the `mistral` model.
- **Support Libraries:** `scikit-learn`, `pillow`, `pytest`, `pydantic`.
- **Frontend / Application interface:** Flask (handling web requests routing to the backend pipeline).
- **Data Sources:** Extracts from the `steubk/wikiart` dataset via Kagglehub, sequentially processing subjects like the "Baroque" sub-category.

## 10. Methodology / Workflow
1. **Vision Preprocessing:** An input image is parsed by CLIP to generate a high-dimensional numerical embedding vector and by BLIP to generate a strict, factual caption.
2. **Signal Extraction:** The factual caption is passed through a spaCy-based pipeline to separate nouns, verbs, and contexts into mapped components (subject, objects, environment, actions, emotion hint).
3. **First Generation Pass:** The signals and base constraints are concatenated as structured text directives inside a system prompt. The Language Layer outputs an initial short story.
4. **Preprocessing & Alignment Scoring:** The resulting text is sanitized and then algorithmically graded:
   - Text-to-Image similarity is evaluated via similarity functions acting against the embeddings.
   - Text-to-Text similarity (Semantic Match) runs against the factual caption.
   - A hallucination rate is explicitly deducted by hunting for missing or fabricated subjects via lemma analysis.
5. **Decision Making:** The scores are normalized and aggregated into a final metric. The Decision Engine checks for absolute constraint violations and compares the final score against a fixed threshold (e.g., Final Score >= 0.6).
6. **Controlled Regeneration:** If the output passes, the loops terminates and returns the validated result. If it fails, the Regeneration Controller explicitly identifies the failure sub-type (e.g., image vs text misalignment) and pushes tighter `negative_rules` (e.g., `NO_NEW_ENTITIES`, `NO_OFF_IMAGE_LOCATIONS`) back to the prompt generation stage. This executes iteratively up to a defined maximum retry limit.
7. **Audio Synthesis (Voice Layer):** After the pipeline successfully accepts a narrative that breaks no constraints and passes all score thresholds, the final story string is passed to the Voice Generation Layer, which processes the text-to-speech (TTS) conversion and generates a playable audio file for the user.

## 11. Implementation
The system is constructed as a rigorous, decoupled Python package executed sequentially. It was initially designed to process batched, chunked JSON outputs created offline by a notebook in the `vision_layer` running on GPUs (like Colab), which passes payload dictionaries containing embeddings and captions into the main local sequence.

Locally, the application (`app.py`) wraps `main_pipeline.py` and manages asynchronous requests via a Web UI or programmatic imports. During execution, it automatically loads instances of `VisionEncoder` and `ImageCaptioner`. Within the loop, internal sub-modules like `validation_layer/scorers/image_scorer.py` instantiate textual variants of `CLIPModel` to perform on-the-fly cosine similarity validation of the story's embeddings against the image. Rather than blindly trusting prompt engineering, the implementation hinges heavily upon deterministic, programmatic fact-checking tools (`spaCy` matching, `sentence-transformers`) to act as rigid gatekeepers over the `ollama` outputs, allowing the pipeline to autonomously heal broken model generations.
