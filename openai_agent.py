import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

tools = [
    {
      "type": "function",
      "function": {
        "name": "transform_agent",
        "description": "Transforms the agent by the specified translation and rotation with respect to the environment.",
        "parameters": {
          "type": "object",
          "properties": {
            "translate_x": {"type": "number", "description": "Move the agent translate_x units to the right if positive, left if negative."},
            "translate_y": {"type": "number", "description": "Move the agent translate_y units up if positive, down if negative."},
            "translate_z": {"type": "number", "description": "Move the agent translate_z units forward if positive, backward if negative."},
            "degrees_x": {"type": "number", "description": "Rotate the agent's camera degrees_x units down if positive, up if negative."},
            "degrees_y": {"type": "number", "description": "Rotate the agent's camera degrees_y units to the right if positive, left if negative."},
            "degrees_z": {"type": "number", "description": "Rotate agent's camera degrees_z units counterclockwise if positive, clockwise if negative."}
          },
          "required": ["translate_x", "translate_y", "translate_z", "degrees_x", "degrees_y", "degrees_z"],
          "additionalProperties": False
        },
        "strict": True
      }
    },
    {
      "type": "function",
      "function": {
        "name": "transform_hands",
        "description": "Transforms the agent's left hand and right hand by the specified translation and rotation with respect to the environment.",
        "parameters": {
          "type": "object",
          "properties": {
            "left_translate_x": {"type": "number", "description": "Move the left hand right if positive, left if negative."},
            "left_translate_y": {"type": "number", "description": "Move the left hand up if positive, down if negative."},
            "left_translate_z": {"type": "number", "description": "Move the left hand forward if positive, backward if negative."},
            "left_degrees_x": {"type": "number", "description": "Rotate the left hand down if positive, up if negative."},
            "left_degrees_y": {"type": "number", "description": "Rotate the left hand right if positive, left if negative."},
            "left_degrees_z": {"type": "number", "description": "Rotate the left hand counterclockwise if positive, clockwise if negative."},
            "right_translate_x": {"type": "number", "description": "Move the right hand right if positive, left if negative."},
            "right_translate_y": {"type": "number", "description": "Move the right hand up if positive, down if negative."},
            "right_translate_z": {"type": "number", "description": "Move the right hand forward if positive, backward if negative."},
            "right_degrees_x": {"type": "number", "description": "Rotate the right hand down if positive, up if negative."},
            "right_degrees_y": {"type": "number", "description": "Rotate the right hand right if positive, left if negative."},
            "right_degrees_z": {"type": "number", "description": "Rotate the right hand counterclockwise if positive, clockwise if negative."}
          },
          "required": ["left_translate_x", "left_translate_y", "left_translate_z", "left_degrees_x", "left_degrees_y", "left_degrees_z", "right_translate_x", "right_translate_y", "right_translate_z", "right_degrees_x", "right_degrees_y", "right_degrees_z"],
          "additionalProperties": False
        },
        "strict": True
      }
    },
    {
      "type": "function",
      "function": {
        "name": "toggle_left_grip",
        "description": "Toggles the grip of the left hand. Will successfully toggle if an XR Grab Interactable object collides with the left hand.",
        "parameters": {
          "type": "object",
          "properties": {},
          "required": [],
          "additionalProperties": False
        },
        "strict": True
      }
    },
    {
      "type": "function",
      "function": {
        "name": "toggle_right_grip",
        "description": "Toggles the grip of the right hand. Will successfully toggle if an XR Grab Interactable object collides with the right hand.",
        "parameters": {
          "type": "object",
          "properties": {},
          "required": [],
          "additionalProperties": False
        },
        "strict": True
      }
    }
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "You have a cereal box in front of you, I need you to grab it. You still need to walk a little though."}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
 