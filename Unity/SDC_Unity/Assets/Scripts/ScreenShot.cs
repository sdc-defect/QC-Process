using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScreenShot : MonoBehaviour
{
    private void Awake()
    {
        StartCoroutine ("Rendering");
    }

    IEnumerator Rendering() 
    {
        yield return new WaitForEndOfFrame ();

        byte[] imgBytes;
        string path = @"C:\test.png";

        Texture2D texture = new Texture2D (Screen.width/10 * 2, Screen.height /10 * 4, TextureFormat.RGB24, false);
        texture.ReadPixels (new Rect (0, 0, Screen.width, Screen.height), 0, 0, false);
        texture.Apply ();

        imgBytes = texture.EncodeToJPG ();
        System.IO.File.WriteAllBytes (path, imgBytes);
        Debug.Log(path + "has been saved");
    }
}
