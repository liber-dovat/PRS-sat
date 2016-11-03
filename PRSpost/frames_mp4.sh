#!/bin/bash

BANDA=$2
INDIR=$1
OUTDIR="/sat/prd-sat/PNGs/"

cd $INDIR; convert -crop 948x1132+0+0 +repage *.png repage%03d.png
cd $INDIR; ffmpeg -y -framerate 5 -i repage%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p $OUTDIR$BANDA.mp4