#!/bin/bash
pkill torcs
torcs -r ~/.torcs/config/raceman/practice.xml & \
python main.py

