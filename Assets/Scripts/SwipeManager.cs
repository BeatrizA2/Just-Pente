using UnityEngine;
using UnityEngine.SceneManagement;

public class SwipeManager : MonoBehaviour
{
    public void LoadDanceScene(string buttonText)
    {
        // Salva o texto do bot�o no PlayerPrefs
        PlayerPrefs.SetString("Button_Text", buttonText);
        SceneManager.LoadScene("Dance");
    }
}
