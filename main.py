# import flask
import os
from flask import Flask
from gtts import gTTS
from pygame import mixer
import html2text
import requests
import timeit
app = Flask(__name__)


@app.route('/')
def info():
    html = "<h3>Text to speech service</h3>"
    return html


@app.route('/textToSpeech')
def text_to_speech():
    start = timeit.timeit()
    gTTS("will return a speech from given text").save(".//tts.mp3")
    end = timeit.timeit()
    return "saved an mp3 in {} seconds, please check".format(end-start)


@app.route('/<texttospeech>')
def runtime_text_to_speech(texttospeech):
    return texttospeech


@app.route('/play/<texttospeech>')
def play_audio(texttospeech):
    # gTTS is not that slow, mixer is comparatively slower
    # or need to use multithreading...
    # play_header: bool = flask.request.headers.get('play')
    # if play_header:
    mp3file = './/' + texttospeech + '.mp3'
    if not os.path.exists(mp3file):
        start = timeit.timeit()
        gTTS(texttospeech).save(mp3file)
        end = timeit.timeit()
        print("time taken by gtts {}".format(end-start))
    start = timeit.timeit()
    mixer.init()
    mixer.music.load(mp3file)
    mixer.music.play()
    end = timeit.timeit()
    print("time taken by mixer {}".format(end - start))
    return texttospeech


@app.route('/gettext')
def get_text():
    html = requests.get("https://www.google.com")
    text = html2text.html2text(html.text)
    textfile = open("htmltext.txt", 'w')
    textfile.write(text)
    textfile.close()
    return html


if __name__ == '__main__':
    app.run()
