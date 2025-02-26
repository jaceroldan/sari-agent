using UnityEngine;
using System.Collections.Generic;
using System;

public class ExpirationGenerator : MonoBehaviour
{
    public static ExpirationGenerator Instance { get; private set; }

    [System.Serializable]
    public class Expiration
    {
        public string productName;
        public DateTime expirationDate;
    }

    // Dictionary to hold the range of expiration dates for each category
    private Dictionary<string, (int minDays, int maxDays)> categoryExpirationRanges = new Dictionary<string, (int minDays, int maxDays)>
    {
        { "Dairy", (7, 14) },
        { "Cookies", (365, 500) },
        { "Candies", (5, 10) },
        { "Liquids", (3, 5) }
    };

    // Dictionary to hold the products under each category
    private Dictionary<string, List<string>> categoryProducts = new Dictionary<string, List<string>>
    {
        { "Dairy", new List<string> { "Milk", "Cheese", "Yogurt" } },
        { "Cookies", new List<string> { "Chocolate Chip", "Oatmeal", "Sugar", "Grocery_ChocoChips" } },
        { "Candies", new List<string> { "Gummy Bears", "Chocolate Bar", "Lollipop" } },
        { "Liquids", new List<string> { "Juice", "Soda", "Water", "DELMONTE_PINEAPPLEDRINK_HEARTSMART_220ML" } }
    };

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    // Function to generate random expiration dates based on category
    public List<Expiration> GenerateRandomExpirations()
    {
        List<Expiration> expirations = new List<Expiration>();

        foreach (var category in categoryExpirationRanges.Keys)
        {
            var range = categoryExpirationRanges[category];
            int randomDays = UnityEngine.Random.Range(range.minDays, range.maxDays);
            DateTime expirationDate = DateTime.Now.AddDays(randomDays);

            foreach (var product in categoryProducts[category])
            {
                expirations.Add(new Expiration
                {
                    productName = product,
                    expirationDate = expirationDate
                });
            }
        }

        return expirations;
    }
}