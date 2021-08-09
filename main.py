import os
from flask import Flask
from flask import request
from gtts import gTTS
from pygame import mixer
import html2text
import requests
import timeit
import json
from newspaper import Article

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
    try:
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
        os.remove(mp3file)
    except Exception as ex:
        print(ex.__str__())
    finally:
        return texttospeech


@app.route('/playmp3', methods=['POST'])
def play_mp3():
    input_text = json.loads(request.data)["text"]
    mp3file = './/text.mp3'
    if os.path.exists(mp3file):
        os.remove(mp3file)
    gTTS(input_text).save(mp3file)
    mixer.init()
    mixer.music.load(mp3file)
    mixer.music.play()
    return input_text


def get_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as ex:
        return ex.__str__()


@app.route('/mp3fromurl', methods=['POST'])
def mp3_from_url():
    input_url = json.loads(request.data)["url"]
    url_text = get_text_from_url(input_url)
    
    if url_text:
        mp3file = './/text.mp3'
        if os.path.exists(mp3file):
            os.remove(mp3file)
        gTTS(url_text).save(mp3file)
        mixer.init()
        mixer.music.load(mp3file)
        mixer.music.play()
        return input_url
    return "Unable to extract the data from the page"


if __name__ == '__main__':
    app.run()
