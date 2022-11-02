using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConvayorBelt2 : MonoBehaviour
{
    public float speed;
    private float fDelayTime = 2f;
    private float fTime = 0.00f;
    public GameObject Product;
    Rigidbody rBody;

    // Start is called before the first frame update
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
        fTime = 6f;
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        fTime += Time.fixedDeltaTime;
        
        // Debug.Log(fTime);

        if (fTime >= fDelayTime)
        {
            
            Vector3 pos = rBody.position;
            rBody.position += Vector3.right * speed * Time.fixedDeltaTime;
            rBody.MovePosition(pos);
            
            if (fTime >= 6)
            {
                Instantiate(Product);
                fTime = 0.00f;
            }

            if (fTime < 2.03)
            {
                StartCoroutine ("Rendering");
            }
        }
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
