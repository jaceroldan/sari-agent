using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using Unity.VisualScripting;
using Unity.VisualScripting.FullSerializer;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEngine.XR.Interaction.Toolkit;

public class StoreManager : MonoBehaviour
{
    public GameObject Plywood;
    public GameObject Floor;
    public GameObject Walls;
    public GameObject PriceTag;
    public GameObject LeftHingeDoor;
    public GameObject RightHingeDoor;
    public GameObject SlidingDoor;
    public float StoreLength;
    public float StoreWidth;
    public List<(float Length, float Width, float XCenter, float ZCenter)> subdivisions = new List<(float, float, float, float)>();
    public Dictionary<string, float> priceDictionary = new Dictionary<string, float>();
    
    public Dictionary<string, GameObject> shelves = new Dictionary<string, GameObject>();
    public Dictionary<string, List<List<GameObject>>> Categories = new Dictionary<string, List<List<GameObject>>>();
    
    public GroceryData groceryData;
    // Start is called before the first frame update
    void Start()
    {
        List<string> Cat = new List<string>() {"Cereal", "Biscuit", "Bread"};
        LoadJson();
        PrintCategories();
        LoadProducts();
        LoadShelves();
        RandomizePrices(1);
        FillShelves(1, 270, Cat);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            ResetEnvironment();
        }
        else if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            SwitchEnvironment("Store1");
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            SwitchEnvironment("Store2");
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            SwitchEnvironment("Store3");
        }
    }

    [System.Serializable]
    public class GroceryCategory
    {
        public string Category;
        public List<string> Items;
    }
    [System.Serializable]
    public class GroceryData
    {
        public List<GroceryCategory> Categories;
    }

    void LoadJson()
    {
        string json = System.IO.File.ReadAllText("Assets/Scripts/Categories.json");
        groceryData = JsonUtility.FromJson<GroceryData>(json);
    }

    void LoadShelves()
    {
        Shelf[] allShelves = FindObjectsOfType<Shelf>();
        foreach (Shelf shelf in allShelves)
        {
            if (!shelves.ContainsKey(shelf.id))
            {
            shelves.Add(shelf.id, shelf.gameObject);
            }
        }
    }
    void PrintCategories()
    {
        foreach (GroceryCategory category in groceryData.Categories)
        {
            Debug.Log("Category: " + category.Category);
            foreach (string item in category.Items)
            {
                Debug.Log("Item: " + item);
            }
        }
    }

    void LoadProducts()
    {
        // Load all products from the Resources folder
        foreach (var category in groceryData.Categories)
        {
            foreach (var item in category.Items)
            {
            GameObject product = Resources.Load<GameObject>("Products/" + item);
            if (product != null)
            {
                if (!Categories.ContainsKey(category.Category))
                {
                Categories[category.Category] = new List<List<GameObject>>();
                }
                Categories[category.Category].Add(new List<GameObject> { product });
                if (product.GetComponent<XRGrabInteractable>() == null)
                {
                    product.AddComponent<XRGrabInteractable>();
                }
                XRGrabInteractable grabInteractable = product.GetComponent<XRGrabInteractable>();
                grabInteractable.movementType = XRBaseInteractable.MovementType.VelocityTracking;
                grabInteractable.useDynamicAttach = true;
            }
            else
            {
                Debug.LogError("Product not found: " + item);
            }
            }
        }
    }

    public void FillShelves(int seed, float rotation, List<string> Items)
    {
        int pseudoseed = 0;
        foreach (var shelfEntry in shelves)
        {
            string shelfId = shelfEntry.Key;
            SpawnProducts(seed + pseudoseed, shelfId, rotation, Items);
            pseudoseed++;
        }
    }

    public void SpawnShelf(string ShelfId, float x, float z, float length, float width, float height, float thickness, int level, float rotation, string DoorType = "None", bool SavePrefab = false)
    {
        List<GameObject> Panels = new List<GameObject>();

        for(int i=0; i<level; i++)
        {
            Vector3 BottomPanelPosition = new Vector3(0, thickness/2+(height+thickness)*i, 0);
            Vector3 BottomPanelScale = new Vector3(length, thickness, width);
            GameObject BottomPanel = Instantiate(Plywood, BottomPanelPosition, Quaternion.identity);
            BottomPanel.transform.localScale = BottomPanelScale;
            Panels.Add(BottomPanel);
        }
        
        if (DoorType != "None")
        {
            Vector3 LeftPanelPosition = new Vector3(-1*length/2-thickness/2, ((height+thickness)*level+thickness)/2, thickness/2);
            Vector3 LeftPanelScale = new Vector3(thickness, (height+thickness)*level+thickness, width+thickness);
            GameObject LeftPanel = Instantiate(Plywood, LeftPanelPosition, Quaternion.identity);
            LeftPanel.transform.localScale = LeftPanelScale;
            Panels.Add(LeftPanel);

            Vector3 RightPanelPosition = new Vector3(length/2+thickness/2, ((height+thickness)*level+thickness)/2, thickness/2);
            Vector3 RightPanelScale = new Vector3(thickness, (height+thickness)*level+thickness, width+thickness);
            GameObject RightPanel = Instantiate(Plywood, RightPanelPosition, Quaternion.identity);
            RightPanel.transform.localScale = RightPanelScale;
            Panels.Add(RightPanel);

            Vector3 TopPanelPosition = new Vector3(0, thickness/2+(height+thickness)*level, thickness / 2);
            Vector3 TopPanelScale = new Vector3(length, thickness, width + thickness);
            GameObject TopPanel = Instantiate(Plywood, TopPanelPosition, Quaternion.identity);
            TopPanel.transform.localScale = TopPanelScale;
            Panels.Add(TopPanel);
        }

        Vector3 BackPanelPosition = new Vector3(0, ((height+thickness)*level+thickness)/2, width/2 + thickness/2);
        Vector3 BackPanelScale = new Vector3(length, (height+thickness)*level+thickness, thickness);
        GameObject BackPanel = Instantiate(Plywood, BackPanelPosition, Quaternion.identity);
        BackPanel.transform.localScale = BackPanelScale;
        Panels.Add(BackPanel);
        

        List<CombineInstance> combine = new List<CombineInstance>();

        foreach (GameObject obj in Panels)
        {
            MeshFilter meshFilter = obj.GetComponent<MeshFilter>();
            if (meshFilter != null)
            {
                CombineInstance ci = new CombineInstance();
                ci.mesh = meshFilter.sharedMesh;
                ci.transform = obj.transform.localToWorldMatrix;
                combine.Add(ci);
                obj.SetActive(false);
                Destroy(obj);
            }
        }
        GameObject NewShelf = new GameObject(ShelfId);
        MeshFilter ShelfMeshFilter = NewShelf.AddComponent<MeshFilter>();
        MeshRenderer ShelfMeshRenderer = NewShelf.AddComponent<MeshRenderer>();

        Shelf TaggedShelf = NewShelf.AddComponent<Shelf>();
        TaggedShelf.id = ShelfId;
        TaggedShelf.length = length;
        TaggedShelf.width = width;
        TaggedShelf.height = height;
        TaggedShelf.thickness = thickness;
        TaggedShelf.level = level;
        TaggedShelf.rotation = rotation;

        shelves[ShelfId] = NewShelf;

        NewShelf.transform.position = new Vector3(x, 0, z);
        NewShelf.transform.rotation = Quaternion.Euler(0, rotation, 0);
        Mesh combinedMesh = new Mesh();
        combinedMesh.CombineMeshes(combine.ToArray(), true, true);
        ShelfMeshFilter.mesh = combinedMesh;

        MeshCollider ShelfMeshCollider = NewShelf.AddComponent<MeshCollider>();
        ShelfMeshCollider.sharedMesh = combinedMesh;

        ShelfMeshRenderer.materials = Panels[0].GetComponent<MeshRenderer>().materials;

        if (DoorType == "LeftHingeDoor")
            {
                Vector3 DoorPosition = NewShelf.transform.position + NewShelf.transform.rotation * new Vector3(0, (thickness/2+(height+thickness)*level)/2, -(width + 2*thickness) / 2);
                GameObject Door = Instantiate(LeftHingeDoor, DoorPosition, NewShelf.transform.rotation);
                Door.transform.localScale = new Vector3(length, thickness/2+(height+thickness)*level, 1);
                Door.transform.SetParent(shelves[ShelfId].transform);

                Rigidbody rb = Door.AddComponent<Rigidbody>();
                rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;

                XRGrabInteractable grabInteractable = Door.AddComponent<XRGrabInteractable>();
                grabInteractable.movementType = XRBaseInteractable.MovementType.VelocityTracking;

                HingeJoint hingeJoint = Door.AddComponent<HingeJoint>();
                hingeJoint.anchor = new Vector3(-0.5f, 0, 0);
                hingeJoint.axis = new Vector3(0, 1, 0);
                hingeJoint.limits = new JointLimits { min = 0, max = 120 };
                hingeJoint.useLimits = true;
            }

        if (DoorType == "RightHingeDoor")
            {
                Vector3 DoorPosition = NewShelf.transform.position + NewShelf.transform.rotation * new Vector3(0, (thickness/2+(height+thickness)*level)/2, -(width + 2*thickness) / 2);
                GameObject Door = Instantiate(RightHingeDoor, DoorPosition, NewShelf.transform.rotation);
                Door.transform.localScale = new Vector3(length, thickness/2+(height+thickness)*level, 1);
                Door.transform.SetParent(shelves[ShelfId].transform);

                Rigidbody rb = Door.AddComponent<Rigidbody>();
                rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;

                XRGrabInteractable grabInteractable = Door.AddComponent<XRGrabInteractable>();
                grabInteractable.movementType = XRBaseInteractable.MovementType.VelocityTracking;

                HingeJoint hingeJoint = Door.AddComponent<HingeJoint>();
                hingeJoint.anchor = new Vector3(0.5f, 0, 0);
                hingeJoint.axis = new Vector3(0, 1, 0);
                hingeJoint.limits = new JointLimits { min = -120, max = 0 };
                hingeJoint.useLimits = true;
            }
            
        else if (DoorType == "SlidingDoor")
        {
            Vector3 DoorPosition = NewShelf.transform.position + NewShelf.transform.rotation * new Vector3(0, (thickness/2+(height+thickness)*level)/2, -(width + 5*thickness) / 2);
            GameObject Door = Instantiate(SlidingDoor, DoorPosition, NewShelf.transform.rotation);
            Door.transform.localScale = new Vector3(length, thickness/2+(height+thickness)*level, 1);
            Door.transform.SetParent(shelves[ShelfId].transform);
        }
    }

    public void SpawnShelfGroup(string ShelfId, float CenterX, float CenterY, float ShelfWidth, float ShelfHeight, float ShelfThickness, int ShelfLevel, float ShelfLength, float Rotation, bool SavePrefab = false){
        float ShelfLengthSide = (ShelfWidth+ShelfThickness)*2;

        SpawnShelf(ShelfId+"_a", 0, - 0.5f*(ShelfWidth + ShelfThickness), ShelfLength, ShelfWidth, ShelfHeight, ShelfThickness, ShelfLevel, 0, "None", SavePrefab);
        SpawnShelf(ShelfId+"_b", 0, 0.5f*(ShelfWidth + ShelfThickness), ShelfLength, ShelfWidth, ShelfHeight, ShelfThickness, ShelfLevel, 180, "None", SavePrefab);
        SpawnShelf(ShelfId+"_c", -(ShelfThickness+ShelfLength+ShelfWidth)/2, 0, ShelfLengthSide, ShelfWidth, ShelfHeight, ShelfThickness, ShelfLevel, 90, "None", SavePrefab);
        SpawnShelf(ShelfId+"_d", (ShelfThickness+ShelfLength+ShelfWidth)/2, 0, ShelfLengthSide, ShelfWidth, ShelfHeight, ShelfThickness, ShelfLevel, 270, "None", SavePrefab);
        
        GameObject shelfGroup = new GameObject(ShelfId + "_Group");
        foreach (var shelf in new[] { ShelfId + "_a", ShelfId + "_b", ShelfId + "_c", ShelfId + "_d" })
        {
            shelves[shelf].transform.SetParent(shelfGroup.transform);
        }

        shelfGroup.transform.position = new Vector3(CenterX, 0, CenterY);
        shelfGroup.transform.rotation = Quaternion.Euler(0, Rotation, 0);
        
    }

    public void SpawnProducts(int seed, string ShelfId, float ProductOrientation, List<string> Categ, bool random = false)
    {
        // Partitions the shelf into sections based on the number of categories and fills each section with products from the corresponding category
        // Partitions vertically

        // Verify and print all valid categories
        foreach (string category in Categ)
        {
            if (!this.Categories.ContainsKey(category))
            {
                Debug.LogError("Invalid category: " + category + ". Cancelling action.");
                return;
            }
            else
            {
                Debug.Log("Valid category: " + category);
            }
        }

        Random.InitState(seed);
        GameObject shelf = shelves[ShelfId];
        float length = shelf.GetComponent<Shelf>().length;
        float width = shelf.GetComponent<Shelf>().width;
        float height = shelf.GetComponent<Shelf>().height;
        float thickness = shelf.GetComponent<Shelf>().thickness;
        int level = shelf.GetComponent<Shelf>().level;
        float PartitionLength = length / Categories.Count;
        int Partitions = Mathf.FloorToInt(Categories.Count);
        Debug.Log("Shelf length: " + length + ", Shelf width: " + width + ", Shelf level: " + level + ", Partitions: " + Partitions);

        Transform shelfTransform = shelf.transform;
        Vector3 shelfRight = shelfTransform.right;  // Use the local right direction
        Vector3 shelfForward = shelfTransform.forward;  // Use the local forward direction based on current rotation
        Vector3 shelfLeftPosition = shelfTransform.position - (shelfRight * (length / 2));  // Calculate the leftmost position of the shelf
        float shelfDownY = shelfTransform.position.y + (shelfTransform.localScale.y / (level+1));  // Calculate the bottom y position of the shelf
        Vector3 shelfBackPosition = shelfTransform.position - (shelfForward * (width / 2));
        Vector3 shelfLeftBackPosition = shelfBackPosition - (shelfRight * (length / 2));  // Calculate the left backmost position of the shelf
        float buffer = 0.03f;  // Buffer space between items

        Debug.Log($"Forward vector: {shelfForward}, Right vector: {shelfRight}, Left position: {shelfLeftPosition}, Down y: {shelfDownY}, Back position: {shelfBackPosition}");
        for(int i = 0; i<level; i++)
        {
            float spaceTaken = 0;
            float spaceTakenDepth = 0;
            List<(GameObject, float)> firstRowItems = new List<(GameObject, float)>();

            while (spaceTaken < length)
            {
                List<GameObject> Products = new List<GameObject>();
                foreach (var sublist in Categories[Categ[Mathf.FloorToInt(spaceTaken/PartitionLength)]])
                {
                    Products.AddRange(sublist);
                }
                GameObject item = Products[Random.Range(0, Products.Count)];
                MeshRenderer itemRenderer = item.GetComponent<MeshRenderer>();
                float itemLength;
                float itemDepth;
                // Adjust item length and depth based on ProductOrientation
                if (ProductOrientation == 90 || ProductOrientation == 270)
                {
                    itemLength = itemRenderer.bounds.size.z;
                    itemDepth = itemRenderer.bounds.size.x;
                }
                else if (ProductOrientation == 0 || ProductOrientation == 180)
                {
                    itemLength = itemRenderer.bounds.size.x;
                    itemDepth = itemRenderer.bounds.size.z;
                }
                else
                {
                    Debug.LogError("Invalid ProductOrientation.");
                    return;
                }
                Debug.Log($"Item: {item.name}, Length: {itemLength}, Depth: {itemDepth}");

                if (spaceTaken + itemLength <= length)
                {
                    // Calculate position for the item
                    Vector3 position = shelfLeftBackPosition + (shelfRight * (spaceTaken + (itemLength / 2) + buffer));
                    position.y = i*(height+thickness)+shelfDownY;  // Use the calculated bottom y position of the shelf
                    position += shelfForward * (itemDepth / 2);  // Adjust position based on item depth

                    // Create a rotation of -90 degrees on the y-axis, limited to the shelf's y-axis rotation
                    Quaternion rotation = Quaternion.LookRotation(shelfForward, Vector3.up) * Quaternion.Euler(0, ProductOrientation, 0);

                    // Instantiate the item with the calculated position and rotation
                    GameObject instantiatedItem = Instantiate(item, position, rotation);
                    instantiatedItem.tag = "Grippable";
                    firstRowItems.Add((instantiatedItem, itemDepth));
                    Debug.Log($"Placed {item.name} at position: {position} with length {itemLength}");

                    // Move to the next position
                    spaceTaken += itemLength + buffer;
                }
                else
                {
                    spaceTaken += itemLength;
                    Debug.Log($"Item {item.name} does not fit on the shelf, stopping arrangement.");
                    break;
                }
            }

            // Copy the first row items to fill the depth of the shelf
            foreach (var (item, itemDepth) in firstRowItems)
            {
                spaceTakenDepth = itemDepth + buffer;

                while (spaceTakenDepth < width)
                {
                    if (spaceTakenDepth + itemDepth <= width)
                    {
                        Vector3 position = item.transform.position + (shelfForward * spaceTakenDepth);
                        Quaternion rotation = item.transform.rotation;

                        Instantiate(item, position, rotation);
                        Debug.Log($"Copied {item.name} to position: {position}");

                        spaceTakenDepth += itemDepth + buffer;
                    }
                    else
                    {
                        spaceTakenDepth += itemDepth;
                    }
                }
            }
        }

        // Spawn price tags for all grocery items in the given categories

        foreach (var category in Categ)
        {
            int Counter = 0;
            foreach (var sublist in Categories[category])
            {
            Debug.Log("Category: " + category + ", Sublist count: " + sublist.Count);
            foreach (var product in sublist)
                {
                    string productName = product.name;
                    float price = priceDictionary[productName];
                    string unit = "pc";
                    float centerX = -length / 2 + 0.071f * (Counter + 1) + Categ.IndexOf(category) * length / Categ.Count;
                    float centerY = (thickness + height) * (level - 1 - Mathf.Floor(Counter * 0.071f / (length / Categ.Count))) + thickness / 2;
                    float centerZ = -width / 2;

                    // Check if the product is instantiated
                    if (GameObject.Find(productName+"(Clone)") != null)
                    {
                    SpawnPriceTag(ShelfId, productName, price, unit, centerX, centerY, centerZ);
                    }
                    Counter++;
                }
            }
        }
    }

    public void SpawnPriceTag(string ShelfId, string ProductName, float Price, string Unit, float CenterX, float CenterY, float CenterZ)    
    {
        GameObject PriceTagInstance = Instantiate(PriceTag);
        PriceTag PriceTagComponent = PriceTagInstance.AddComponent<PriceTag>();
        PriceTagComponent.ProductName = ProductName;
        PriceTagComponent.Price = Price;
        PriceTagComponent.Unit = Unit;
        TMPro.TextMeshProUGUI productNameText = PriceTagInstance.transform.Find("Canvas/Product Name").GetComponent<TMPro.TextMeshProUGUI>();
        TMPro.TextMeshProUGUI priceText = PriceTagInstance.transform.Find("Canvas/Price").GetComponent<TMPro.TextMeshProUGUI>();

        if (productNameText != null)
        {
            productNameText.text = ProductName;
        }
        else
        {
            Debug.LogError("ProductNameText component not found on PriceTagInstance.");
        }

        if (priceText != null)
        {
            priceText.text = Price.ToString("F2") + " / " + Unit;
        }
        else
        {
            Debug.LogError("PriceText component not found on PriceTagInstance.");
        }
        PriceTagInstance.transform.SetParent(shelves[ShelfId].transform);
        PriceTagInstance.transform.localPosition = new Vector3(CenterX, CenterY, CenterZ - 0.001f);
        PriceTagInstance.transform.rotation = shelves[ShelfId].transform.rotation;
    }

    public void RandomizePrices(int seed)
    {
        Random.InitState(seed); // Set a fixed seed for reproducibility
        foreach (var category in groceryData.Categories)
        {
            foreach (var item in category.Items)
            {
            float randomPrice = Random.Range(0, 500.0f); // Generate a random price between 1 and 20
            priceDictionary.Add(item, randomPrice);
            }
        }
    }

    public void ResetEnvironment()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
    }

    public void SwitchEnvironment(string sceneName)
    {
            if (Application.CanStreamedLevelBeLoaded(sceneName))
            {
                UnityEngine.SceneManagement.SceneManager.LoadScene(sceneName);
            }
            else
            {
                Debug.LogError("Scene " + sceneName + " does not exist!");
            }
    }
    
    [System.Serializable]
    public class Products
    {
        public string Category;
        public List<string> Items;
    }
}