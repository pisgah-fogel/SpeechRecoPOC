#!/usr/bin/env python3

# Get model with: wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
# Works beter on bigger model: wget https://alphacephei.com/vosk/models/vosk-model-en-us-daanzu-20200905.zip
# pip3 install vosk
# pip install pyttsx3
#

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

# for speach synthesis
import pyttsx3
engine = pyttsx3.init()

q = queue.Queue()

skipDatas = False

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    if not skipDatas:
        q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    tmp = rec.Result()
                    tmp = tmp[:tmp.rfind("\"")]
                    tmp = tmp[tmp.rfind("\"")+1:]
                    print("=> " + tmp)
                    if tmp == "test":
                        skipDatas = True
                        engine.say("This is a test")
                        engine.runAndWait()
                        skipDatas = False
                    elif tmp == "exit" or tmp == "quit":
                        skipDatas = True
                        engine.say("quitting")
                        engine.runAndWait()
                        skipDatas = False
                        break
                else:
                    tmp = rec.PartialResult()
                    tmp = tmp[17:]
                    tmp = tmp[:tmp.find("\"")]
                    if tmp != "":
                        print(tmp)
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
