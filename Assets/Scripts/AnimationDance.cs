using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.SceneManagement;
using System.Threading;

public class AnimationDance : MonoBehaviour
{
    public GameObject[] Body;
    List<string> lines;
    int counter = 0;
    AudioSource audioSource;

    private void Start()
    {
        string buttonText = PlayerPrefs.GetString("Button_Text");
        lines = System.IO.File.ReadLines($"Assets/Position files/{buttonText}.txt").ToList();

        // Load and play the audio from the "Audios" directory with the same name as the button text.
        audioSource = gameObject.AddComponent<AudioSource>();
        AudioClip audioClip = Resources.Load<AudioClip>("Audios/" + buttonText);
        if (audioClip != null)
        {
            audioSource.clip = audioClip;
            audioSource.Play();
        }
        else
        {
            Debug.LogError("Audio clip not found: " + buttonText);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (!audioSource.isPlaying)
        {
            // Transition to the "ScoreBoard" scene.
            SceneManager.LoadScene("ScoreBoard");
        }

        string[] points = lines[counter].Split(',');

        for (int i = 0; i <= 32; i++)
        {
            float x = float.Parse(points[0 + i * 3]) / 100;
            float y = float.Parse(points[1 + i * 3]) / 100;
            float z = float.Parse(points[2 + i * 3]) / 300;

            Body[i].transform.localPosition = new Vector3(x, y, z);
        }

        counter += 1;

        if (counter == lines.Count)
        {
            counter = 0;
        }
        Thread.Sleep(25);
    }
}
