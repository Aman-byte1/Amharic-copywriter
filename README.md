# ✍️ AI Copywriting Assistant

## ✨ Overview

The AI Copywriting Assistant is a Streamlit web application designed to help users quickly generate engaging marketing copy and accompanying visuals using Google's powerful Gemini AI models. Whether you need product descriptions, ad headlines, social media posts, or email subject lines, this tool streamlines the content creation process.

It leverages the multimodal capabilities of `gemini-pro` for text generation and `gemini-2.0-flash-preview-image-generation` for creating relevant images, making it a comprehensive solution for your content marketing needs.

## 🚀 Features

* **Diverse Content Types:** Generate text for product descriptions, ad headlines, social media posts, and email subject lines.
* **Customizable Tone:** Select from various tones (Professional, Friendly, Excited, Luxurious, Playful, Direct) to match your brand voice.
* **AI-Powered Image Generation:** Automatically generate relevant images to complement your marketing copy using a multimodal Gemini model.
* **Dynamic Prompting:** Intelligent prompt construction ensures high-quality and contextually relevant AI outputs.
* **Image Aspect Ratio Selection:** While the `gemini-2.0-flash-preview-image-generation` model handles this implicitly through prompts, the UI provides options for common aspect ratios (1:1, 4:3, 3:4, 16:9, 9:16) to guide your visual requests.
* **Multiple Image Variations:** Request up to 2 image variations for each generation task.
* **Direct Image Download:** Easily download generated images with a click.
* **User-Friendly Interface:** Built with Streamlit for an intuitive and responsive user experience.

## 🛠️ Technologies Used

* **Python 3.9+**
* **Streamlit:** For building the interactive web application.
* **Google Generative AI SDK (`google-generativeai`):** For interacting with Gemini models.
  * `gemini-pro`: Text generation.
  * `gemini-2.0-flash-preview-image-generation`: Multimodal text and image generation.
* **`python-dotenv`:** For managing API keys securely.
* **Pillow (PIL):** For image manipulation (opening and saving generated images).

## ⚙️ Setup and Installation

Follow these steps to get the AI Copywriting Assistant up and running on your local machine.

### Prerequisites

* Python 3.9 or higher installed.
* A Google Cloud Project with the Gemini API enabled.
* A Google API Key with access to Gemini models (`gemini-pro` and `gemini-2.0-flash-preview-image-generation`).
  * **How to get an API Key:**
    1. Go to the [Google AI Studio](https://aistudio.google.com/app/apikey).
    2. Click "Get API key" or "Create API key in new project."
    3. Copy your generated API key.

### Installation Steps

1. **Clone the Repository:**
   **Bash**

   ```
   git clone https://github.com/your-username/ai-copywriting-assistant.git
   cd ai-copywriting-assistant
   ```

   *(Replace `your-username/ai-copywriting-assistant` with your actual GitHub repository path if you fork it.)*
2. **Create a Virtual Environment (Recommended):**
   **Bash**

   ```
   python -m venv .venv
   ```
3. **Activate the Virtual Environment:**

   * **On Windows:**
     **Bash**

     ```
     .venv\Scripts\activate
     ```
   * **On macOS/Linux:**
     **Bash**

     ```
     source .venv/bin/activate
     ```
4. **Install Dependencies:**
   **Bash**

   ```
   pip install -r requirements.txt
   ```

   (If you don't have a `requirements.txt` file yet, create one by running `pip freeze > requirements.txt` after installing the necessary packages: `streamlit`, `google-generativeai`, `python-dotenv`, `Pillow`.)

   To manually install them:

   **Bash**

   ```
   pip install streamlit google-generativeai python-dotenv Pillow
   ```
5. **Set Your Google API Key:**
   Create a file named `.env` in the root directory of your project (the same directory as `app.py`) and add your Google API key:

   ```
   GOOGLE_API_KEY="YOUR_API_KEY_HERE"
   ```

   **Important:** Do not commit your `.env` file to version control (e.g., Git). It's already included in the `.gitignore` file, but always double-check.

## 🏃 How to Run the App

Once you've completed the setup, run the Streamlit application:

**Bash**

```
streamlit run app.py
```

This command will open the application in your default web browser.

## 💡 Usage

1. **Enter Product Details:** Fill in the "Product Name," "Product Description/Key Features," and "Target Audience" fields with relevant information about your product or service. The more detailed and specific you are, the better the AI's output will be.
2. **Select Content Type and Tone:**
   * Choose the "Type of Text Content to Generate" from the dropdown (e.g., Product Description, Ad Headline).
   * Select the "Desired Tone" for your copy (e.g., Professional, Friendly).
3. **Image Generation Options:**
   * Check "Generate a related image?" if you want an image to be created.
   * Select the "Image Aspect Ratio" and "Number of Images to Generate" (up to 2).
4. **Generate Content:** Click the "Generate Content & Image" button.
5. **View Results:** The generated marketing copy will appear under "Generated Marketing Copy," and any generated images will be displayed under "Generated Image(s)." You can download the images directly.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your chan**ges.**^^
4. **Commit your changes (**`<span class="citation-14">git commit -m 'Add some feature'</span>`).^^
5. **Push to the branch (**`<span class="citation-13">git push origin feature/your-feature-name</span>`).^^
6. **Open a Pull Request.**^^

## 📜 License^^

This project is licensed under the MIT License - see the [LICENSE^^](https://www.google.com/search?q=LICENSE) file for details.

## 📞 Contact

If you have any questions or feedback, feel free to open an issue in this repository.

---

**Happy Copywriting with AI!**
