using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConvayorBelt4 : MonoBehaviour
{
   public float speed = 4f;
    private float fTime = 0.00f;
    Rigidbody rBody;

    // Start is called before the first frame update
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
        fTime = 4f;
        speed = 4f;

    }

    // Update is called once per frame
    void FixedUpdate()
    {
        fTime += Time.fixedDeltaTime;

        // Debug.Log(fTime);

        fTime = 0.00f;

        Vector3 pos = rBody.position;
        rBody.position += Vector3.right * speed * Time.fixedDeltaTime;
        rBody.MovePosition(pos);
    }
}
