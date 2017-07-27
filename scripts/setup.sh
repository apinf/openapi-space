#!/bin/bash
python=$(which python3)
if [[ -z $python ]]; then
	echo "I couldn't find a Python 3 installation :("
	echo "Make sure you have python3 in your PATH."
	exit 1
fi

echo "Creating virtual environment..."
virtualenv -p $python venv
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
if [ ! -f config.yaml ]; then
    cp example-config.yaml config.yaml
    echo "Copying example-config.yaml to config.yaml"
fi
echo "All done!"
echo 'Use `./start.sh` to start the server in debug mode.'
