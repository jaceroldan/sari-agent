using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.XR.Interaction.Toolkit;

public class Agent : MonoBehaviour
{
    public GameObject xrRig;
    public GameObject mainCamera;
    public GameObject leftHandObject;
    public GameObject rightHandObject;
    public CharacterController character;
    public Transform cameraOffset;
    
    public Grip leftGrip;
    public Grip rightGrip;
    public bool isLeftGrip = false;
    public bool isRightGrip = false;

    void Start()
    {
        cameraOffset = xrRig.transform.Find("Camera Offset");
    }

    void Update()
    {
        if (leftGrip.isGrip)
        {
            leftGrip.Grab();
        }
        else if (leftGrip.isGrip == false)
        {
            leftGrip.Release();
        }
    }

    public void TransformAgent(Vector3 translation, Vector3 rotation)
    {
        Vector3 horizontalTranslation = new Vector3(translation.x, 0, translation.z);
        Vector3 verticalTranslation = new Vector3(0, translation.y, 0);

        character.Move(mainCamera.transform.TransformDirection(horizontalTranslation));
        cameraOffset.Translate(verticalTranslation, Space.Self);
        cameraOffset.Rotate(rotation, Space.Self);
        Debug.Log("Agent Moved: " + translation);
        Debug.Log("Agent Rotated: " + rotation);
    }
    

    public void TransformHands(Vector3 leftTranslation, Vector3 leftRotation, Vector3 rightTranslation, Vector3 rightRotation)
    {
        leftHandObject.transform.Translate(leftTranslation, Space.Self);
        leftHandObject.transform.Rotate(leftRotation, Space.Self);

        rightHandObject.transform.Translate(rightTranslation, Space.Self);
        rightHandObject.transform.Rotate(rightRotation, Space.Self);

        Debug.Log("Left Hand Moved: " + leftTranslation);
        Debug.Log("Left Hand Rotated" + leftRotation);
        Debug.Log("Right Hand Moved: " + rightTranslation);
        Debug.Log("Right Hand Rotated" + rightRotation);
    }

    public void ToggleGrip(Grip grip)
    {
        if(grip.isGrip == false)
        {
            if(grip.directInteractor.interactablesHovered.Count > 0)
            {
                grip.isGrip = true;
            }
        }
        else
        {
            grip.isGrip = false;
        }
        Debug.Log("Grip: " + grip.isGrip);
    }

    public IEnumerator TakeScreenshotCoroutine(Action<byte[]> callback)
    {
        yield return new WaitForEndOfFrame();

        Texture2D screenshotTexture = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        screenshotTexture.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenshotTexture.Apply();

        byte[] screenshotBytes = screenshotTexture.EncodeToPNG();
        callback(screenshotBytes);

        Destroy(screenshotTexture);
    }

    public void TakeScreenshot(Action<byte[]> callback)
    {
        StartCoroutine(TakeScreenshotCoroutine(callback));
    }
}

