import flask
from flask import Flask
from gtts import gTTS
from pygame import mixer
app = Flask(__name__)


@app.route('/')
def info():
    html = "<h3>Hello World!</h3>"
    return html


@app.route('/textToSpeech')
def text_to_speech():

    gTTS("will return a speech from given text").save(".//tts.mp3")
    return "saved an mp3, please check"


@app.route('/<texttospeech>')
def runtime_text_to_speech(texttospeech):
    mp3file = './/'+texttospeech+'.mp3'
    #gTTS seems to be slow, need to find something faster
    play_header: bool = flask.request.headers.get('play')
    if play_header:
        gTTS(texttospeech).save(mp3file)
        mixer.init()
        mixer.music.load(mp3file)
        mixer.music.play()
    return texttospeech


if __name__ == '__main__':
    app.run()