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
            // �ó׸ӽ� ��ü�� �����Ϸ��� �̷��� �ص� �ȴ�.
            // cinevirtual.m_Lens.FieldOfView = 60;
    
            // ������ transposer �� follow offset�� �����Ϸ��� �Ʒ��� ���� ������Ʈ�� ��������
            // ������� �����;� �Ѵ�.
            // cinevirtual.GetCinemachineComponent<CinemachineTransposer>().m_FollowOffset.y = 10;
        }
    }
}