#!/bin/bash
module load intel/2021.2
module load impi/2021.2
module load netcdf/intel/4.7.4
module load hdf5/intel/1.12.0
export NETCDF_ROOT=/sw/dataformats/netcdf/intel.19/4.7.4/skl
export MPI_ROOT=$(dirname $(dirname `which mpiifort`))
export MPI_INC_DIR=${MPI_ROOT}/include
export LD_LIBRARY_PATH="/sw/dataformats/netcdf/intel.19/4.7.4/skl/lib/:$LD_LIBRARY_PATH"
#
ROOTDIR="/home/hbknama0/gsa_recom2/code/model/MITgcm"
CODEDIR="/home/hbknama0/gsa_recom2/code/model/code_1d"
OPTIONFILE="/home/hbknama0/gsa_recom2/code/model/linux_ia64_ifort_hlrn"
BUILDDIR="/scratch/usr/hbknama0/GSA/model"

rm -rf $BUILDDIR/*
cd $BUILDDIR

$ROOTDIR/tools/genmake2 -of $OPTIONFILE -mods $CODEDIR -rootdir $ROOTDIR -mpi

make depend
make -j 8
