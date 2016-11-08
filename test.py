import sys
import time
import subprocess


if __name__ == "__main__":
	print("Start!")
	path = "calc.exe"
	p = subprocess.Popen(path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#print(p.stdout.read())
	p.wait()
	print("Done!")
