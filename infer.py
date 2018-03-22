import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

def facerecognition(image):
    try:
        temp = subprocess.check_output(['python', '/home/pansek/openface/demos/classifier.py', 'infer', '/home/pansek/openface/demos/lab509_features/classifier.pkl', image])
        text = temp.decode('utf-8')
        lines = temp.split('\n')
        lineEnd = lines[len(lines)-2]
        words = lineEnd.split(' ')
        if(words[0] == "Predict"):
            return(words[1])
        else:
            return None
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

image = args.echo
face = facerecognition(image)
if face:
    print(face)
else:
    print('None')
