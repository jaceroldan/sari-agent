import re
import requests
import time
import ClientSide
import json

# API endpoints
BASE_URL = "http://202.92.159.242:8000"  # Change if hosted elsewhere
CAPTION_ENDPOINT = f"{BASE_URL}/caption_image"
PLAN_ENDPOINT = f"{BASE_URL}/plan_actions"  # New planning step endpoint
DECISION_ENDPOINT = f"{BASE_URL}/decide_action"

# Image path (update per frame in real simulation)
image_path = "ClientScreenshot.png"

goal = "Find the box of cereal."

while True:
    with open(image_path, "rb") as image_file:
        image_data = {"file": image_file}
        caption_prompt = f"Your goal is: {goal}. What do you see?"
        
        # Step 1: Caption the image
        caption_response = requests.post(CAPTION_ENDPOINT, data={"prompt": caption_prompt}, files=image_data)
        if caption_response.status_code == 200:
            caption = caption_response.json()["response"]
            print("Caption:", caption)
        else:
            print("Error in captioning image:", caption_response.text)
            break

    # Step 2: Generate a strict sequence of planned actions
    plan_response = requests.post(PLAN_ENDPOINT, json={"goal": goal, "caption": caption})
    if plan_response.status_code == 200:
        planned_steps = plan_response.json()["steps"]
        print("Planned Steps:", planned_steps)
    else:
        print("Error in planning actions:", plan_response.text)
        break

    # Step 3: Execute each planned step in sequence
    for step in planned_steps:
        with open(image_path, "rb") as image_file:
            image_data = {"file": image_file}
            decision_prompt = f"{step}. Based on this scene: {caption}, what should I do?"
            
            decision_response = requests.post(DECISION_ENDPOINT, data={"prompt": decision_prompt}, files=image_data)
            if decision_response.status_code == 200:
                decision = decision_response.json()["response"]
                print("Decision:", decision)
                
                # Extract JSON from <tool_call> tags
                match = re.search(r'<tool_call>(.*?)</tool_call>', decision, re.DOTALL)
                if match:
                    json_text = match.group(1).strip()
                    try:
                        decision_data = json.loads(json_text)
                        print("Parsed Decision:", decision_data)

                        # Execute appropriate action
                        action_name = decision_data["name"]
                        args = decision_data.get("arguments", {})
                        if action_name == "transform_agent":
                            ClientSide.TransformAgent(
                                (args.get("translate_x", 0), args.get("translate_y", 0), args.get("translate_z", 0)),
                                (args.get("degrees_x", 0), args.get("degrees_y", 0), args.get("degrees_z", 0))
                            )
                        elif action_name == "transform_hands":
                            ClientSide.TransformHands(
                                (args.get("left_translate_x", 0), args.get("left_translate_y", 0), args.get("left_translate_z", 0)),
                                (args.get("left_degrees_x", 0), args.get("left_degrees_y", 0), args.get("left_degrees_z", 0)),
                                (args.get("right_translate_x", 0), args.get("right_translate_y", 0), args.get("right_translate_z", 0)),
                                (args.get("right_degrees_x", 0), args.get("right_degrees_y", 0), args.get("right_degrees_z", 0))
                            )
                        elif action_name == "toggle_left_grip":
                            ClientSide.ToggleLeftGrip()
                        elif action_name == "toggle_right_grip":
                            ClientSide.ToggleRightGrip()
                    except json.JSONDecodeError as e:
                        print("Error parsing JSON:", e)
                else:
                    print("No valid JSON found in decision response.")
            else:
                print("Error in deciding action:", decision_response.text)
                break
    
    # Wait before next loop iteration (to simulate real-time processing)
    time.sleep(2)
