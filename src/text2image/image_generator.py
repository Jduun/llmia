from abc import ABC, abstractmethod


class ImageGenerator(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str) -> str:
        pass
