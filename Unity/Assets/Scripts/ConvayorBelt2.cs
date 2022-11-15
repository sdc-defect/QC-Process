using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using UnityEngine.UI;
using System.Diagnostics;
using System.Threading;

public class ConvayorBelt2 : MonoBehaviour
{
    public float speed;
    private float fDelayTime = 2f;
    private float fTime = 0.00f;
    public GameObject Product;
    Rigidbody rBody;
    public Material[] mat = new Material[13];
    bool isCapture = true;
    bool isFirstCapture = true;
    int i = 0;

    // 통신 변수
    Thread mThread;
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 25001;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    Vector3 receivedPos = Vector3.zero;
    
    byte[] sendImgBytes;
    bool running;

    public static bool direction = false;


    // 그래프 변수
    
    public static int denominator = 0;
    public static int numerator = 0;

    // 로그 변수
    public Text logText;

    // Start is called before the first frame update
    void Start()
    {
        rBody = GetComponent<Rigidbody>();
        fTime = 6f;

        // 통신 로직
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        fTime += Time.fixedDeltaTime;
        
        // Debug.Log(fTime);

        // UnityEngine.Debug.Log(sendImgBytes);

        if (fTime >= fDelayTime)
        {
            
            Vector3 pos = rBody.position;
            rBody.position += Vector3.right * speed * Time.fixedDeltaTime;
            rBody.MovePosition(pos);
            
            if (fTime >= 6)
            {
                // print(i);
                i = ++i % 13;
                GameObject create = Instantiate(Product);
                create.gameObject.GetComponent<MeshRenderer>().material = mat[i];
                fTime = 0.00f;
                isCapture = true;

            }
            // print(fTime);
            if (fTime != 0 && isCapture)
            {
                denominator++;
                if (i == 3)
                {
                    direction = true;
                    logText.text += "2022-11-09_04:55:43:907 파일명: 2022_11_09_04_55_43_907 불품 ";
                }
                else 
                {
                    numerator++;
                    direction = false;
                    logText.text += "2022-11-09_04:55:43:907 파일명: 2022_11_09_04_55_43_907 양품 ";

                }
                windowGraph.valueList.Add((numerator * 100) / denominator);

                isCapture = false;
                StartCoroutine ("Rendering");
            }
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            try
            {
                Process psi = new Process();
                psi.StartInfo.FileName = "C:/Program Files/Python37/python.exe";
                // 파이썬 환경 연결
                psi.StartInfo.Arguments = "C:/Users/multicampus/Desktop/socket/server.py";
                // 실행할 파이썬 파일
                psi.StartInfo.CreateNoWindow = true;
                // 새창에서 시작

                psi.StartInfo.UseShellExecute = false;
                // 프로세스를 시작할때 운영체제 셸을 사용할지
                // psi.Start();
                psi.Kill();
                UnityEngine.Debug.Log("[알림] server.py file 실행");

            }
            catch (Exception e)
            {
                UnityEngine.Debug.LogError("[알림] 에러발생: " + e.Message);
            }
        }

        if (Input.GetKeyDown(KeyCode.T))
        {
            Application.Quit();
            UnityEngine.Debug.Log("[알림] server.py file 종료");
        }
    }

    IEnumerator Rendering() 
    {
        if (isFirstCapture)    
        {
            isFirstCapture = false;
            
        }
        else
        {
            yield return new WaitForEndOfFrame ();

            byte[] imgBytes;
            string path = string.Format(@"C:\ok{0}.png", i);
            Texture2D texture = new Texture2D (Screen.width/10 * 2, Screen.height /10 * 4, TextureFormat.RGB24, false);
            texture.ReadPixels (new Rect (0, 0, Screen.width, Screen.height), 0, 0, false);
            texture.Apply ();
            imgBytes = texture.EncodeToJPG ();
            sendImgBytes = imgBytes; 
 

            //  Debug.Log(imgBytes.Length);

            System.IO.File.WriteAllBytes (path, imgBytes);
            // Debug.Log(path + "has been saved");

        }
    }

    void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            SendAndReceiveData();
        }
        listener.Stop() ;
    }

    void SendAndReceiveData()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        //---receiving Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (dataReceived != null)
        {
            //---Using received data---
            receivedPos = StringToVector3(dataReceived); //<-- assigning receivedPos value from Python
            // print(receivedPos);
            // print("received pos data, and moved the Cube!");

            //---Sending Data to Host----
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes("Hey I got your message Python! Do You see this massage?"); //Converting string to byte data
            

        }
        while(sendImgBytes == null) 
        {

        }
        // UnityEngine.Debug.Log("여기");
        // UnityEngine.Debug.Log(sendImgBytes);
        // UnityEngine.Debug.Log(sendImgBytes.Length);
            
        // nwStream.Write(sendImgBytes, 0, sendImgBytes.Length); //Sending the data in Bytes to Python
        nwStream.Write(sendImgBytes); //Sending the data in Bytes to Python
        sendImgBytes = null;

    }
    public static Vector3 StringToVector3(string sVector)
    {
        // Remove the parentheses
        if (sVector.StartsWith("(") && sVector.EndsWith(")"))
        {
            sVector = sVector.Substring(1, sVector.Length - 2);
        }

        // split the items
        string[] sArray = sVector.Split(',');

        // store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(sArray[0]),
            float.Parse(sArray[1]),
            float.Parse(sArray[2]));

        return result;
    }
}
