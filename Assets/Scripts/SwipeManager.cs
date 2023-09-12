using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SwipeManager : MonoBehaviour
{
    [SerializeField] private string cupid;
    [SerializeField] private string danceNight;

    public void Cupid()
    {
        SceneManager.LoadScene(cupid);
    }

    public void Night()
    {
        SceneManager.LoadScene(danceNight);
    }
}
