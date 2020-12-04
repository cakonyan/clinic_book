#!/bin/sh

pip3 install -r requirements.txt -q 

mkdir ~/clinic

cp ~/Dowaloads/book ~/clinic

echo "alias clinic='python3 ~/clinic/book/main.py'" >> ~/.zshrc 
