using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OpenPyQT : MonoBehaviour
{   
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Escape))
        {
            var obj = GameObject.Find("Canvas").transform.Find("PyQTScreen");
            print(obj);
            obj.gameObject.SetActive(false);
        }
    }

}
