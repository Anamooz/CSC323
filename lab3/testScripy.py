import subprocess
import os
import requests

BASE_URL = "http://localhost:6100/?q=foo&mac="
for i in range(10, 30, 1):
    print("I = ", i)
    os.chdir("./Server-Files/HMAC-TimingPartBv2")
    process = subprocess.Popen(
        [
            "/home/brian/.pyenv/shims/python3",
            "./server.py",
            str(i / 1000),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.chdir("../../")
    result = subprocess.run(["python3", "./task4bv2.py"], capture_output=True)
    print(result.stdout.decode("utf-8"))
    if result.returncode == 0:
        result_output = result.stdout.decode("utf-8")
        result_output = result_output.split("Recovered MAC: ")[1].split("\n")[0].strip()
        res = requests.get(BASE_URL + result_output)
        if "Invalud Signature" not in res.text:
            print("Success at i = ", i)
            print("Recovered MAC: ", result_output)
            input("Press Enter to continue...")
            break
    else:
        process.kill()
        print("Failed at i = ", i)
