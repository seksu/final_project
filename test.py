import subprocess
def facerecognition(image):
    subprocess.check_call(['python', '/home/pansek/openface/demos/classifier.py', 'infer', 'classifier.pkl', image])
