import cv2
import numpy as np
import pytesseract
import bettercam
import time

# Path to Tesseract OCR binary (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    """Convert image to grayscale for better OCR accuracy."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def extract_text(image):
    """Extract text using Tesseract OCR with custom config."""
    custom_config = '--psm 6'  # Assume a uniform block of text
    return pytesseract.image_to_string(image, config=custom_config).strip()

def find_camo_name(text):
    """Return the first line containing the word 'camo'."""
    for line in text.splitlines():
        if "camo" in line.lower():
            return line.strip()
    return None

def monitor_screen(show_monitor_window=True, region=None):
    """Monitor a screen region using BetterCam and detect camo unlocks."""
    print("[CamoWatcher] Starting BetterCam screen capture...")

    # Initialize BetterCam
    cam = bettercam.create(output_color="BGR")

    if region:
        cam.start(region=region)
        get_frame = cam.get_latest_frame
    else:
        get_frame = cam.grab

    last_camo_name = None
    last_detection_time = 0
    detection_timeout = 1  # seconds
    preview_interval = 0.5  # seconds
    last_preview_time = 0

    try:
        while True:
            frame = get_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            gray = preprocess_image(frame)
            text = extract_text(gray)
            camo_name = find_camo_name(text)

            if camo_name and camo_name != last_camo_name:
                last_camo_name = camo_name
                last_detection_time = time.time()
                print(f"[CamoWatcher] Camo Unlocked: {camo_name}")

            # Reset camo if timeout passed
            if time.time() - last_detection_time > detection_timeout:
                last_camo_name = None

            # Show the frame preview
            if show_monitor_window and time.time() - last_preview_time > preview_interval:
                cv2.imshow("CamoWatcher - BetterCam", frame)
                last_preview_time = time.time()

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[CamoWatcher] Exiting...")
                break

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[CamoWatcher] Monitoring interrupted by user.")
    finally:
        if region:
            cam.stop()
        cv2.destroyAllWindows()

def select_region_on_screen():
    """Allow the user to draw a box on their screen to define the capture region."""
    print("[CamoWatcher] Draw a region using the mouse. Press 'q' when done.")
    screen_cam = bettercam.create(output_color="BGR")
    full_frame = screen_cam.grab()

    region_box = {"start": None, "end": None, "selecting": False}
    selected_region = {}

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            region_box["start"] = (x, y)
            region_box["selecting"] = True
        elif event == cv2.EVENT_MOUSEMOVE and region_box["selecting"]:
            region_box["end"] = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            region_box["end"] = (x, y)
            region_box["selecting"] = False

    cv2.namedWindow("Select Region")
    cv2.setMouseCallback("Select Region", mouse_callback)

    while True:
        frame = full_frame.copy()
        if region_box["start"] and region_box["end"]:
            cv2.rectangle(frame, region_box["start"], region_box["end"], (0, 255, 0), 2)
        cv2.imshow("Select Region", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    if region_box["start"] and region_box["end"]:
        x1, y1 = region_box["start"]
        x2, y2 = region_box["end"]
        selected_region = {
            "left": min(x1, x2),
            "top": min(y1, y2),
            "right": max(x1, x2),
            "bottom": max(y1, y2)
        }
        print(f"[CamoWatcher] Selected region: {selected_region}")
        return (selected_region["left"], selected_region["top"], selected_region["right"], selected_region["bottom"])
    else:
        print("[CamoWatcher] No region selected, defaulting to full screen.")
        return None

if __name__ == "__main__":
    use_custom_region = input("Do you want to select a screen region? (yes/no): ").strip().lower() == "yes"
    region = select_region_on_screen() if use_custom_region else None

    show_window = input("Do you want to show the monitoring preview window? (yes/no): ").strip().lower() == "yes"

    monitor_screen(show_monitor_window=show_window, region=region)
