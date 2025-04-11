import re
import requests
import time
import ClientSide
import json

from ClientSide import (
    _MOVE_FWD_,
    _MOVE_BCK_,
    _MOVE_LEFT_,
    _MOVE_RIGHT_,
    _PAN_LEFT_,
    _PAN_RIGHT_,
    _PAN_UP_,
    _PAN_DOWN_,
    _GRIP_LEFT_,
    _GRIP_RIGHT_,
    _XTNFWD_LEFT_,
    _XTNFWD_RIGHT_,
    _PLLBCK_LEFT_,
    _PLLBCK_RIGHT_,
    _RSE_LEFT_,
    _RSE_RIGHT_,
    _LWR_LEFT_,
    _LWR_RIGHT_,
)

LOOP_LIMIT = 999

# API endpoints
BASE_URL = "http://202.92.159.242:8000"  # Change if hosted elsewhere
# CAPTION_ENDPOINT = f"{BASE_URL}/caption_image_light"
CAPTION_ENDPOINT = f"{BASE_URL}/caption_image"
PLAN_ENDPOINT = f"{BASE_URL}/plan_actions"  # New planning step endpoint
DECISION_ENDPOINT = f"{BASE_URL}/decide_action"

# Image path (update per frame in real simulation)
image_path = "screenshots/ClientScreenshot.png"

goal = "Find the box of Koko Krunch"
i = 0

while i < LOOP_LIMIT:
    ClientSide.RequestScreenshot()
    i += 1
    print("*"*100)
    print(f"STEP {i}")  
    print("*"*100)
    with open(image_path, "rb") as image_file:
        image_data = {"file": image_file}
        caption_prompt = f"""
        You are the vision component for an agent in a virtual store environment.
        Your goal is: {goal}. You will need to describe the environment very
        comprehensively. For example:

        Goal: Find the box of cereal.
        Description: The box of cereal is near the edge of the grocery store. There seems to be a variety of different boxes,
        but it is unclear to me which one is the box of cereal exactly. I will need to get a closer look to see the item labels.

        Your description of the environment will be sent to a planning agent,
        which will create a sequence of steps to achieve your goal.
        Then, the planner will send these steps to the action agent,
        who will call the right set of tools to move the agent in the grocery store environment.

        What do you see now?
        """
        # Step 1: Caption the image
        caption_response = requests.post(CAPTION_ENDPOINT, data={"prompt": caption_prompt}, files=image_data)
        if caption_response.status_code == 200:
            caption = caption_response.json()["response"] # this actually returns a list, so I need to answer the first element.
            print(">" * 100)
            print("Caption:", caption)
            print(">" * 100)
        else:
            print("Error in captioning image:", caption_response.text)
            break

    # Step 2: Generate a strict sequence of planned actions
    plan_response = requests.post(PLAN_ENDPOINT, data={"goal": goal, "caption": caption})
    if plan_response.status_code == 200:
        planned_steps = plan_response.json()["plan"]
        print("<" * 100)
        print("Planned Steps:", planned_steps)
        print("<" * 100)
    else:
        print("Error in planning actions:", plan_response.text)
        break

    # Step 3: Execute each planned step in sequence
    # print(len(planned_steps), type(planned_steps))
    with open(image_path, "rb") as image_file:
        image_data = {"file": image_file}
        decision_prompt = f"""
        You are the decider agent for an agent in a virtual grocery store environment. 
        These are the planned steps from the planner module:
        {planned_steps}.
        
        What should I do now? Tell me what you see.
        Please return the right tool call to help the agent achieve its goal.
        """
        
        decision_response = requests.post(DECISION_ENDPOINT, data={"prompt": decision_prompt}, files=image_data)
        if decision_response.status_code == 200:
            decision = decision_response.json()["response"]
            print("+" * 100)
            print("Decision:", decision)
            print("+" * 100)
            print(type(decision))
            # Extract JSON from <tool_call> tags
            for item in decision:
                try:
                    print('Item: ', item)
                    decision_data = item["function"]
                    # Execute appropriate action
                    action_name = decision_data["name"]
                    args = decision_data.get("arguments", {})
                    if action_name == "move_forward":
                        _MOVE_FWD_()
                    elif action_name == "move_backward":
                        _MOVE_BCK_()
                    elif action_name == "move_left":
                        _MOVE_LEFT_()
                    elif action_name == "move_right":
                        _MOVE_RIGHT_()
                    elif action_name == "pan_left":
                        _PAN_LEFT_()
                    elif action_name == "pan_right":
                        _PAN_RIGHT_()
                    elif action_name == "pan_up":
                        _PAN_UP_()
                    elif action_name == "pan_down":
                        _PAN_DOWN_()

                    elif action_name == "extend_left_hand_forward":
                        _XTNFWD_LEFT_()
                    elif action_name == "extend_right_hand_forward":
                        _XTNFWD_RIGHT_()
                    
                    elif action_name == "pull_left_hand_backward":
                        _PLLBCK_LEFT_()
                    elif action_name == "pull_right_hand_backward":
                        _PLLBCK_RIGHT_()

                    elif action_name == "raise_left_hand":
                        _RSE_LEFT_()
                    elif action_name == "raise_right_hand":
                        _RSE_RIGHT_()

                    elif action_name == "lower_left_hand":
                        _LWR_LEFT_()
                    elif action_name == "lower_right_hand":
                        _LWR_RIGHT_()

                    elif action_name == "toggle_left_grip":
                        _GRIP_LEFT_()
                    elif action_name == "toggle_right_grip":
                        _GRIP_RIGHT_()
                except json.JSONDecodeError as e:
                    print("Error parsing JSON:", e)
        else:
            print("Error in deciding action:", decision_response.text)
            break
    
    # Wait before next loop iteration (to simulate real-time processing)
    time.sleep(2)
