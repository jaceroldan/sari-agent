import json
import time
import requests
import ClientSide
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
    extend_left_hand_forward,
    extend_right_hand_forward,
    pull_left_hand_backward,
    pull_right_hand_backward,
    raise_left_hand,
    raise_right_hand,
    lower_left_hand,
    lower_right_hand,
)
from perception import center_object_on_screen
from manipulation import grab_and_read_item, rotate_and_read
from letta_client import Letta, CreateBlock, MessageCreate
from requests.exceptions import RequestException

# === Configuration ===
BASE_URL = "http://202.92.159.242:8000"
CAPTION_ENDPOINT = f"{BASE_URL}/caption_image"
PLAN_ENDPOINT = f"{BASE_URL}/plan_actions"
DECISION_ENDPOINT = f"{BASE_URL}/decide_action"

# === Letta Agent Setup ===
client = Letta(base_url="http://localhost:8283")
agent_state = client.agents.create(
    name="vpd_agent",
    memory_blocks=[
        CreateBlock(label="vision", value="", limit=5000),
        CreateBlock(label="plan", value="", limit=5000),
        CreateBlock(label="decision", value="", limit=5000),
    ],
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    include_base_tools=False
)

# === Memory Utilities ===
def update_block(agent_state, block_label, value):
    # Ensure value is a string: serialize if necessary
    if not isinstance(value, str):
        value = json.dumps(value)
    client.agents.blocks.modify(
        agent_id=agent_state.id,
        block_label=block_label,
        value=value
    )

def retrieve_block(agent_state, block_label):
    raw = client.agents.blocks.retrieve(
        agent_id=agent_state.id,
        block_label=block_label
    ).value
    # Try to parse JSON string back to Python object if possible
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw

# === Helper to extract assistant messages ===
def get_last_assistant_content(messages):
    # Search from latest to earliest
    for msg in reversed(messages):
        # Prefer content if present
        if hasattr(msg, 'content') and msg.content:
            return msg.content
        # Otherwise fallback to reasoning text
        if msg.message_type == 'reasoning_message' and hasattr(msg, 'reasoning'):
            return msg.reasoning
    return None

# === Client-Side Action Map ===
ACTION_MAP = {
    "move_forward": move_forward,
    "move_backward": move_backward,
    "move_left": move_left,
    "move_right": move_right,
    "pan_left": pan_left,
    "pan_right": pan_right,

    "pan_up": pan_up,
    "pan_down": pan_down,
    "extend_left_hand_forward": extend_left_hand_forward,
    "extend_right_hand_forward": extend_right_hand_forward,
    "pull_left_hand_backward": pull_left_hand_backward,
    "pull_right_hand_backward": pull_right_hand_backward,
    "raise_left_hand": raise_left_hand,
    "raise_right_hand": raise_right_hand,
    "lower_left_hand": lower_left_hand,
    "lower_right_hand": lower_right_hand,
    "toggle_left_grip": _GRIP_LEFT_,
    "toggle_right_grip": _GRIP_RIGHT_,
    # "center_object_on_screen": center_object_on_screen,
    # "grab_and_read_item": grab_and_read_item,
    "rotate_and_read": rotate_and_read,   
}

# === Agent Loop ===
LOOP_LIMIT = 999
image_path = "screenshots/ClientScreenshot.png"
goal = input("Enter your goal: ")
goal_tag = f"<goal>{goal}</goal>"
step_count = 0

while step_count < LOOP_LIMIT:
    ClientSide.RequestScreenshot()
    step_count += 1
    print(f"\n===== STEP {step_count} =====")

    # --- LOCAL VISION via endpoint ---
    try:
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            vision_payload = {
                "prompt": (
                    f"You are the vision component. Goal: {goal_tag}\n"
                    f"Previous captions: {retrieve_block(agent_state, 'vision')}"
                )
            }
            cap_res = requests.post(CAPTION_ENDPOINT, data=vision_payload, files=files)
            cap_res.raise_for_status()
            caption = cap_res.json()["response"]
        update_block(agent_state, "vision", caption)
        print("VISION CAPTION:", caption)
    except RequestException as e:
        print("Error in external caption endpoint:", e)
        continue

    # --- LOCAL PLANNING via endpoint ---
    try:
        plan_payload = {
            "goal": goal_tag,
            "caption": caption,
            "previous_plans": retrieve_block(agent_state, 'plan')
        }
        plan_res = requests.post(PLAN_ENDPOINT, data=plan_payload)
        plan_res.raise_for_status()
        plan = plan_res.json()["plan"]
        update_block(agent_state, "plan", plan)
        print("PLANNED STEPS:", plan)
    except RequestException as e:
        print("Error in external planning endpoint:", e)
        continue

    # --- LOCAL DECISION via endpoint ---
    try:
        decision_payload = {"plan": plan, "previous_actions": retrieve_block(agent_state, 'decision')}
        dec_res = requests.post(DECISION_ENDPOINT, data=decision_payload)
        dec_res.raise_for_status()
        decision_struct = dec_res.json()
        # commit structured decision to memory: serialize automatically in update_block
        update_block(agent_state, "decision", decision_struct)
        print("DECISION from endpoint:", decision_struct)
        decisions = decision_struct["response"]

        for item in decisions:
            try:
                decision_data = item["function"]
                action_name = decision_data["name"]
                args = json.loads(decision_data.get("arguments", "{}"))

                action_func = ACTION_MAP.get(action_name)
                if action_func:
                    print(f"Executing: {action_name}")
                    action_func(**args)
                else:
                    print(f"Unknown action: {action_name}")
            except json.JSONDecodeError as e:
                print("Error parsing decision JSON:", e)
    except RequestException as e:
        print("Error in external decision endpoint:", e)
        continue

    # --- LETTA AGENT for integrated reasoning ---
    try:
        # Combine blocks as context
        vision_mem = retrieve_block(agent_state, 'vision')
        plan_mem = retrieve_block(agent_state, 'plan')
        dec_mem = retrieve_block(agent_state, 'decision')
        combined_context = (
            f"Goal: {goal_tag}\n"
            f"Vision: {vision_mem}\n"
            f"Plan: {plan_mem}\n"
            f"Decision: {dec_mem}"
        )
        response = client.agents.messages.create(
            agent_id=agent_state.id,
            messages=[MessageCreate(role="user", content=combined_context)]
        )
        print('DEBUG response:', response)
        print('DEBUG response.messages: ', response.messages)
        integrated = get_last_assistant_content(response.messages)
        print("INTEGRATED RESPONSE:", integrated)
        # TODO: put this back into memory?
    except Exception as e:
        import traceback; traceback.print_exc()
        print("Error in Letta integrated reasoning:", e)

    time.sleep(0.5)