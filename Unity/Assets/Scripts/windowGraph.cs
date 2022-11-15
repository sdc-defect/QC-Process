using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using CodeMonkey.Utils;

public class windowGraph : MonoBehaviour
{
	[SerializeField] private Sprite circleSprite;
	private RectTransform graphContainer;
	public static List<int> valueList = new List<int>() {};
	private void Awake() 
	{
		graphContainer = transform.Find("graphContainer").GetComponent<RectTransform>();
		// CreateCircle(new Vector2(200, 200));
		// List<int> valueList = new List<int>() {99, 98, 97, 96, 85, 56, 45, 30, 22, 17, 15,13, 17,25,37,40, 36, 33 };
		// ShowGraph(valueList);
	}

	void Start()
	{	
	}

	void Update()
	{	
		GameObject obj1 = GameObject.Find("graphContainer");
		Transform[] childList = obj1.GetComponentsInChildren<Transform>();
		if (childList != null)
		{
			for (int i = 4; i < childList.Length; i++)
			{
				if (childList[i] != transform)
					Destroy(childList[i].gameObject);
			}
		}

		ShowGraph(valueList);
	}

	private GameObject CreateCircle(Vector2 anchoredPosition)
	{
		GameObject gameObject = new GameObject("circle", typeof(Image));
		gameObject.GetComponent<Image>().color = new Color(0, 0, 0, 1);
		gameObject.transform.SetParent(graphContainer, false);
		gameObject.GetComponent<Image>().sprite = circleSprite;
		RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
		rectTransform.anchoredPosition = anchoredPosition;
		rectTransform.sizeDelta = new Vector2(5, 5);
		rectTransform.anchorMin = new Vector2(0, 0);
		rectTransform.anchorMax = new Vector2(0, 0);
		return gameObject;
	}

	private void ShowGraph(List<int> valueList)
	{
		float graphHeight = graphContainer.sizeDelta.y;
		float yMaximum = 100f;
		float xSize = 18f;
		
		GameObject lastCircleGameObject = null;
		for (int i = 0; i < valueList.Count; i++)
		{
			float xPosition = i * xSize;
			float yPosition = (valueList[i] / yMaximum) * graphHeight;
			GameObject circleGameObject = CreateCircle(new Vector2(xPosition, yPosition));
			if (lastCircleGameObject != null)
			{
				CreateDotConnection(lastCircleGameObject.GetComponent<RectTransform>().anchoredPosition, circleGameObject.GetComponent<RectTransform>().anchoredPosition);
			}
			lastCircleGameObject = circleGameObject;
		}
	}

	private void CreateDotConnection (Vector2 dotPositionA, Vector2 dotPositionB)
	{
		GameObject gameObject = new GameObject("dotConnetion", typeof(Image));
		gameObject.transform.SetParent(graphContainer, false);
		gameObject.GetComponent<Image>().color = new Color(0, 0, 0, 1);
		RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
		Vector2 dir = (dotPositionB - dotPositionA).normalized;
		float distance = Vector2.Distance(dotPositionA, dotPositionB);
		rectTransform.anchorMin = new Vector2(0, 0);
		rectTransform.anchorMax = new Vector2(0, 0);
		rectTransform.sizeDelta = new Vector2(distance, 3f);
		rectTransform.anchoredPosition = dotPositionA + dir * distance * .5f;
		rectTransform.localEulerAngles = new Vector3(0, 0, UtilsClass.GetAngleFromVectorFloat(dir));
	}


}