using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Cinemachine;

public class HoldCamera : MonoBehaviour
{
    public CinemachineVirtualCamera cinevirtual;

    void Update()
    {
        if(Input.GetButtonUp("Fire2"))
        {
            cinevirtual.gameObject.SetActive(false);
            // 시네머신 자체에 접근하려면 이렇게 해도 된다.
            // cinevirtual.m_Lens.FieldOfView = 60;
    
            // 하지만 transposer 의 follow offset에 접근하려면 아래와 같이 컴포넌트를 가져오는
            // 방식으로 가져와야 한다.
            // cinevirtual.GetCinemachineComponent<CinemachineTransposer>().m_FollowOffset.y = 10;
        }
    }
}