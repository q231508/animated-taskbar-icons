import threading
import time 
import pystray
from PIL import Image, ImageSequence

running = False
count = 0
frames = []

def animate(icon):
    # Handles the animation loop
    # runs on a different thread
    global count, running, frames
    while running and icon.visible:
        icon.icon = frames[count]
        count = (count + 1) % len(frames)
        time.sleep(1 / 48)  # <-- FPS

def on_clicked(icon, item):
    # Checks if user chose an action from the menu
    # Complete one of the available actions
    global running
    if str(item) == "Run":
        if not running:
            running = True
            threading.Thread(target=animate, args=(icon,), daemon=True).start()
    elif str(item) == "Stop":
        running = False
    elif str(item) == "Exit":
        running = False
        icon.stop()
     
def main():
    global frames
    print("just a moment...")
    print(f"Processing Frames: 0%", end='\r')
    
    target_file = "bad_apple.gif" # <-- Provide filename, or path to file 
    gif = Image.open(target_file)
    
    raw_frames = list(ImageSequence.Iterator(gif)) 
    total = len(raw_frames)
    
    frames = []
    frames_processed = 1
    for frame in ImageSequence.Iterator(gif):
        processed_frame = frame.copy().convert("RGBA").resize((32, 32), Image.LANCZOS)
        frames.append(processed_frame)
        print(f"Processing Frames: {round((frames_processed + 1) / total * 100, 2)}%", end='\r')
        frames_processed += 1
    print(f"Processing Frames: Finished!")

    icon_image = frames[0] # <-- Icon thumbnail is the first frame of the provided file
    
    icon = pystray.Icon("Animated_icon", icon_image, title="Bad apple", menu=pystray.Menu(
        pystray.MenuItem("Run", on_clicked),
        pystray.MenuItem("Stop", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    ))
    
    icon.run()
    
if __name__ == "__main__":
    main()