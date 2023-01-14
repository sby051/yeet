#!/bin/bash

# install pyinstaller
pip install pyinstaller

pyinstaller --onefile ./src/yeet.py

# create bin folder if it doesn't exist
mkdir -p ./bin
mv ./dist/yeet ./bin/yeet
rm -rf ./dist
rm -rf ./yeet.spec
rm -rf ./build

echo "Yeet has been built and placed in ./bin/yeet"