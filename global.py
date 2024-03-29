import subprocess

p = subprocess.run( ["python3", "/home/drh/PiPod_Zero2W/Sofware/main.py"] )
#print( p )
if p.returncode == 1:
  print("FAILED. Re-launching...")
  p = subprocess.run( ["python3", "/home/drh/PiPod_Zero2W/Sofware/main.py"] )

