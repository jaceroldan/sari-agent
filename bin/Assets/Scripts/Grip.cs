using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class Grip : MonoBehaviour
{
    public XRDirectInteractor directInteractor;
    public Animator animator;
    public bool isGrip = false;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void Grab()
    {

        if (directInteractor.interactablesHovered.Count > 0)
        {
            IXRSelectInteractable interactable = directInteractor.interactablesHovered[0] as IXRSelectInteractable;
            
            if (interactable != null && !directInteractor.hasSelection)
            {
                directInteractor.StartManualInteraction(interactable);
                Debug.Log("Grabbed " + interactable);
            }
        }
        else
        {
            Debug.Log("Nothing to grab");
        }
    }

    public void Release()
    {
        if (directInteractor.hasSelection)
        {
            directInteractor.EndManualInteraction();
            Debug.Log("Released");
        }
        else
        {
            Debug.Log("Nothing to release");
        }
    }
}
