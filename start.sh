#!/bin/bash
pip install opencv-python numpy
pip install mediapipe==0.9.0.1
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:$PORT
