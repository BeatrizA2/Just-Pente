using UnityEngine;
using TMPro;

public class Score : MonoBehaviour
{
    public TextMeshProUGUI scoreText;

    // Update is called once per frame
    void Update()
    {
        // Defina o texto do TextMeshProUGUI
        scoreText.text = "200";
    }
}
