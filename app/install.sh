#!/bin/bash

pip install --upgrade pip

# 安裝 requirements.txt 中列出的套件
pip install -r requirements.txt

# 下載Spacy語言模型
python -m spacy download en_core_web_md