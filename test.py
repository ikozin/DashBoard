import sys
import time
import subprocess


if __name__ == "__main__":
	print("Start!")
	p = subprocess.Popen("calc.exe", shell=True)
	p.wait()
	print("Done!")
