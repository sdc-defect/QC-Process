using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;

public class Test : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
        {// �׳� R Ű ������ ����
            try
            {
                Process psi = new Process();
                psi.StartInfo.FileName = "C:/Program Files/Python37/python.exe";
                // ���̽� ȯ�� ����
                psi.StartInfo.Arguments = "C:/Users/multicampus/Desktop/socket/testUI.py";
                // ������ ���̽� ����
                psi.StartInfo.CreateNoWindow = true;
                // ��â���� ���� �� ���� �δµ�

                psi.StartInfo.UseShellExecute = false;
                // ���μ����� �����Ҷ� �ü�� ���� ������� �̰͵� �� ���� �δµ�
                psi.Start();

                UnityEngine.Debug.Log("[�˸�] testUI.py file ����");
            }
            catch (Exception e)
            {
                UnityEngine.Debug.LogError("[�˸�] �����߻�: " + e.Message);
            }
        }


    }
}
