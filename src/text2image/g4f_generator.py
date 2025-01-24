from g4f.client import Client

from src.text2image.image_generator import ImageGenerator

client = Client()


class G4FImageGenerator(ImageGenerator):
    async def generate_image(self, prompt: str) -> str:
        response = await client.images.async_generate(
            model="flux",
            prompt=prompt,
            response_format="url",
            cookies={
                "_U": "cookie value",
            },
        )
        image_url = response.data[0].url
        return image_url
