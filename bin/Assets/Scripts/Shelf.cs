using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Shelf : MonoBehaviour
{
    public string id;
    public float length;
    public float width;
    public float height;
    public float thickness;
    public int level;
    public float rotation;
    public List<(string Id, float Length, float Width, float XCenter, float ZCenter)> Partitions;
}