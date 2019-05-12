@echo off
PATH = %PATH%;%USERPROFILE%\Miniconda3\Scripts
conda create -n dataset-tools pip python=3.6 -y
call activate dataset-tools
pip install --ignore-installed --upgrade -r requirements.txt
