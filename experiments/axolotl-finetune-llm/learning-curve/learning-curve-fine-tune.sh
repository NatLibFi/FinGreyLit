#!/bin/bash
#SBATCH --job-name=learning-curve-fine-tune
#SBATCH -o lc-ft-output-%j.txt
#SBATCH -M ukko
#SBATCH -p gpu
#SBATCH -G 1
#SBATCH --constraint=a100
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t4:00:00
 
# mennään oikeaan paikkaan mistä tiedostot löytyvät
cd /home/oisuomin/wrk/git/FinGreyLit/experiments/axolotl-finetune-llm/learning-curve
 
# aktivoidaan oikeanlainen python-ympäristö
module purge
module load Python cuDNN
source ../venv/bin/activate
 
# ajetaan varsinainen laskentatyö
python learning-curve-fine-tune.py $1 $2
