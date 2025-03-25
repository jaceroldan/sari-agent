import re
import requests
import time
import ClientSide
import json

# API endpoints
BASE_URL = "http://202.92.159.242:8000"  # Change this if hosted elsewhere
CAPTION_ENDPOINT = f"{BASE_URL}/caption_image"
DECISION_ENDPOINT = f"{BASE_URL}/decide_action"

# Image path (this should be updated per frame in a real simulation)
image_path = "ClientScreenshot.png"  # Replace with the correct image source

# Loop for agent inference
current_prompt = ""
while True:
    with open(image_path, "rb") as image_file:
        image_data = {"file": image_file}
        prompt = "Your goal is to find the box of cereal. What do you see?"
        current_prompt = prompt
        
        # Step 1: Caption the image
        caption_response = requests.post(CAPTION_ENDPOINT, data={"prompt": prompt}, files=image_data)
        if caption_response.status_code == 200:
            caption = caption_response.json()["response"]
            print("Caption:", caption)
        else:
            print("Error in captioning image:", caption_response.text)
            break
        
    with open(image_path, "rb") as image_file:
        image_data = {"file": image_file}
        decision_prompt = f"Your goal is to find the box of cereal. Based on this scene: {caption}, what should I do? Please tell me what actions I can do."
        
        # Step 2: Decide the next action
        decision_response = requests.post(DECISION_ENDPOINT, data={"prompt": decision_prompt}, files=image_data)
        if decision_response.status_code == 200:
            decision = decision_response.json()["response"]
            print("Decision:", decision)
            # Extract JSON from <tool_call> tags
            match = re.search(r'<tool_call>(.*?)</tool_call>', decision, re.DOTALL)
            if match:
                json_text = match.group(1).strip()
                print("JSON Text:", json_text)
                try:
                    decision_data = json.loads(json_text)
                    print("Parsed Decision:", decision_data)

                    if decision_data["name"] == "transform_agent":
                        # Extract movement values
                        move_x = decision_data["arguments"].get("translate_x", 0)
                        move_y = decision_data["arguments"].get("translate_y", 0)
                        move_z = decision_data["arguments"].get("translate_z", 0)
                        rotate_x = decision_data["arguments"].get("degrees_x", 0)
                        rotate_y = decision_data["arguments"].get("degrees_y", 0)
                        rotate_z = decision_data["arguments"].get("degrees_z", 0)
                        
                        print(f"Move: x={move_x}, y={move_y}, z={move_z}")
                        print(f"Rotate: x={rotate_x}, y={rotate_y}, z={rotate_z}")
                        ClientSide.TransformAgent((move_x, move_y, move_z), (rotate_x, rotate_y, rotate_z))

                except json.JSONDecodeError as e:
                    print("Error parsing JSON:", e)
            else:
                print("No valid JSON found in decision response.")
                
        else:
            print("Error in deciding action:", decision_response.text)
            break
    
    # Wait before the next loop iteration (to simulate real-time processing)
    time.sleep(2)
