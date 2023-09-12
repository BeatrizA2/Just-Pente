using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;

public class AnimationTCP : MonoBehaviour
{
    public GameObject[] Body;
    int counter = 0;

    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;

    List<string> receivedLines = new List<string>(); // Store received lines

    // Start is called before the first frame update
    void Start()
    {
        // Start receiving positions on a separate thread
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.Start();
    }

    void GetData()
    {
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        client = server.AcceptTcpClient();

        running = true;
        while (running)
        {
            Connection();
        }
        server.Stop();
    }

    void Connection()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);


        if (!string.IsNullOrEmpty(dataReceived))
        {
            receivedLines.AddRange(dataReceived.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries));
            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (counter < receivedLines.Count)
        {
            string[] aux = receivedLines[counter].Split('"');
            string[] points = aux[1].Split(',');



            for (int i = 0; i <= 32; i++)
            {
                float x = float.Parse(points[0 + i * 3]) / 100;
                print(x);
                float y = float.Parse(points[1 + i * 3]) / 100;
                float z = float.Parse(points[2 + i * 3]) / 300;

                Body[i].transform.localPosition = new Vector3(x, y, z);
            }

            counter++;
        }
    }

    private void OnDestroy()
    {
        running = false;
        thread.Join();
    }
}
