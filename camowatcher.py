import cv2
import numpy as np
import pytesseract
from mss import mss
import time

# Update the Tesseract path default path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

selected_region = None

def preprocess_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def extract_text(image):
    custom_config = '--psm 6'  #OCR mode optimized for sparse text
    return pytesseract.image_to_string(image, config=custom_config).strip()

def find_camo_name(text):
    for line in text.splitlines():
        if "camo" in line.lower():
            return line.strip()
    return None

def live_preview_and_monitor(sct, show_monitor_window):
    global selected_region

    if not selected_region:
        print("No region selected! Please select a region before running.")
        return

    print("Real-time monitoring started. Press 'q' to stop.")
    last_preview_update = 0
    preview_interval = 0.5  # Adjust this to control how often the preview updates (in seconds)

    last_camo_name = None
    last_detection_time = 0
    detection_timeout = 1

    try:
        while True:
            screen = np.array(sct.grab(selected_region))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

            preprocessed = preprocess_image(screen)
            detected_text = extract_text(preprocessed)

            camo_name = find_camo_name(detected_text)
            if camo_name and camo_name != last_camo_name:
                last_camo_name = camo_name
                last_detection_time = time.time()
                print(f"[CamoWatcher] Camo Unlocked: {camo_name}")

            # Reset the last_camo_name if the timeout has passed
            if time.time() - last_detection_time > detection_timeout:
                last_camo_name = None

            # Update preview window less frequently to save CPU
            if show_monitor_window and (time.time() - last_preview_update > preview_interval):
                cv2.imshow("Monitoring Window - CamoWatcher", screen)
                last_preview_update = time.time()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nExiting real-time monitoring...")
                break

            # Add a small delay to reduce CPU usage
            time.sleep(0.05)  # Sleep for 50ms to reduce CPU load

    except KeyboardInterrupt:
        print("\nMonitoring interrupted.")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    with mss() as sct:
        monitors = sct.monitors
        print("Available monitors:")
        for idx, monitor in enumerate(monitors):
            print(f"{idx}: {monitor}")

        monitor_index = int(input("Enter the monitor index you want to use (default is 1): ").strip() or 1)
        if monitor_index < 1 or monitor_index >= len(monitors):
            print("Invalid index. Defaulting to monitor 1.")
            monitor_index = 1

        selected_monitor = monitors[monitor_index]
        print(f"Selected Monitor: {selected_monitor}")

        screen = np.array(sct.grab(selected_monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

        global start_point, end_point, is_selecting
        start_point, end_point, is_selecting = None, None, False

        def select_region(event, x, y, flags, param):
            global start_point, end_point, is_selecting, selected_region
            if event == cv2.EVENT_LBUTTONDOWN:
                start_point = (x, y)
                is_selecting = True
            elif event == cv2.EVENT_MOUSEMOVE and is_selecting:
                end_point = (x, y)
            elif event == cv2.EVENT_LBUTTONUP:
                end_point = (x, y)
                is_selecting = False
                selected_region = {
                    "left": selected_monitor["left"] + min(start_point[0], end_point[0]),
                    "top": selected_monitor["top"] + min(start_point[1], end_point[1]),
                    "width": abs(end_point[0] - start_point[0]),
                    "height": abs(end_point[1] - start_point[1]),
                }
                print(f"Selected Region: {selected_region}")

        cv2.namedWindow("Select Region")
        cv2.setMouseCallback("Select Region", select_region)

        while True:
            temp_image = screen.copy()
            if start_point and end_point and is_selecting:
                cv2.rectangle(temp_image, start_point, end_point, (0, 255, 0), 2)

            cv2.imshow("Select Region", temp_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        user_choice = input("Do you want to see the monitoring box? (yes/no): ").strip().lower()
        show_monitor_window = user_choice == "yes"

        live_preview_and_monitor(sct, show_monitor_window)
