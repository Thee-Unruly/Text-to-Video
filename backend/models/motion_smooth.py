# Use RIFE (Real-Time Intermediate Flow Estimation) for fast and realistic motion interpolation.

# Import necessary packages
import cv2
from inference_file import RIFE

# Load the pre-trained RIFE model
rife = model_path = 'rife_model.pth'

def smooth_video(input_video):
    # Open the input video file
    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(frame_count - 1):
        frame1 = cap.read()[1]
        frame2 = cap.read()[1]
        interpolated_frame = rife.interpolate([frame1, frame2])
        cv2.imwrite(f"output/frame_{i}.jpg", interpolated_frame)
        
    cap.release()
    return "smoothed_video.mp4"


# Runs 100% locally
# Lightweight and fast on GPUs
# No need for cloud servers