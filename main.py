import streamlit as st
import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image
import os

st.title("Text-to-Image Generation with SDXL Turbo")

# Detect device (MPS for Mac, CUDA for GPU, CPU as fallback)
def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

# Load the Stable Diffusion XL Turbo model
@st.cache_resource()
def load_model():
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
    )
    device = get_device()
    pipe.to(device)
    return pipe

pipe = load_model()

dev_info = get_device()
st.write(f"Using device: {dev_info}")

# User input for the prompt
prompt = st.text_input("Enter a prompt:", "A cinematic shot of a baby raccoon wearing an intricate Italian priest robe.")

if st.button("Generate Image"):
    with st.spinner("Generating Image..."):
        image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
        st.image(image, caption="Generated Image", use_column_width=True)

        # Option to download the image
        img_path = "generated_image.png"
        image.save(img_path)
        with open(img_path, "rb") as file:
            st.download_button("Download Image", file, file_name="generated_image.png", mime="image/png")