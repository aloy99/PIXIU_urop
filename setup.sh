#!/bin/bash

# Exit on any error
cd /home/shadeform
set -e

echo "Starting setup process..."


echo "Installing Faireval..."
git clone https://github.com/aloy99/PIXIU_urop.git --recursive
cd Faireval
pip install -r requirements.txt
cd src/financial-evaluation
pip install -e .[multilingual]
cd ../../

echo "Installing gdown and downloading BART checkpoint..."
pip install gdown
export PATH=$PATH:"/home/shadeform/.local/bin"
gdown https://drive.google.com/uc?id=1_7JfF7KOInb7ZrxKHIigTMR4ChVET01m -O src/metrics/BARTScore/bart_score.pth

# Login to HuggingFace
echo "Logging in to HuggingFace..."
echo [inserttoken] | huggingface-cli login

# Fix datasets version and run evaluation
echo "Installing correct datasets version..."
pip install datasets==2.21.0

echo "Setup complete!"