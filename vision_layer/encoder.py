# ============================================
# VISION ENCODER MODULE (FINALIZED)
# --------------------------------------------
# - Uses CLIP (openai/clip-vit-base-patch32)
# - Outputs 512-dim embedding
# - Aligned with validation layer
#
# DO NOT MODIFY unless:
# - validation model changes
# - embedding space changes
# ============================================

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


class VisionEncoder:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def encode(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.vision_model(**inputs)

            pooled_output = outputs.last_hidden_state[:, 0, :]  # shape (1, 768)

            image_features = self.model.visual_projection(pooled_output)  # → (1, 512)

        return image_features[0].cpu().numpy()