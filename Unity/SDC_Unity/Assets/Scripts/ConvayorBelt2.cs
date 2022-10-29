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
        fTime = 4f;
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        fTime += Time.fixedDeltaTime;
        
        Debug.Log(fTime);

        if (fTime >= fDelayTime)
        {
            Vector3 pos = rBody.position;
            rBody.position += Vector3.back * speed * Time.fixedDeltaTime;
            rBody.MovePosition(pos);

            if (fTime >= 4)
            {
                Instantiate(Product);

                fTime = 0.00f;
            }
        }
    }
}
