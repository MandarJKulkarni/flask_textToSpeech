# flask_textToSpeech

Flask application to create an mp3 from a given input text

Use /play/ path to convert the text to audio file and play

e.g. if you are running the server on localhost:5000 then 

     type localhost:5000/play/hello to listen the browser say "hello"

     localhost:5000/play/there will make the browser say "there"
        
More interesting work is in progress!!

Use /playmp3 post request to convert the input text into audio and play the same.

curl -X POST   http://127.0.0.1:5000/playmp3  -H 'Content-Type: text/plain' -d '{
"text":"Hello there, I am using Python."
}'