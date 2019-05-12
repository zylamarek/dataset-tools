#!/bin/bash

conda create -n dataset-tools pip python=3.6 -y
source activate dataset-tools
pip install --ignore-installed --upgrade -r requirements.txt
