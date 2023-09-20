using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuPrincipal : MonoBehaviour
{
    [SerializeField] private string slider;
    public void Jogar()
    {
        SceneManager.LoadScene(slider);

        ProcessStartInfo start = new ProcessStartInfo();
        start.FileName = "/usr/bin/python3.10";
        start.WorkingDirectory = "/home/CIN/giln/Documents/bsc/multimidia/Just-Dance/Python";
        start.Arguments = string.Format("{0}", "StreamFlow.py");
        start.UseShellExecute = true;
        // start.RedirectStandardOutput = true;
        using(Process process = Process.Start(start))
        {
        }

    }
}
