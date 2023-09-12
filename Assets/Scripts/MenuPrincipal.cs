using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuPrincipal : MonoBehaviour
{
    [SerializeField] private string slider;
    public void Jogar()
    {
        SceneManager.LoadScene(slider);
    }
}
