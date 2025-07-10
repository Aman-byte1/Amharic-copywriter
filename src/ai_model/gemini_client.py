import google.generativeai as genai
from google.genai import types # Import types for GenerateImagesConfig
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv() # Load environment variables from .env

class GeminiClient:
    def __init__(self, text_model_name="gemini-pro", image_model_name="imagen-4.0-generate-preview-06-06"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")
        genai.configure(api_key=self.api_key)

        self.text_model = genai.GenerativeModel(text_model_name)
        self.image_model_name = image_model_name # Store model name for image generation

    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generates text content using the Gemini text model.
        """
        try:
            response = self.text_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating text content: {e}"

    def generate_image(self, prompt: str, number_of_images: int = 1, aspect_ratio: str = "1:1") -> list[Image.Image]:
        """
        Generates images using the specified Imagen model.

        Args:
            prompt (str): The descriptive prompt for the image.
            number_of_images (int): Number of images to generate (1 to 4 for Imagen, 1 for Ultra).
            aspect_ratio (str): Aspect ratio of the image ("1:1", "3:4", "4:3", "9:16", "16:9").

        Returns:
            list[PIL.Image.Image]: A list of generated PIL Image objects.
        """
        if not (1 <= number_of_images <= 4):
            raise ValueError("number_of_images must be between 1 and 4 for Imagen models.")
        if self.image_model_name == "imagen-4.0-ultra-generate-preview-06-06" and number_of_images > 1:
            # Imagen 4 Ultra only generates one image at a time
            number_of_images = 1

        try:
            # Use client.models.generate_images for Imagen models
            # Note: For Imagen, you usually create a client without specifying a model in init,
            # and then specify the model in the generate_images call.
            # Let's adjust the __init__ to reflect this, or ensure genai.Client() is accessible.
            # For simplicity, we'll instantiate genai.Client() directly in the method.
            # In a larger app, you might pass genai.Client() as an argument or make it a class attribute.
            client = genai.Client(api_key=self.api_key) # Re-instantiate if necessary, or make it a class-level client if it doesn't cause issues

            response = client.models.generate_images(
                model=self.image_model_name,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                    # person_generation="allow_adult" # Default, or set "allow_all" based on requirements/region
                )
            )

            generated_images = []
            for generated_image_part in response.generated_images:
                # The generated_image_part object contains a .image attribute which is a PIL.Image
                generated_images.append(generated_image_part.image)
            return generated_images

        except Exception as e:
            st.error(f"Error generating image: {e}") # Use st.error here for Streamlit context
            return []

# No direct __main__ block for image generation here, as it requires specific prompt context
# from the app.py to be meaningful.