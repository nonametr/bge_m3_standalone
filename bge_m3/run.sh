#!/bin/bash

#python3 bge_m3_standalone.py
gunicorn -b 0.0.0.0:8093 -w 1 --threads 2 --log-level "debug" bge_m3_standalone:app
