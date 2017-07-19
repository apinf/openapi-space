#!/bin/bash
if [[ -z $VIRTUAL_ENV ]]; then
	source venv/bin/activate
fi

clear
python main.py
