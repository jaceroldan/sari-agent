using UnityEngine;
using TMPro;
using System.Collections.Generic;

public class ExpirationSet : MonoBehaviour
{
    public TextMeshProUGUI expirationText;
    private string productName;

    // Start is called before the first frame update
    void Start()
    {
        // Set the productName to the GameObject's name
        productName = gameObject.name;

        // Generate random expirations using the ExpirationGenerator singleton instance
        List<ExpirationGenerator.Expiration> expirations = ExpirationGenerator.Instance.GenerateRandomExpirations();
        DisplayExpiration(expirations);
    }

    // Function to display the expiration date for the assigned product
    public void DisplayExpiration(List<ExpirationGenerator.Expiration> expirations)
    {
        foreach (var expiration in expirations)
        {
            if (expiration.productName == productName)
            {
                expirationText.text = $"{expiration.expirationDate.ToString("dd MMM yy")}";
                break;
            }
        }
    }
}