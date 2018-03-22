import subprocess
save_path = '/home/pansek/webserver/media/search/search.jpeg'
try:
    face = subprocess.check_output(['python', '/home/pansek/workspace/infer.py', save_path])
    lines = face.split("\n")
    result = str(lines[len(lines)-1])
    print(result)
except subprocess.CalledProcessError as e:
    raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
