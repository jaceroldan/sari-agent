# sari-sari-sandbox
! FOR ALPHA TESTING !

Sari-sari Sandbox 0.2.1

# Updates
0.2.1
1. Fixed bug: right hand not gripping properly
2. Fixed bug: decal projector not showing the expiration date
3. VR hands are lowered by 0.1 instead of 0.5

0.2
1. Forward movement is now dependent on the XR rig forward vector instead of the camera's forward vector to prevent flying when camera is rotated about x and z axes
2. Y translation restricted to [0, 2] unity units
3. Added hand physics so they do not pass through objects.
4. If no VR controller detected (API mode,) VR hands are lowered by 0.5
5. Added Reset() function in ClientSide API

# To control agent through terminal:

1. Open the folder containing ClientSide.py in terminal
2. Open Python Shell and import ClientSide
3. Open bin/sss.exe
4. Run ClientSide functions in Python

e.g.

	python
	import ClientSide as a
	a.TransformAgent((0,0,0.02),(0,0,0))
	a.RequestScreenshot()

# ClientSide Documentation
This module provides functions to send various commands to a WebSocket server and handle the responses.

Functions:
	
	TransformAgent((translateX, translateY, translateZ), (degreesX, degreesY, degreesZ)):
		Transforms the agent by the specified translation and rotation with respect to the camera transform.
	
	TransformHands((leftTranslateX, leftTranslateY, leftTranslateZ), (leftDegreesX, leftDegreesY, leftDegreesZ), (rightTranslateX, rightTranslateY, rightTranslateZ), (rightDegreesX, rightDegreesY, rightDegreesZ)):
		Transforms the agent hands by the specified translation and rotation with respect to their corresponding transforms.
	
	ToggleLeftGrip():
		Toggles the grip of the left hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the left hand.
	
	ToggleRightGrip():
		Toggles the grip of the right hand. Will successfully toggle from false to true if an XR Grab Interactable object collides with the right hand.
	
	RequestScreenshot():
		Requests a screenshot and saves the received image as "ClientScreenshot.png" in the same directory as this module.

  	RequestData():
   		Requests a plain screenshot, screenshot with bounding boxes, and bounding box coordinates.

	Reset():
		Resets the environment to its initial state with randomized grocery product placement.
