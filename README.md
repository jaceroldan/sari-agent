# sari-sari-sandbox
! FOR ALPHA TESTING !
Sari-sari Sandbox 0.1

1. Open the folder containing ClientSide.py in terminal
2. Open Python Shell and import ClientSide
3. Open bin/sss.exe
4. Run ClientSide functions in Python
   
   e.g.
   import ClientSide as a
   a.TransformAgent((0,0,0.02),(0,0,0))
   a.RequestScreenshot()

# ClientSide API Documentation
This module provides functions to send various commands to a WebSocket server and handle the responses.

Functions:
	TransformAgent(translation, rotation):
		Transforms the agent by the specified translation and rotation with respect to the camera transform.

	TransformHands(leftTranslation, leftRotation, rightTranslation, rightRotation):
		Transforms the agent hands by the specified translation and rotation with respect to their corresponding transforms.

	ToggleLeftGrip():
 		Toggles the grip of the left hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the left hand.
	
 	ToggleRightGrip():
		Toggles the grip of the right hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the right hand.

	RequestScreenshot():
		Requests a screenshot and saves the received image as "ClientScreenshot.png" in the same directory as this module.
