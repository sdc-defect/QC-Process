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
        {// 그냥 R 키 누르면 실행
            try
            {
                Process psi = new Process();
                psi.StartInfo.FileName = "C:/Program Files/Python37/python.exe";
                // 파이썬 환경 연결
                psi.StartInfo.Arguments = "C:/Users/multicampus/Desktop/socket/testUI.py";
                // 실행할 파이썬 파일
                psi.StartInfo.CreateNoWindow = true;
                // 새창에서 시작 걍 일케 두는듯

                psi.StartInfo.UseShellExecute = false;
                // 프로세스를 시작할때 운영체제 셸을 사용할지 이것도 걍 일케 두는듯
                psi.Start();

                UnityEngine.Debug.Log("[알림] testUI.py file 실행");
            }
            catch (Exception e)
            {
                UnityEngine.Debug.LogError("[알림] 에러발생: " + e.Message);
            }
        }


    }
}
