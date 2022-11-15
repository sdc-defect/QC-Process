using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Cinemachine;

public class ChangeCamera : MonoBehaviour
{
	public Camera MiniCam;
	public GameObject UI;
	bool isOpenUI = true;
    public CinemachineVirtualCamera cinevirtual;

	void Update ()
	{
		if( Input.GetButtonUp("Fire3"))
		{
			MiniCam.enabled = !MiniCam.enabled;

		}

		if( Input.GetButtonUp("Fire2") && isOpenUI == false)
		{
			UI.transform.GetChild(0).gameObject.SetActive(false);
			cinevirtual.gameObject.SetActive(true);
			isOpenUI = true;
		}
		else if( Input.GetButtonUp("Fire2") && isOpenUI == true)
		{
			GameObject.Find("Canvas").transform.Find("Panel").gameObject.SetActive(true);
			cinevirtual.gameObject.SetActive(false);
			//UI.transform.GetChild(0).gameObject.SetActive(false);
			isOpenUI = false;
		}
		// Debug.Log(isOpenUI);

		if (Input.GetKeyDown(KeyCode.Escape))
		{ 
			Application.Quit();
		}

	}
}