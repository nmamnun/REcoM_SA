#!/bin/bash
#SBATCH --job-name=recom
#SBATCH --time=10:59:00
#SBATCH --nodes=1
#SBATCH --ntasks=96
#SBATCH --mem-per-cpu=1500M
cat $0
module load intel/2021.2
module load impi/2021.2
module load netcdf/intel/4.7.4
module load hdf5/intel/1.12.0
export NETCDF_ROOT=/sw/dataformats/netcdf/intel.19/4.7.4/skl
export MPI_ROOT=$(dirname $(dirname `which mpiifort`))
export MPI_INC_DIR=${MPI_ROOT}/include
export LD_LIBRARY_PATH="/sw/dataformats/netcdf/intel.19/4.7.4/skl/lib/:$LD_LIBRARY_PATH"
#
export NAMELISTDIR=/scratch/usr/hbknama0/GSA/namelists/bats
export DATADIR=/scratch/usr/hbknama0/GSA/input_fields/bats
export MODELDIR=/scratch/usr/hbknama0/GSA/model
export SAMPLEDIR=/home/hbknama0/param_sample/sample_shortlist_100k/data
export OUTPUTSDIR=/scratch/usr/hbknama0/GSA/model_outputs/bats
export TMPDIR=/tmp
if [ ! -d "$LOCAL_TMPDIR" ]; then
  echo "No LOCAL_TMPDIR exists"
  exit 1
fi
#
srun="srun --exclusive -N1 -n1"
parallel="parallel --delay 0.2 -j $SLURM_NTASKS --joblog recom_runtask.log.$SLURM_JOB_ID --resume"
#
$parallel "mkdir $LOCAL_TMPDIR/bin-{} \
  && cd $LOCAL_TMPDIR/bin-{} \
  && cp $MODELDIR/mitgcmuv . \
  && cp $NAMELISTDIR/* . \
  && cp $SAMPLEDIR/data.recom-{} data.recom \
  && cp $DATADIR/* . \
  && $srun ./mitgcmuv >slurm_out.{} \
  && mv recomDiags2D.0000000000.t001.nc $OUTPUTSDIR/bats_diags2d_sl_{} \
  && mv recomDiags3D.0000000000.t001.nc $OUTPUTSDIR/bats_diags3d_sl_{} \
  && cd .. \
  && rm -r $LOCAL_TMPDIR/bin-{}" ::: {000001..010000}
#
