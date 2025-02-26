using System.Collections;
using System.Collections.Generic;
using System.Data;
using UnityEngine;
using WebSocketSharp.Server;
using WebSocketSharp;

public class WebSocketHandler : MonoBehaviour
{
    private WebSocketServer wss;

    void Start()
    {
        // Start the WebSocket server on port 8080
        
        wss = new WebSocketServer("ws://localhost:8080");
        wss.AddWebSocketService<CommandBehavior>("/commands");
        wss.Start();
        Debug.Log("WebSocket server started on ws://localhost:8080/commands...");
        UnityMainThreadDispatcher.Instance();
    }

    void OnDestroy()
    {
        if (wss != null) wss.Stop();
    }
}

public class CommandBehavior : WebSocketBehavior
{
    protected override void OnMessage(MessageEventArgs e)
    {
        Debug.Log("Message received: " + e.Data);
        
        // Run the command on Unity's main thread using the dispatcher
        UnityMainThreadDispatcher.Instance().Enqueue(() => HandleCommand(e.Data));
    }

    private void HandleCommand(string json)
    {
        // Parse the incoming JSON and apply transformations
        CommandData command = JsonUtility.FromJson<CommandData>(json);
        Debug.Log(command);
        Agent agent = GameObject.FindObjectOfType<Agent>();
        Transform cameraOffset = agent.xrRig.transform.Find("Camera Offset");
        if (cameraOffset != null)
        {
            Debug.Log("Camera Offset found: " + cameraOffset.name);
        }
        else
        {
            Debug.Log("Camera Offset not found");
        }

        switch (command.command)
        {

            //Camera commands

            case "TransformAgent":
                agent.TransformAgent(new Vector3(command.translation[0], command.translation[1], command.translation[2]), 
                                     new Vector3(command.rotation[0], command.rotation[1], command.rotation[2]));
                Vector3 currentPosition = new Vector3(agent.xrRig.transform.position.x, cameraOffset.position.y, agent.xrRig.transform.position.z);
                Debug.Log("Current position: " + currentPosition + " Current rotation: " + cameraOffset.rotation.eulerAngles);
                Send("Current position: " + currentPosition + " Current rotation: " + cameraOffset.rotation.eulerAngles);
                break;

            case "TransformHands":
                agent.TransformHands(
                    new Vector3(command.leftTranslation[0], command.leftTranslation[1], command.leftTranslation[2]),
                    new Vector3(command.leftRotation[0], command.leftRotation[1], command.leftRotation[2]),
                    new Vector3(command.rightTranslation[0], command.rightTranslation[1], command.rightTranslation[2]),
                    new Vector3(command.rightRotation[0], command.rightRotation[1], command.rightRotation[2])
                );
                Debug.Log("Current left hand position: " + agent.leftHandObject.transform.position + "\nCurrent left hand rotation: " + agent.leftHandObject.transform.rotation.eulerAngles + "C\nurrent right hand position: " + agent.rightHandObject.transform.position + "\nCurrent right hand rotation: " + agent.rightHandObject.transform.rotation.eulerAngles);
                Send("Current left hand position: " + agent.leftHandObject.transform.position + "\nCurrent left hand rotation: " + agent.leftHandObject.transform.rotation.eulerAngles + "C\nurrent right hand position: " + agent.rightHandObject.transform.position + "\nCurrent right hand rotation: " + agent.rightHandObject.transform.rotation.eulerAngles);
                break;

            case "ToggleLeftGrip":
                agent.ToggleGrip(agent.leftGrip);
                Debug.Log("Left Grip: " + agent.leftGrip.isGrip);
                Send("Left Grip: " + agent.leftGrip.isGrip);
                break;

            case "ToggleRightGrip":
                agent.ToggleGrip(agent.rightGrip);
                Debug.Log("Right Grip: " + agent.rightGrip.isGrip);
                Send("Right Grip: " + agent.rightGrip.isGrip);
                break;
                
            case "RequestScreenshot":
                agent.TakeScreenshot(screenshotBytes =>
                {
                    Send(screenshotBytes);
                });
                Debug.Log("Screenshot taken");
                break;

            default:
                Debug.Log("Unknown command: " + command.command);
                Send("Unknown command: " + command.command);
                break;
        }
    }

    [System.Serializable]
    public class CommandData
    {
        public string command;
        public float[] translation;
        public float[] rotation;
        public float[] leftTranslation;
        public float[] leftRotation;
        public float[] rightTranslation;
        public float[] rightRotation;
    }
}