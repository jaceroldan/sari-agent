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
    move_forward,
    move_backward,
    move_left,
    move_right,
    pan_left,
    pan_right,
    pan_up,
    pan_down,
)
from perception import (
    center_object_on_screen
)
from manipulation import (
    grab_and_read_item
)



def run_agent(goal):
    LOOP_LIMIT = 999

    BASE_URL = "http://202.92.159.242:8000"
    CAPTION_ENDPOINT = f"{BASE_URL}/caption_image"
    PLAN_ENDPOINT = f"{BASE_URL}/plan_actions"
    DECISION_ENDPOINT = f"{BASE_URL}/decide_action"

    image_path = "screenshots/ClientScreenshot.png"
    goal = f"<goal>{goal}</goal>"

    # Memory object to track history
    memory = {
        "captions": [],
        "plans": [],
        "actions": [],
        "step_count": 0,
    }

    ACTION_MAP = {
        "move_forward": move_forward,
        "move_backward": move_backward,
        "move_left": move_left,
        "move_right": move_right,
        "pan_left": pan_left,
        "pan_right": pan_right,

        "pan_up": pan_up,
        "pan_down": pan_down,
        "extend_left_hand_forward": _XTNFWD_LEFT_,
        "extend_right_hand_forward": _XTNFWD_RIGHT_,
        "pull_left_hand_backward": _PLLBCK_LEFT_,
        "pull_right_hand_backward": _PLLBCK_RIGHT_,
        "raise_left_hand": _RSE_LEFT_,
        "raise_right_hand": _RSE_RIGHT_,
        "lower_left_hand": _LWR_LEFT_,
        "lower_right_hand": _LWR_RIGHT_,
        "toggle_left_grip": _GRIP_LEFT_,
        "toggle_right_grip": _GRIP_RIGHT_,
        "center_object_on_screen": center_object_on_screen,
        "grab_and_read_item": grab_and_read_item,
    }

    while memory["step_count"] < LOOP_LIMIT:
        ClientSide.RequestScreenshot()
        memory["step_count"] += 1

        print("*" * 100)
        print(f"STEP {memory['step_count']}")
        print("*" * 100)

        # VISION
        with open(image_path, "rb") as image_file:
            image_data = {"file": image_file}
            caption_prompt = f"""
            You are the vision component for an agent in a virtual store environment.
            Goal: {goal}

            Previous memory:
            - Prior captions: {memory['captions'][-3:]}

            Now, describe what you currently see.
            """

            caption_response = requests.post(CAPTION_ENDPOINT, data={"prompt": caption_prompt}, files=image_data)
            if caption_response.status_code != 200:
                print("Error in captioning image:", caption_response.text)
                break

            caption = caption_response.json()["response"]
            memory["captions"].append(caption)
            print("VISION CAPTION:", caption)

        # PLANNING
        planner_prompt = f"""
        You are the planning component for an agent in a virtual store environment.

        Goal: {goal}
        Vision Caption: <vision-caption>{caption}</vision-caption>
        Previous 2 plans: {memory['plans'][-2:]}

        Make a strict plan of steps that bring the agent closer to achieving the goal. 
        Indicate if object is in vision or within reach.
        """

        plan_response = requests.post(PLAN_ENDPOINT, data={"goal": goal, "caption": planner_prompt})
        if plan_response.status_code != 200:
            print("Error in planning actions:", plan_response.text)
            break

        planned_steps = plan_response.json()["plan"]
        memory["plans"].append(planned_steps)
        print("PLANNED STEPS:", planned_steps)

        # DECISION
        decision_prompt = f"""
        You are the decider agent for an agent in a virtual grocery store.

        Goal: {goal}
        Current plan: {planned_steps}
        Prior actions: {memory['actions'][-5:]}

        Follow these heuristics:
        1. Move closer to object.
        2. If visible, center the object.
        3. If centered, grab and read item.
        """

        decision_response = requests.post(DECISION_ENDPOINT, data={"prompt": decision_prompt})
        if decision_response.status_code != 200:
            print("Error in deciding action:", decision_response.text)
            break

        decisions = decision_response.json()["response"]
        print("DECISION:", decisions)

        for item in decisions:
            try:
                decision_data = item["function"]
                action_name = decision_data["name"]
                args = json.loads(decision_data.get("arguments", "{}"))

                action_func = ACTION_MAP.get(action_name)
                if action_func:
                    print(f"Executing: {action_name}")
                    action_func(**args)
                    memory["actions"].append({"name": action_name, "args": args})
                else:
                    print(f"Unknown action: {action_name}")
            except json.JSONDecodeError as e:
                print("Error parsing decision JSON:", e)
