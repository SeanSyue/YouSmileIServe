#! /bin/sh

cp -R .config ~/
sudo apt-get install portaudio19-dev libffi-dev libssl-dev libmpg123-dev -y
sudo apt-get install libzbar-dev libzbar0 -y
pip3 install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/google-vision/vision-936e81092155.json
sudo python3 setup.py install