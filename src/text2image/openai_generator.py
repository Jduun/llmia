from openai import OpenAI

from src.text2image.image_generator import ImageGenerator

client = OpenAI()


class OpenAIImageGenerator(ImageGenerator):
    async def generate_image(self, prompt: str) -> str:
        response = await client.images.async_generate(
            model="dall-e-3",
            prompt=prompt,
            size="768x768",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
