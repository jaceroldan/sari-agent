import requests
from PIL import Image
from paddleocr import PaddleOCR
from camera_tools import annotate_located_object
from ClientSide import _ROT_LEFT_CLOCK_, _ROT_RIGHT_CLOCK_, _REQUEST_SCREENSHOT_

ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extract_text_from_image(image):
    result = ocr.ocr(image, cls=True)
    return "\n".join([line[1][0] for line in result[0]]) if result else ""


def rotate_and_read(hand="left", text_read_fn=extract_text_from_image):
    rotate_fn = _ROT_LEFT_CLOCK_ if hand == 'left' else _ROT_RIGHT_CLOCK_
    texts = []

    for i in range(24):  # Full 360° sweep
        _REQUEST_SCREENSHOT_()
        if text_read_fn:
            texts.append(text_read_fn("screenshots/ClientScreenshot.png"))
        rotate_fn()
    return texts


def center_object_on_screen(
    target_name,
    pan_fn_map,
    locate_url="http://202.92.159.242:8000/locate-object/",
    screenshot_path="screenshots/ClientScreenshot.png",
    max_steps=30,
    tolerance=40  # pixels
):
    for step in range(max_steps):
        _REQUEST_SCREENSHOT_()

        with open(screenshot_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                locate_url,
                params={"prompt": target_name},
                files=files
            )
            # response = requests.post(f"{server_url}/locate-object/", params=params, files=files)
        
        if response.status_code != 200:
            print(f"[Step {step}] Request failed with status {response.status_code}")
            continue

        data = response.json()
        offset_x = data["offset_x"]
        offset_y = data["offset_y"]
        print(f"[Step {step}] Offset: ({offset_x}, {offset_y})")

        # Get annotations on where the CLIP model had matching patches
        annotated_image = annotate_located_object(screenshot_path, data)
        annotated_image.save("annotated_output.png")
        print("Saved annotated image in annotated_output.png")

        # Stop if object is centered
        if abs(offset_x) <= tolerance and abs(offset_y) <= tolerance:
            print(f"[Step {step}] Object centered!")
            return True, step

        # Pan based on direction
        if offset_x > tolerance:
            pan_fn_map["right"]()
        elif offset_x < -tolerance:
            pan_fn_map["left"]()

        if offset_y > tolerance:
            pan_fn_map["down"]()
        elif offset_y < -tolerance:
            pan_fn_map["up"]()

    return False, max_steps
