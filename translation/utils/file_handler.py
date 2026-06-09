import os

def create_folders():
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("output/final_videos", exist_ok=True)
    