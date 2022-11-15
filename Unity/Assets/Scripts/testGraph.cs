using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using CodeMonkey.Utils;

public class testGraph : MonoBehaviour
{
    [SerializeField] private Sprite dotSprite;
    private RectTransform barContainer;
    private List<GameObject> gameObjectList;
    List<int> valueList = new List<int>() { 97, 96, 94, 100, 94, 89, 97, 95, 99, 100 };

	
	private void Awake()
	{
		barContainer = transform.Find("barContainer").GetComponent<RectTransform>();

        gameObjectList = new List<GameObject>();

        ShowGraph(valueList, -1);
	}

	void Update()
	{	
    	GameObject obj1 = GameObject.Find("barContainer");
		Transform[] childList = obj1.GetComponentsInChildren<Transform>();
		if (childList != null)
		{
			for (int i = 4; i < childList.Length; i++)
			{
				if (childList[i] != transform)
					Destroy(childList[i].gameObject);
			}
		}
        if (ConvayorBelt2.denominator != 0)
        {
            valueList[9] = (ConvayorBelt2.numerator * 100) / ConvayorBelt2.denominator;
        }
        ShowGraph(valueList, -1);

		// ShowGraph(windowGraph.valueList);
       //ShowGraph(windowGraph.valueList, -1);

	}

	private void ShowGraph(List<int> valueList, int maxVisibleValueAmount = -1)
    {
        float xSize = 20f;
        if (maxVisibleValueAmount <= 0) {
            maxVisibleValueAmount = valueList.Count;
        }

        foreach (GameObject gameObject in gameObjectList) {
            Destroy(gameObject);
        }
        gameObjectList.Clear();
        
        float graphWidth = barContainer.sizeDelta.x;
        float graphHeight = barContainer.sizeDelta.y;

        float yMaximum = valueList[0];
        float yMinimum = valueList[0];
        
        for (int i = Mathf.Max(valueList.Count - maxVisibleValueAmount, 0); i < valueList.Count; i++) {
            int value = valueList[i];
            if (value > yMaximum) {
                yMaximum = value;
            }
            if (value < yMinimum) {
                yMinimum = value;
            }
        }

        float yDifference = yMaximum - yMinimum;
        if (yDifference <= 0) {
            yDifference = 5f;
        }
        yMaximum = yMaximum + (yDifference * 0.2f);
        yMinimum = yMinimum - (yDifference * 0.2f);

        yMinimum = 0f; // Start the graph at zero

        // float xSize = graphWidth / (maxVisibleValueAmount + 1);

        int xIndex = 0;

        //GameObject lastDotGameObject = null;
        for (int i = Mathf.Max(valueList.Count - maxVisibleValueAmount, 0); i < valueList.Count; i++) {
            float xPosition = 9 + i * xSize;
            float yPosition = ((valueList[i] - yMinimum) / (yMaximum - yMinimum)) * graphHeight;
            GameObject barGameObject = CreateBar(new Vector2(xPosition, yPosition), xSize * .9f);
            gameObjectList.Add(barGameObject);
            /*
            GameObject dotGameObject = CreateDot(new Vector2(xPosition, yPosition));
            gameObjectList.Add(dotGameObject);
            if (lastDotGameObject != null) {
                GameObject dotConnectionGameObject = CreateDotConnection(lastDotGameObject.GetComponent<RectTransform>().anchoredPosition, dotGameObject.GetComponent<RectTransform>().anchoredPosition);
                gameObjectList.Add(dotConnectionGameObject);
            }
            lastDotGameObject = dotGameObject;
            */
        }

    }


	private GameObject CreateDot(Vector2 anchoredPosition)
	{
		GameObject gameObject = new GameObject("dot", typeof(Image));
		gameObject.GetComponent<Image>().color = new Color(0, 0, 0, 1);
		gameObject.transform.SetParent(barContainer, false);
		gameObject.GetComponent<Image>().sprite = dotSprite;
		RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
		rectTransform.anchoredPosition = anchoredPosition;
		rectTransform.sizeDelta = new Vector2(5, 5);
		rectTransform.anchorMin = new Vector2(0, 0);
		rectTransform.anchorMax = new Vector2(0, 0);
		return gameObject;
	}

	private void CreateDotConnection (Vector2 dotPositionA, Vector2 dotPositionB)
	{
		GameObject gameObject = new GameObject("dotConnetion", typeof(Image));
		gameObject.transform.SetParent(barContainer, false);
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

    private GameObject CreateBar(Vector2 graphPosition, float barWidth) 
	{
        GameObject gameObject = new GameObject("bar", typeof(Image));
		gameObject.GetComponent<Image>().color = new Color(0, 0, 0, 1);
        gameObject.transform.SetParent(barContainer, false);
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        rectTransform.anchoredPosition = new Vector2(graphPosition.x, 0f);
        rectTransform.sizeDelta = new Vector2(barWidth, graphPosition.y);
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
        rectTransform.pivot = new Vector2(.5f, 0f);
        return gameObject;
    }
}
