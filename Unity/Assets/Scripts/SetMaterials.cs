using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SetMaterials : MonoBehaviour
{
    public Material[] mat = new Material[3];
 
    int i = 0;
 
    public void ChangeCubeMat()
    {
        i = ++i % 3;
 
        // Change Material
        gameObject.GetComponent<MeshRenderer>().material = mat[i];
    }

    void Update()
    {
        ChangeCubeMat();
    }
}
