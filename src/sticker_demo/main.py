from moviepy import ImageClip, concatenate_videoclips
import os

# --- Configuration ---
# NOTE: Replace this with the actual path to your 390x130 image
SOURCE_IMAGE_PATH = '../assets/merged.jpg' 
OUTPUT_GIF_PATH = '../output/test.gif'

# Duration for which each "frame" of the animation should display (in seconds)
FRAME_DURATION = 0.5

# The width and height of the individual square images
SEGMENT_SIZE = 130

def create_progressive_gif(image_path, output_path, duration, segment_size):
    """
    Creates an animated GIF by progressively revealing a combined horizontal image.

    :param image_path: Path to the 390x130 source image.
    :param output_path: Path to save the final GIF.
    :param duration: Duration (in seconds) for each frame of the GIF.
    :param segment_size: The width/height of the individual squares (130).
    """
    if not os.path.exists(image_path):
        print(f"Error: Source image not found at '{image_path}'")
        return

    # 1. Load the entire image as a clip (but we will only use parts of it)
    full_clip = ImageClip(image_path, duration=duration)
    
    # The total height is 130
    H = segment_size
    
    # --- Define the three progressive frames ---
    
    # Frame 1: 130x130 (first segment)
    # The image is 390x130. We take a crop from (x1, y1) to (x2, y2)
    # Crop: x=0, y=0 to x=130, y=130
    W1 = segment_size
    clip_130x130 = full_clip.resize(
        newsize=(W1, H) # This is a simple crop because ImageClip's size
                        # is automatically set to the size of the loaded image.
                        # We use `set_make_frame` to crop in the next step.
    ).set_duration(duration)
    
    # We define a function to crop the full image to the desired size.
    def make_frame_1(t):
        # t is the time. We want to crop from (x1, y1, x2, y2)
        # Cropping the first 130 pixels of width
        return full_clip.get_frame(t)[:H, :W1]

    # Assign the cropping function to the clip
    clip_130x130.make_frame = make_frame_1
    
    
    # Frame 2: 260x130 (first two segments)
    W2 = 2 * segment_size
    clip_260x130 = full_clip.resize(
        newsize=(W2, H)
    ).set_duration(duration)
    
    def make_frame_2(t):
        # Cropping the first 260 pixels of width
        return full_clip.get_frame(t)[:H, :W2]
        
    clip_260x130.make_frame = make_frame_2

    
    # Frame 3: 390x130 (all three segments)
    W3 = 3 * segment_size
    # We can just use the full_clip directly, but we set the duration explicitly
    clip_390x130 = full_clip.set_duration(duration)
    
    def make_frame_3(t):
        # Cropping the full 390 pixels of width
        return full_clip.get_frame(t)[:H, :W3]
        
    clip_390x130.make_frame = make_frame_3


    # 2. Concatenate the clips in the desired order
    # Order: 130x130 -> 260x130 -> 390x130 (and then back to the start for loop)
    final_clip = concatenate_videoclips([
        clip_130x130, 
        clip_260x130, 
        clip_390x130
    ])

    # 3. Write the result to a GIF file
    print(f"Generating GIF... saving to {output_path}")
    final_clip.write_gif(
        output_path, 
        fps=1, # Since each frame is 1 second, fps=1 is appropriate.
        loop=0 # 0 means the GIF will loop infinitely
    )
    print("GIF generation complete!")

# --- Execute the function ---
create_progressive_gif(
    SOURCE_IMAGE_PATH, 
    OUTPUT_GIF_PATH, 
    FRAME_DURATION, 
    SEGMENT_SIZE
)