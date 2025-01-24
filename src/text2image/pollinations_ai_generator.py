from urllib.parse import quote

from src.text2image.image_generator import ImageGenerator


class PollinationsAIGenerator(ImageGenerator):
    async def generate_image(self, prompt: str) -> str:
        image_url = f"https://pollinations.ai/p/{quote(prompt)}"
        return image_url
