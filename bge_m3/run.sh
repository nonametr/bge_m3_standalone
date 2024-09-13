#!/bin/bash

screen -dmS www gunicorn -b 0.0.0.0:8093 -w 1 --threads 8 --log-level "debug" bge_m3_standalone:app
