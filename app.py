import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64 # Import base64 for handling inline_data if needed, though PIL can often directly open BytesIO
from io import BytesIO

# Load environment variables from .env file at the root of the project
load_dotenv()

# --- Gemini API Client Class ---
class GeminiClient:
    def __init__(self, text_model_name="gemini-2.0-flash", image_model_name="gemini-2.0-flash-preview-image-generation"):
        """
        Initializes the GeminiClient with specified text and image model names.
        Ensures the GOOGLE_API_KEY is loaded from environment variables.
        """
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")

        genai.configure(api_key=self.api_key)

        # Initialize the text generation model
        self.text_model = genai.GenerativeModel(text_model_name)
        
        # Initialize the image generation model (using the multimodal Gemini 2.0 Flash for images)
        self.image_model = genai.GenerativeModel(image_model_name)

    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generates text content using the configured Gemini text model.
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
        Generates images using the configured multimodal Gemini model (gemini-2.0-flash-preview-image-generation).

        Args:
            prompt (str): The descriptive prompt for the image.
            number_of_images (int): The number of images to generate.
                                    Note: gemini-2.0-flash-preview-image-generation may not strictly adhere
                                    to this or might generate a single image and text based on its multimodal nature.
                                    We'll process all images found in the response.
            aspect_ratio (str): Aspect ratio is not directly controllable via 'gemini-2.0-flash-preview-image-generation'
                                in the same way as dedicated Imagen models. The model will try to infer it from the prompt
                                or use a default. This parameter will be noted but not directly applied to the config.

        Returns:
            list[PIL.Image.Image]: A list of generated PIL Image objects. Returns an empty list if an error occurs.
        """
        # For gemini-2.0-flash-preview-image-generation, aspects like 'number_of_images' and 'aspect_ratio'
        # are often implicitly handled by the model's multimodal generation, or require prompt engineering.
        # Direct configuration for these isn't as granular as with dedicated Imagen models.
        # We will still pass the prompt that implies these desires.

        try:
            # The prompt is what drives the image generation for this model.
            # We explicitly ask for an image in the prompt for better results.
            image_generation_prompt = f"Please generate a photorealistic image based on this description: {prompt}"
            
            # If a specific number of images or aspect ratio is critical, you might try
            # adding it to the prompt, e.g., "Generate 2 square images of..."
            # However, direct config parameters for these are not available for this model variant.

            response = self.image_model.generate_content(
                contents=image_generation_prompt,
                generation_config=types.GenerationConfig(
                    # Crucially, tell the model to respond with both text AND image
                    response_modalities=['IMAGE'] 
                )
            )
            
            generated_images = []
            # Iterate through all parts of the response candidates to find images
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        # part.inline_data contains the image data
                        # PIL can open from BytesIO directly from base64 decoded data
                        image_data = base64.b64decode(part.inline_data.data)
                        image = Image.open(BytesIO(image_data))
                        generated_images.append(image)
                    elif part.text:
                        # You might want to display accompanying text if the model generates it
                        st.info(f"Model also provided text: {part.text}")
            
            # The 'number_of_images' parameter from the app UI is a request.
            # The model might return fewer or more, but we will show what it provides.
            # If you strictly need 'number_of_images' for this model, you'd need to
            # make multiple API calls or refine the prompt to ask for multiple images.
            # For this example, we'll just return all images found.

            return generated_images

        except Exception as e:
            st.error(f"Error generating image: {e}")
            return []

# The rest of your app.py code remains the same:
# --- Prompt Utility Functions ---
def get_marketing_prompt(content_type, product_name, product_description, target_audience, tone):
    """
    Constructs a detailed prompt for generating marketing text content.
    """
    prompt = f"You are an expert copywriter. Generate a {content_type} for the following product:\n\n"
    prompt += f"Product Name: {product_name}\n"
    prompt += f"Product Description/Key Features: {product_description}\n"
    prompt += f"Target Audience: {target_audience}\n"
    prompt += f"Desired Tone: {tone}\n\n"
    prompt += f"Please ensure the {content_type} is compelling and persuasive."

    # Add specific instructions based on the content type for better results
    if content_type == "Product Description":
        prompt += " Focus on benefits, unique selling points, and a clear call to action if applicable."
    elif content_type == "Ad Headline":
        prompt += " Make it short, attention-grabbing, impactful, and suitable for a digital ad banner."
    elif content_type == "Social Media Post":
        prompt += " Keep it concise, engaging, and include 2-3 relevant hashtags and emojis."
    elif content_type == "Email Subject Line":
        prompt += " Make it concise, intriguing, and designed to maximize email open rates. Suggest 3 variations."

    prompt += "\n\nGenerated Content:"
    return prompt

def get_image_prompt(product_name, product_description, target_audience, content_type, tone):
    """
    Constructs a detailed prompt for generating a related image.
    This prompt aims to guide the image generation model to create a visual
    that complements the marketing content.
    """
    # Start with a strong visual description of the product
    base_prompt = f"A photorealistic image of {product_name}. "
    base_prompt += f"The image should visually represent the core features of: {product_description}. "
    base_prompt += f"It is intended for a {target_audience} audience. "
    base_prompt += f"The overall mood and style should be {tone}. "

    # Add specific visual cues based on the content type
    if content_type == "Product Description":
        base_prompt += "Show the product in a clean, well-lit studio setting, highlighting its key features."
    elif content_type == "Ad Headline":
        base_prompt += "Create a dynamic and eye-catching visual that evokes curiosity and impact."
    elif content_type == "Social Media Post":
        base_prompt += "Make it vibrant and shareable, suitable for a social media feed. Focus on a lifestyle context."
    elif content_type == "Email Subject Line":
        base_prompt += "Generate a conceptual or abstract image that subtly hints at the product's benefits or purpose."

    # Add general quality modifiers for better image output
    base_prompt += "High quality, professional photography, studio lighting, detailed, vibrant colors."

    return base_prompt

# --- Streamlit Application UI ---
st.set_page_config(page_title="AI Copywriting Assistant", layout="wide", page_icon="✍️") # Corrected icon parameter

st.title("✍️ AI Copywriting Assistant")
st.markdown("Generate engaging marketing content and related visuals with the power of AI!")

# Initialize Gemini Client using Streamlit's cache_resource to prevent re-initialization on rerun
@st.cache_resource
def get_gemini_client_instance():
    """
    Caches the GeminiClient instance to avoid re-creating it on every Streamlit rerun.
    This is crucial for performance and API rate limits.
    """
    return GeminiClient()

gemini_client = get_gemini_client_instance()

# --- Input Section for Product Details ---
st.header("Product Details")
product_name = st.text_input("Product Name:", placeholder="e.g., 'GlowUp Vitamin C Serum'")
product_description = st.text_area(
    "Product Description/Key Features:",
    placeholder="e.g., 'Brightens skin, reduces dark spots, natural ingredients, vegan-friendly.'"
)
target_audience = st.text_input(
    "Target Audience:",
    placeholder="e.g., 'Women aged 25-45 interested in natural skincare.'"
)

# --- Content Generation Options ---
st.header("Content Generation Options")
col1, col2 = st.columns(2)
with col1:
    content_type = st.selectbox(
        "Type of Text Content to Generate:",
        ("Product Description", "Ad Headline", "Social Media Post", "Email Subject Line")
    )
with col2:
    tone = st.selectbox(
        "Desired Tone:",
        ("Professional", "Friendly", "Excited", "Luxurious", "Playful", "Direct")
    )

# --- Image Generation Options ---
st.header("Image Generation Options")
generate_image_option = st.checkbox("Generate a related image?", value=True, help="Check to generate an image that complements your marketing content.")
if generate_image_option:
    # Dropdown for image aspect ratio
    image_aspect_ratio = st.selectbox(
        "Image Aspect Ratio:",
        ("1:1 (Square)", "4:3 (Standard)", "3:4 (Portrait)", "16:9 (Widescreen)", "9:16 (Tall Portrait)"),
        index=0, # Default to Square
        help="Choose the desired shape for your image. Different ratios are suitable for various platforms."
    )
    # Map display string to the API's required value
    # NOTE: For 'gemini-2.0-flash-preview-image-generation', explicit aspect ratio is not
    # a direct config parameter. It relies on the prompt or default behavior.
    # This selection will mostly serve as a hint to the user for what to describe in the prompt.
    aspect_ratio_map = {
        "1:1 (Square)": "1:1",
        "4:3 (Standard)": "4:3",
        "3:4 (Portrait)": "3:4",
        "16:9 (Widescreen)": "16:9",
        "9:16 (Tall Portrait)": "9:16"
    }
    selected_aspect_ratio = aspect_ratio_map[image_aspect_ratio]

    # Slider for number of images, capped at 2 for a reasonable balance of options and generation time
    num_images_to_generate = st.slider(
        "Number of Images to Generate:",
        min_value=1,
        max_value=2, # Limiting to 2 for faster demonstration and resource management
        value=1,
        step=1,
        help="Select how many image variations you'd like (max 2 for this demo). Note: Model may generate fewer or more."
    )

# --- Generation Button ---
if st.button("Generate Content & Image", use_container_width=True, type="primary"):
    # Input validation
    if not product_name or not product_description or not target_audience:
        st.warning("Please fill in all product details (Product Name, Description/Features, Target Audience) to generate content.")
    else:
        # --- Generate Text Content ---
        st.subheader("Generated Marketing Copy:")
        with st.spinner("Generating text content..."):
            # Construct the text prompt using the utility function
            text_prompt = get_marketing_prompt(
                content_type,
                product_name,
                product_description,
                target_audience,
                tone
            )
            # Call the Gemini API client for text generation
            generated_text = gemini_client.generate_content(text_prompt)

            if "Error" in generated_text:
                st.error(generated_text) # Display specific error if text generation failed
            else:
                st.write(generated_text) # Display the generated text

        # --- Generate Image(s) if option is selected ---
        if generate_image_option:
            st.subheader("Generated Image(s):")
            with st.spinner("Generating image(s)... This may take a moment."):
                # Construct the image prompt (can use the same input details as text)
                image_prompt = get_image_prompt(
                    product_name,
                    product_description,
                    target_audience,
                    content_type,
                    tone
                )
                
                # Append aspect ratio and number of images to the prompt if they are selected,
                # as the gemini-2.0-flash-preview-image-generation model relies on prompt hints.
                if selected_aspect_ratio != "1:1": # Only add if not default
                    image_prompt += f" The image should have a {selected_aspect_ratio} aspect ratio."
                if num_images_to_generate > 1:
                    image_prompt += f" Generate {num_images_to_generate} variations of this image."


                # Call the Gemini API client for image generation
                generated_images = gemini_client.generate_image(
                    image_prompt,
                    # These specific params will be primarily hinted in the prompt for this model
                    # and not directly in the config.
                    number_of_images=num_images_to_generate, 
                    aspect_ratio=selected_aspect_ratio
                )

                if generated_images:
                    # Display each generated image and provide a download button
                    for i, img in enumerate(generated_images):
                        st.image(img, caption=f"{product_name} - {content_type} Image {i+1}", use_column_width=True)
                        
                        # Prepare image for download
                        buf = io.BytesIO()
                        img.save(buf, format="PNG") # Save PIL Image to a BytesIO object as PNG
                        byte_im = buf.getvalue() # Get the bytes

                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=byte_im,
                            file_name=f"{product_name.replace(' ', '_').lower()}_{content_type.replace(' ', '_').lower()}_image_{i+1}.png",
                            mime="image/png"
                        )
                else:
                    st.warning("Could not generate image(s). Please try adjusting your prompt or options.")

# --- Footer/Tips ---
st.markdown("---")
st.info("💡 **Tip:** For best results, provide detailed and specific descriptions for your product and target audience!")
st.caption("Powered by Google Gemini API")