#!/bin/bash
#SBATCH -p standard96
#SBATCH -N 1
#SBATCH -t 09:59:00

source /home/hbknama0/miniconda3/bin/activate
conda activate general

export TMPDIR=/tmp
if [ ! -d "$LOCAL_TMPDIR" ]; then
  echo "No LOCAL_TMPDIR exists"
  exit 1
fi

mkdir $LOCAL_TMPDIR/model_outputs
cd $LOCAL_TMPDIR/model_outputs
cp /scratch/usr/hbknama0/GSA/model_outputs/dyfamed_diags2d_shortlist_param_100k.tar .
cp /scratch/usr/hbknama0/GSA/model_outputs/dyfamed_diags3d_shortlist_param_100k.tar .

tar -cvzf dyfamed_diags2d_shortlist_param_100k.tar .
tar -cvzf dyfamed_diags2d_shortlist_param_100k.tar .

rm *.tar

cp /home/hbknama0/gsa_recom2/code/jobs/get_monthly_data_dyfamed.py .
srun python get_monthly_data_dyfamed.py

exit
