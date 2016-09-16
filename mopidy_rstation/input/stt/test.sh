o "Recording, press ctrl+c to stop..."
arecord -D "plughw:1,0" -q -f cd -t wav | ffmpeg -loglevel panic -y -i - -ar 16000 -acodec flac speech.flac  > /dev/null 2>&1

echo "Processing..."
wget -q -U "Mozilla/5.0" --post-file speech.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" | cut -d\" -f12  > speech.txt

echo -n "You said: "
cat speech.txt

rm speech.flac
