import os
import asyncio
import websockets
import json

async def SendCommand(command, uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(json.dumps(command))
        if command["command"] == "RequestScreenshot":
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
            print(response)

async def FetchData(uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        response = await websocket.recv()
        return response

def TransformAgent(translation, rotation, uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand({
        "command": "TransformAgent",
        "translation": translation,
        "rotation": rotation
    }, uri))
    print("Client Side: Agent moved by", translation, rotation)

def TransformHands(leftTranslation, leftRotation, rightTranslation, rightRotation, uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "TransformHands",
        "leftTranslation": leftTranslation,
        "leftRotation": leftRotation,
        "rightTranslation": rightTranslation,
        "rightRotation": rightRotation
    }, uri))
    print("Client Side: Hands transformed")

def ToggleLeftGrip(uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleLeftGrip"
    }, uri))
    print("Client Side: Toggle Left Grip")

def ToggleRightGrip(uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "ToggleRightGrip"
    }, uri))
    print("Client Side: Toggle Right Grip")

def RequestScreenshot(prefix="", suffix="", folder_name="", uri="ws://localhost:8080/commands"):
    asyncio.get_event_loop().run_until_complete(SendCommand(
        {
        "command": "RequestScreenshot",
        "prefix": prefix,
        "suffix": suffix,
        "folder_name": folder_name
    }, uri))
    print("Client Side: Screenshot requested.")