import torch
import torch.cuda.graphs as cg
import gc
from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
import imageio
from torch import autocast

# Free GPU memory
def free_memory():
    torch.cuda.empty_cache()
    gc.collect()

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load text-to-image model with optimizations
def load_models():
    print("Loading text-to-image model...")
    txt2img_pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, use_safetensors=True
    ).to(device)
    txt2img_pipe.safety_checker = None  
    txt2img_pipe.enable_xformers_memory_efficient_attention()

    free_memory()

    print("Loading video diffusion model...")
    video_pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid", torch_dtype=torch.float16
    ).to(device)
    video_pipe.enable_xformers_memory_efficient_attention()

    # Optimize with torch.compile()
    txt2img_pipe.unet = torch.compile(txt2img_pipe.unet)
    video_pipe.unet = torch.compile(video_pipe.unet)

    print("Models loaded successfully!")
    return txt2img_pipe, video_pipe

# Pre-capture CUDA Graph
def capture_graph(pipe, prompt):
    img = pipe(prompt).images[0]  
    graph = cg.Graph()
    with torch.cuda.graph(graph):
        img = pipe(prompt).images[0]
    return img, graph

# Generate video
def generate_video(prompt, txt2img_pipe, video_pipe):
    try:
        print(f"Generating video for: {prompt}")

        with autocast("cuda"):
            img, graph = capture_graph(txt2img_pipe, prompt)

        free_memory()

        with autocast("cuda"):
            result = video_pipe(img, decode_chunk_size=4)
            video_frames = result.frames[0]

        if not video_frames:
            raise ValueError("No frames generated!")

        output_path = "output.mp4"
        imageio.mimsave(output_path, video_frames, fps=8)
        print(f"Video saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Generation error: {e}")
        return None

if __name__ == "__main__":
    try:
        txt2img_pipe, video_pipe = load_models()
        generate_video("A running zebra.", txt2img_pipe, video_pipe)
    except Exception as e:
        print(f"Fatal error: {e}")
