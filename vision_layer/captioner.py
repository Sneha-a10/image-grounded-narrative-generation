from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageCaptioner:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)

    def generate_caption(self, image_path: str):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=30)

        caption = self.processor.decode(output[0], skip_special_tokens=True)

        return caption