using UnityEngine;
using UnityEngine.SceneManagement;
using System.Text;

public class SwipeManager : MonoBehaviour
{
    public void LoadDanceScene(string buttonText)
    {
        // Salva o texto do botão no PlayerPrefs
        PlayerPrefs.SetString("Button_Text", buttonText);

        // Envia o texto do botão para o Python via TCP
        SendButtonTextToPython(buttonText);

        // Carrega a cena "Dance"
        SceneManager.LoadScene("Dance");
    }

    private void SendButtonTextToPython(string buttonText)
    {
        try
        {
            // Cria um cliente TCP para se comunicar com o Python
            using (System.Net.Sockets.TcpClient client = new System.Net.Sockets.TcpClient())
            {
                client.Connect("127.0.0.1", 25002); // Conecta-se ao servidor Python

                // Converte o texto do botão em bytes
                byte[] data = Encoding.ASCII.GetBytes(buttonText);

                // Obtém a stream de saída do cliente
                System.IO.Stream stream = client.GetStream();

                // Envia os dados para o servidor Python
                stream.Write(data, 0, data.Length);

                // Fecha a conexão
                client.Close();
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError("Error sending button text to Python: " + e.Message);
        }
    }
}
