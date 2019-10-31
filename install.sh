#!/bin/bash

conda create -n dataset-tools pip python=3.6 -y
source activate dataset-tools
pip install -r requirements.txt
git submodule init
git submodule update
pip install -r frederic/requirements.txt
