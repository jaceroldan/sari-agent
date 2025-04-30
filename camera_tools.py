import requests

from PIL import ImageDraw, Image
import ClientSide as cs

def recenter_camera(prompt: str, image_path: str, server_url: str):
    # 1. Send image + prompt to FastAPI server
    files = {"file": open(image_path, "rb")}
    params = {"prompt": prompt}

    response = requests.post(f"{server_url}/locate-object/", params=params, files=files)
    result = response.json()
    print("Response:", result)

    offset_x = result["offset_x"]
    offset_y = result["offset_y"]

    # 2. Decide rotation based on offset
    # Tweak these multipliers depending on your agent sensitivity
    ROTATION_SCALE = 0.001  # radians or degrees per pixel offset
    THRESHOLD = 20  # pixels; ignore tiny offsets

    rotation_x = 0.0  # looking up/down (pitch)
    rotation_y = 0.0  # looking left/right (yaw)

    if abs(offset_x) > THRESHOLD:
        rotation_y = offset_x * ROTATION_SCALE

    if abs(offset_y) > THRESHOLD:
        rotation_x = offset_y * ROTATION_SCALE

    # 3. Call TransformAgent
    translation = (0.0, 0.0, 0.0)  # No moving forward/backward yet, just rotate to face object
    rotation = (rotation_x, rotation_y, 0.0)

    cs.TransformAgent(translation, rotation)

    return {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "rotation_x": rotation_x,
        "rotation_z": rotation_y
    }


def center_until_close(prompt, image_capture_fn, server_url, tolerance=10, color="red", radius=20):
    while True:
        # 1. Capture a new screenshot
        image_capture_fn()
        image_path = "screenshots/ClientScreenshot.png"

        # 2. Send to FastAPI endpoint to locate the object
        files = {"file": open(image_path, "rb")}
        params = {"prompt": prompt}
        response = requests.post(f"{server_url}/locate-object/", params=params, files=files)
        result = response.json()

        # 3. Annotate the object in the image (for visual feedback)
        image = Image.open(image_path)
        annotated_image = annotate_located_object(image, result, color, radius)

        # 4. Save the annotated image (optional)
        annotated_image.save("annotated_output.png")

        # 5. Check if the object is centered within the tolerance limit
        if abs(result["offset_x"]) < tolerance and abs(result["offset_y"]) < tolerance:
            break

        # 6. Optionally: Send TransformAgent with computed rotation
        recenter_camera(prompt, image_path, server_url)



def annotate_located_object(image: Image.Image or str, result: dict, color="red", radius=20):
    """
    Draws a circle at the best patch center location based on CLIP locate result.

    Args:
        image (PIL.Image): The original image.
        result (dict): The result dict from locate_object_in_frame().
        color (str): Color of the annotation. Default "red".
        radius (int): Radius of the annotation circle. Default 20.

    Returns:
        PIL.Image: Annotated image.
    """
    if type(image) == str:
        image = Image.open(image)

    annotated_image = image.copy()
    draw = ImageDraw.Draw(annotated_image)

    center = result["best_patch_center"]
    x, y = center

    # Draw a circle centered at (x, y)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=4)

    # Optional: Draw a smaller crosshair at frame center too
    frame_center = result["frame_center"]
    fx, fy = frame_center
    draw.line((fx - 10, fy, fx + 10, fy), fill="blue", width=2)
    draw.line((fx, fy - 10, fx, fy + 10), fill="blue", width=2)

    return annotated_image
