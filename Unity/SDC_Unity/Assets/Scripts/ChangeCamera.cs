using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeCamera : MonoBehaviour
{
	public Camera MiniCam;

	void Update ()
	{
		if( Input.GetButtonUp("Fire3"))
		{
			MiniCam.enabled = !MiniCam.enabled;

		}
	}
}