def get_marketing_prompt(content_type, product_name, product_description, target_audience, tone):
    """
    Constructs a marketing content generation prompt for the AI.
    """
    prompt = f"You are an expert copywriter. Generate a {content_type} for the following product:\n\n"
    prompt += f"Product Name: {product_name}\n"
    prompt += f"Product Description/Key Features: {product_description}\n"
    prompt += f"Target Audience: {target_audience}\n"
    prompt += f"Desired Tone: {tone}\n\n"
    prompt += f"Please ensure the {content_type} is compelling and persuasive."

    if content_type == "Product Description":
        prompt += " Focus on benefits and unique selling points."
    elif content_type == "Ad Headline":
        prompt += " Make it short, attention-grabbing, and impactful."
    elif content_type == "Social Media Post":
        prompt += " Keep it concise and include relevant emojis or hashtags. Suggest 2-3 relevant hashtags."
    elif content_type == "Email Subject Line":
        prompt += " Make it concise, intriguing, and likely to increase open rates."

    prompt += "\n\nGenerated Content:"
    return prompt
def get_image_prompt(product_name, product_description, target_audience, content_type, tone):
    """
    Constructs an image generation prompt based on marketing content details.
    """
    base_prompt = f"A photorealistic image of {product_name}. "
    base_prompt += f"It should visually represent the core features of: {product_description}. "
    base_prompt += f"The image is intended for a {target_audience} audience. "
    base_prompt += f"The overall mood and style should be {tone}. "

    # Add specifics based on content type, if helpful for the image
    if content_type == "Product Description":
        base_prompt += "Show the product clearly and highlight its benefits visually."
    elif content_type == "Ad Headline":
        base_prompt += "Create a striking and eye-catching visual that complements an advertisement."
    elif content_type == "Social Media Post":
        base_prompt += "Make it engaging and suitable for social media feeds."
    elif content_type == "Email Subject Line":
        # Image for email might be more conceptual
        base_prompt += "Generate an abstract or conceptual image that evokes the product's essence."

    base_prompt += "High quality, studio lighting, detailed." # Quality modifiers

    return base_prompt

# You can add more prompt templates here as you expand content types