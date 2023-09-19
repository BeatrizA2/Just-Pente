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
    private float comparisonValue = 0f;

    private void Start()
    {
        // Inicia a escuta na porta especificada
        listener = new TcpListener(IPAddress.Any, listenPort);
        listener.Start();

        // Inicia uma thread para receber o comparisonValue
        ThreadStart ts = new ThreadStart(ReceiveComparisonValue);
        Thread thread = new Thread(ts);
        thread.Start();
    }

    private void ReceiveComparisonValue()
    {
        while (true)
        {
            // Aceita uma conexão do Python
            TcpClient client = listener.AcceptTcpClient();
            NetworkStream stream = client.GetStream();

            // Lê os dados recebidos
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string comparisonValueStr = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            // Converte a string de volta para um float
            if (float.TryParse(comparisonValueStr, out float value))
            {
                // Atualiza o comparisonValue
                comparisonValue = value;
            }

            // Fecha a conexão
            client.Close();
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Define o texto do TextMeshProUGUI com base no comparisonValue
        scoreText.text = comparisonValue.ToString("F2"); // Formata para exibir duas casas decimais
    }

    private void OnDestroy()
    {
        // Fecha a escuta quando o objeto for destruído
        listener.Stop();
    }
}
