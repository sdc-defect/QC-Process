using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeCamera : MonoBehaviour
{
	public Camera[] arrCam; //ī�޶� ��ҵ��� �߰��Ѵ�.
	int nCamCount = 2;
	int nNowCam = 0;

	void Update ()
	{
		if( Input.GetButtonUp("Fire3"))
		{
			++nNowCam;
			if (nNowCam >= nCamCount)
			{
				nNowCam = 0;
			}
			for ( int i=0; i<arrCam.Length; ++i )
			{
				arrCam[i].enabled = (i == nNowCam);
			}
		}
	}
}