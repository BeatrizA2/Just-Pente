using UnityEngine;
using TMPro;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class Score : MonoBehaviour
{
    public TextMeshProUGUI scoreText;

    // Porta para ouvir o comparisonValue
    public int listenPort = 25001;
    private TcpListener listener;
    private string comparisonValue = "0";
    TcpClient client;

    private void Start()
    {
        // Inicia a escuta na porta especificada
        listener = new TcpListener(IPAddress.Any, listenPort);
        listener.Start();

        // Inicia uma thread para receber o comparisonValue
        ThreadStart ts = new ThreadStart(ReceiveComparisonValue);
        Thread thread = new Thread(ts);
        client = listener.AcceptTcpClient();
        thread.Start();
    }

    private void ReceiveComparisonValue()
    {
        while (true)
        {

            NetworkStream stream = client.GetStream();

            // Lê os dados recebidos
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string comparisonValueStr = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            comparisonValue = comparisonValueStr;

            
        }
        
    }

    // Update is called once per frame
    void Update()
    {
        scoreText.text = comparisonValue;
    }

    private void OnDestroy()
    {
        // Fecha a conexão
        client.Close();
        // Fecha a escuta quando o objeto for destruído
        listener.Stop();
    }
}
