#!/bin/bash

gnome-terminal -- bash -c "python3 servidor_load_balancer.py"

gnome-terminal -- bash -c "python3 servidor_processor.py"

sleep 1

gnome-terminal -- bash -c "python3 sensor.py"

gnome-terminal -- bash -c "python3 servidor_terminales.py"

gnome-terminal -- bash -c "python3 servidor_proxy.py"