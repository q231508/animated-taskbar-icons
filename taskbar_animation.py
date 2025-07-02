import threading
import time 
import pystray
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageSequence, UnidentifiedImageError

running = False
count = 0
frames = []
tray_icon = None

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
    global running, count, frames
    if str(item) == "Run":
        if not running:
            running = True
            threading.Thread(target=animate, args=(icon,), daemon=True).start()
    elif str(item) == "Stop":
        running = False
    elif str(item) == "Restart":
        count = 0
        icon.icon = frames[count]
    elif str(item) == "Exit":
        running = False
        icon.stop()

def select_and_processing():
    # Selects the target file
    # If valid, processes each frame of the file to fit on the taskbar
    global frames
    print("Select a file")
    
    root = tk.Tk()
    root.withdraw()
    target_file = filedialog.askopenfilename(title="Select a file") # <-- Pick an image or gif
    root.destroy()
    if not target_file:
        print("No file selected")
        return None

    try:
        gif = Image.open(target_file)
    except UnidentifiedImageError:
        print("Invalid file selected")
        return
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    print(f"Processing Frames: 0%", end='\r')
    
    frames.clear()
    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        processed_frame = frame.copy().convert("RGBA").resize((32, 32), Image.LANCZOS)
        frames.append(processed_frame)
        percent = round((i + 1) / gif.n_frames * 100, 2)
        print(f"Processing Frames: {percent}%", end='\r')

    print(f"Processing Frames: Finished!")
    return(frames[0])
        
def main():
    global tray_icon
    
    icon_image = select_and_processing() # <-- Icon thumbnail is the first frame of the provided file
    if icon_image is None:
        return
    
    tray_icon = pystray.Icon("Animated_icon", icon_image, title="Animated Icon", menu=pystray.Menu(
        pystray.MenuItem("Run", on_clicked),
        pystray.MenuItem("Stop", on_clicked),
        pystray.MenuItem("Restart", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    ))
    
    tray_icon.run()
    
if __name__ == "__main__":
    main()
