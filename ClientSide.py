import os
import asyncio
import websockets
import json
import re
from typing import (
    Tuple,
    Dict,
    Any
)

async def SendCommand(command: Dict[str, Any], uri: str):
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(json.dumps(command))
        if command["command"] == "RequestScreenshot" or command["command"] == "RequestAnnotation":
            imageBytes = await websocket.recv()

            folder_name = os.path.join("screenshots", command["folder_name"])
            prefix = str(command["prefix"]) + "-" if str(command["prefix"]) else ""
            suffix = "-" + str(command["suffix"]) if str(command["suffix"]) else ""
            file_name = f"{prefix}ClientScreenshot{suffix}.png"

            if folder_name:
                os.makedirs(folder_name, exist_ok=True)  # Creates the folder if it doesn't exist

            # Save the image file in the specified folder
            file_path = os.path.join(folder_name, file_name) if folder_name else file_name

            with open(file_path, "wb") as file:
                file.write(imageBytes)
            print(f"Screenshot received and saved as {file_name}")
        else:
            response = await websocket.recv()
            return response

def TransformAgent(translation: Tuple[float],
                   rotation: Tuple[float],
                   uri: str = "ws://localhost:8080/commands") -> Dict[str, Tuple[float]]:
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformAgent",
        "translation": translation,
        "rotation": rotation
    }, uri))

    extracted_state = re.findall(r'\((.*?)\)', result, re.DOTALL)
    assert len(extracted_state) == 2, "Expected 2 Tuple[float], got " + str(len(extracted_state))
    agent_state = {
        'translation': tuple(map(float, extracted_state[0].split(', '))),
        'rotation': tuple(map(float, extracted_state[1].split(', ')))
    }
    return agent_state

def TransformHands(leftTranslation: Tuple[float],
                   leftRotation: Tuple[float],
                   rightTranslation: Tuple[float],
                   rightRotation: Tuple[float],
                   uri: str = "ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformHands",
        "leftTranslation": leftTranslation,
        "leftRotation": leftRotation,
        "rightTranslation": rightTranslation,
        "rightRotation": rightRotation
    }, uri))
    
    extracted_state = re.findall(r'\((.*?)\)', result, re.DOTALL)
    assert len(extracted_state) == 4, "Expected 4 Tuple[float], got " + str(len(extracted_state))
    current_state = {
        'leftTranslation': tuple(map(float, extracted_state[0].split(', '))),
        'leftRotation': tuple(map(float, extracted_state[1].split(', '))),
        'rightTranslation': tuple(map(float, extracted_state[2].split(', '))),
        'rightRotation': tuple(map(float, extracted_state[3].split(', ')))
    }
    return current_state

def ToggleLeftGrip(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ToggleLeftGrip"
    }, uri))

    if "True" in result:    return True
    return False

def ToggleRightGrip(uri="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ToggleRightGrip"
    }, uri))

    if "True" in result:    return True
    return False

def RequestScreenshot(prefix="", suffix="", folder_name="", uri="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestScreenshot",
        "prefix": prefix,
        "suffix": suffix,
        "folder_name": folder_name
    }, uri))
    return result

def Reset(uri: str="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "ResetEnvironment"
    }, uri))

def RequestAnnotation(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestAnnotation"
    }, uri))
    return result

def RequestJson(uri: str="ws://localhost:8080/commands"):
    result = asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestJson"
    }, uri))
    return result

def ResetHandsNoVR():
    TransformHands((0, 0.025*16, 0), (0, 0, 0), (0, 0.025*16, 0), (0, 0, 0))

# Controls
_MOVE_FWD_ = lambda: TransformAgent((0, 0, 0.1), (0, 0, 0))
_MOVE_BCK_ = lambda: TransformAgent((0, 0, -0.1), (0, 0, 0))
_MOVE_LEFT_ = lambda: TransformAgent((-0.1, 0, 0), (0, 0, 0))
_MOVE_RIGHT_ = lambda: TransformAgent((0.1, 0, 0), (0, 0, 0))
_PAN_LEFT_ = lambda: TransformAgent((0, 0, 0), (0, -2.5, 0))
_PAN_RIGHT_ = lambda: TransformAgent((0, 0, 0), (0, 2.5, 0))
_PAN_UP_ = lambda: TransformAgent((0, 0, 0), (-2.5, 0, 0))
_PAN_DOWN_ = lambda: TransformAgent((0, 0, 0), (2.5, 0, 0))
_GRIP_LEFT_ = lambda: ToggleLeftGrip()
_GRIP_RIGHT_ = lambda: ToggleRightGrip()
_XTNFWD_LEFT_ = lambda: TransformHands((0, 0, 0.025), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_PLLBCK_LEFT_ = lambda: TransformHands((0, 0, -0.025), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_XTNFWD_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, 0.025), (0, 0, 0))
_PLLBCK_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, -0.025), (0, 0, 0))
_RSE_LEFT_ = lambda: TransformHands((0, 0.025, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_LWR_LEFT_ = lambda: TransformHands((0, -0.025, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
_RSE_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0.025, 0), (0, 0, 0))
_LWR_RIGHT_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, -0.025, 0), (0, 0, 0))
_ROT_RIGHT_CLOCK_ = lambda: TransformHands((0, 0, 0), (0, 15, 0), (0, 0, 0), (0, 0, 0))
_ROT_RIGHT_CTRCLOCK_ = lambda: TransformHands((0, 0, 0), (0, -15, 0), (0, 0, 0), (0, 0, 0))
_ROT_LEFT_CLOCK_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 15, 0))
_ROT_LEFT_CTRCLOCK_ = lambda: TransformHands((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, -15, 0))
_RESET_ = lambda: Reset()
_RESET_HANDS_NO_VR_ = lambda: ResetHandsNoVR()
_REQUEST_SCREENSHOT_ = lambda: RequestScreenshot()
_REQUEST_ANNOTATION_ = lambda: RequestAnnotation()
_REQUEST_JSON_ = lambda: RequestJson()

__all__ = [
    "TransformAgent",
    "TransformHands",
    "ToggleLeftGrip",
    "ToggleRightGrip",
    "RequestScreenshot",
    "RequestAnnotation",
    "RequestJson",
    "_MOVE_FWD_",
    "_MOVE_BCK_",
    "_MOVE_LEFT_",
    "_MOVE_RIGHT_",
    "_PAN_LEFT_",
    "_PAN_RIGHT_",
    "_PAN_UP_",
    "_PAN_DOWN_",
    "_GRIP_LEFT_",
    "_GRIP_RIGHT_",
    "_XTNFWD_LEFT_",
    "_PLLBCK_LEFT_" ,
    "_XTNFWD_RIGHT_",
    "_PLLBCK_RIGHT_",
    "_RSE_LEFT_",
    "_LWR_LEFT_",
    "_RSE_RIGHT_",
    "_LWR_RIGHT_",
    "_ROT_RIGHT_CLOCK_",
    "_ROT_RIGHT_CTRCLOCK_",
    "_ROT_LEFT_CLOCK_",
    "_ROT_LEFT_CTRCLOCK_",
    "_RESET_",
    "_RESET_HANDS_NO_VR_",
    "_REQUEST_SCREENSHOT_",
    "_REQUEST_ANNOTATION_",
    "_REQUEST_JSON_",
]
