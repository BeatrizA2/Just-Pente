using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

public class ScoreManager : MonoBehaviour
{
    public TextMeshProUGUI scoreText;

    private void Start()
    {
        float finalScore = PlayerPrefs.GetFloat("Score");
        scoreText.text = finalScore.ToString("F2");
    }

    public void Continuar()
    {
        SceneManager.LoadScene("Slider");
    }

}
