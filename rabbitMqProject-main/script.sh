#!/bin/bash


gnome-terminal -- bash -c "python3 sensor.py"
gnome-terminal -- bash -c "python3 sensor.py"
gnome-terminal -- bash -c "python3 sensor.py"
gnome-terminal -- bash -c "python3 sensor.py"

gnome-terminal -- bash -c "python3 processor.py"
gnome-terminal -- bash -c "python3 processor.py"


sleep 1

gnome-terminal -- bash -c "python3 proxy.py"

gnome-terminal --bash -c "python3 terminal.py terminal1_queue"
gnome-terminal --bash -c "python3 terminal.py terminal2_queue"
