@echo off
PATH = %PATH%;%USERPROFILE%\Miniconda3\Scripts
conda create -n dataset-tools pip python=3.6 -y
call activate dataset-tools
conda install -c anaconda keras-gpu==2.2.4 cudnn=7.6.0=cuda9.0_0 -y
pip install -r requirements.txt
git submodule init
git submodule update
pip install -r frederic/requirements.txt
