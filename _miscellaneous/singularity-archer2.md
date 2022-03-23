---
layout: page-fullwidth
title: Singularity on ARCHER2
subheadline: Miscellaneous
teaser: Supplementary documentation to the ARCHER2 <a href="https://docs.archer2.ac.uk/user-guide/containers/">containers</a> documentation.
---
<div class="row">
<div class="medium-4 medium-push-8 columns" markdown="1">
<div class="panel radius" markdown="1">
**Table of Contents**
{: #toc }
*  TOC
{:toc}
</div><!-- /.panel -->
</div><!-- /.medium-4 -->

<div class="medium-8 medium-pull-4 columns" markdown="1">

*Note: Knowledge of [Singularity](https://sylabs.io/) is assumed.*

## General comments

* Singularity documentation is at ​[https://sylabs.io/docs](https://sylabs.io/docs)

* The `glibc` version of the container OS has to be ≥ 2.26 to avoid GLIC version issues when using the container with Cray system libraries. ​[Distrowatch](https://distrowatch.com) can provide information on this.

* The container requires MPICH and not OpenMP to allow use of Cray's MPT and fast interconnects at runtime via MPICH ABI.

* Add `/opt/cray/pe/lib64` to the end of `SINGULARITYENV_LD_LIBRARY_PATH` to ensure the default version of Cray libraries is used with the container.

* The executable **has** to be linked with `libxpmem` despite the fact it doesn't have any dependencies for it. Otherwise the executable will run more slowly than an equivalent executable compiled directly on ARCHER2. Full details below.

</div><!-- /.medium-8 -->
</div><!-- /.ros -->

## Building a container for ARCHER2

This example is based on ​[https://epcced.github.io/2020-12-08-Containers-Online/12-singularity-mpi/index.html](https://epcced.github.io/2020-12-08-Containers-Online/12-singularity-mpi/index.html) but has been set up to use ​[https://github.com/LLNL/mpiBench](https://github.com/LLNL/mpiBench) rather than OSU Micro-Benchmarks.

On local system, build container using the following `def` file:
~~~
Bootstrap: docker
From: ubuntu:20.04

%files

%environment
    export SINGULARITY_MPICH_DIR=/usr   
%post
    apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get -y install build-essential libfabric-dev libibverbs-dev gfortran wget git
    export MPICH_VERSION=3.3.2
    export MPICH_URL="http://www.mpich.org/static/downloads/$MPICH_VERSION/mpich-$MPICH_VERSION.tar.gz"
    cd /root
    wget -O mpich-$MPICH_VERSION.tar.gz $MPICH_URL && tar xzf mpich-$MPICH_VERSION.tar.gz && cd mpich-$MPICH_VERSION
    echo "Configuring and building MPICH..."
    ./configure --prefix=/usr --with-device=ch3:nemesis:ofi && make -j8 && make install
#Base MPICH installed, now install application and required software stack.

#Install mpiBench
    cd /opt
    git clone https://github.com/LLNL/mpiBench mpiBench.git
    cp mpiBench.git/mpiBench.c .
    #create dummy libxpmem
    echo "" | g++ -shared -fPIC -x c++ - -o libxpmem.so
    mpicc -o mpiBench -Wl,--allow-shlib-undefined -Wl,--no-as-needed -L. -lxpmem mpiBench.c #Fast version with xpmem
    mpicc -o mpiBench_noxpmem mpiBench.c #Slow version without xpmem****
~~~

### xpmem

When an executable is compiled on ARCHER2, `libxpmem` is automatically built into the ELF header of the executable. xpmem is Cray's memory management system and is faster than the standard linux kernel version on ARCHER2 and in general, executables without libxpmem in their `ELF DT_NEEDED` header will run slower than those with it. Note that there's no dependencies on libxpmem in the code, it is only used at runtime.

Cray's propitiatory version of libxpmem is unavailable in the container, but as there are no code dependencies on it, it's only used at runtime, a dummy library can be used instead. The dummy library needs to be created, and linked in the executable to set `ELF DT_NEEDED` tag, which can then be picked up when the executable is run.

The lines
~~~
    echo "" | g++ -shared -fPIC -x c++ - -o libxpmem.so
    mpicc -o mpiBench -Wl,--allow-shlib-undefined -Wl,--no-as-needed -L. -lxpmem mpiBench.c
~~~
do this. `echo "" | g++ -shared -fPIC -x c++ - -o libxpmem.so` creates a empty dummy library, and `-Wl,--allow-shlib-undefined -Wl,--no-as-needed -L. -lxpmem` forces the linker to update the `ELF DT_NEEDED` tag with `libxpmem`, even thought there's no code dependencies for it.

The ​[patchelf](https://github.com/NixOS/patchelf) tool can also be used to update the ELF header.

## Running container on ARCHER2

The following illustrates how to run the above container on ARCHER2, and also illustartes the affect of libxpmem on the MPI benchmark executable. The job submission script is based on​ [osu_latency.slurm.template](https://github.com/EPCCed/2020-12-08-Containers-Online/blob/gh-pages/files/osu_latency.slurm.template) The options to `SINGULARITYENV_LD_LIBRARY_PATH` and `singopts` ensure that Cray's MPICH ABI compatible MPI is used when the container is run.

~~~
#!/bin/bash --login

# Slurm job options (name, compute nodes, job time)

#SBATCH --job-name=singmpitest
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00

#SBATCH --account=<account>
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the batch environment
module load epcc-job-env
module load cpe-gnu gcc/9.3.0
gcc --version

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically 
#   using threading.
export OMP_NUM_THREADS=1

SDIR=/work/n02/n02/simon/sing #work dir of container
SIF=mpitest_ubuntu.sif #container name
EXEC=mpiBench #executable name

cd $SDIR
rm -f ${EXEC}_cray ${EXEC}_con ${EXEC}_noxpmem $EXEC.c

# Run the executables

echo Cray built
#Extract code from container, compile and run
singularity exec -B /work:/work $SDIR/$SIF cp /opt/$EXEC.c $SDIR
cc -o ${EXEC}_cray $EXEC.c
srun $SDIR/${EXEC}_cray

echo Singularity no xpmem
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/mpich/8.0.16/ofi/gnu/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64
singopts="-B /opt/cray,/usr/lib64:/usr/lib64/host,/usr/lib64/tcl,/var/spool/slurmd/mpi_cray_shasta"
srun --cpu-bind=cores singularity exec $singopts $SDIR/$SIF /opt/${EXEC}_noxpmem

echo Singularity
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/mpich/8.0.16/ofi/gnu/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64:/etc/alternatives/cray-xpmem/lib64
singopts="-B /opt/cray,/usr/lib64:/usr/lib64/host,/usr/lib64/tcl,/var/spool/slurmd/mpi_cray_shasta,/etc/alternatives/cray-xpmem"
srun --cpu-bind=cores singularity exec $singopts $SDIR/$SIF /opt/${EXEC}
~~~

The script runs three versions of the mpiBench benchmark

1. The C code is extracted from the container, compiled and run natively.
2. The version of the benchmark executable without xpmem run inside the container with srun.
3. The version of the benchmark executable with xpmem run inside the container with srun.

For 3. `/etc/alternatives/cray-xpmem/lib64` has been added to `SINGULARITYENV_LD_LIBRARY_PATH` and `/etc/alternatives/cray-xpmem` added to `singopts` to ensure Crays's `libepmem`, rather than the dummy version is used by the executable.

Sample output, grepping on a message size of 16384 bytes. Avg: is the average speed of the MPI call, so lower is better.

~~~
Cray built
Bcast               	Bytes:	   16384	Iters:	    314	Avg:	123.6885	Min:	123.6869	Max:	123.6899	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoall            	Bytes:	   16384	Iters:	     26	Avg:	1809.5307	Min:	1809.4686	Max:	1809.5878	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoallv           	Bytes:	   16384	Iters:	     48	Avg:	916.1998	Min:	916.1731	Max:	916.2277	Comm: MPI_COMM_WORLD	Ranks: 128
Allgather           	Bytes:	   16384	Iters:	      7	Avg:	6693.9246	Min:	6693.8741	Max:	6693.9763	Comm: MPI_COMM_WORLD	Ranks: 128
Allgatherv          	Bytes:	   16384	Iters:	     14	Avg:	3361.8193	Min:	3361.7871	Max:	3361.8382	Comm: MPI_COMM_WORLD	Ranks: 128
Gather              	Bytes:	   16384	Iters:	     89	Avg:	455.4998	Min:	455.4920	Max:	455.5134	Comm: MPI_COMM_WORLD	Ranks: 128
Gatherv             	Bytes:	   16384	Iters:	    125	Avg:	360.3713	Min:	360.3630	Max:	360.3802	Comm: MPI_COMM_WORLD	Ranks: 128
Scatter             	Bytes:	   16384	Iters:	    122	Avg:	373.7975	Min:	373.7856	Max:	373.8071	Comm: MPI_COMM_WORLD	Ranks: 128
Allreduce           	Bytes:	   16384	Iters:	    187	Avg:	199.4249	Min:	199.4225	Max:	199.4289	Comm: MPI_COMM_WORLD	Ranks: 128
Reduce              	Bytes:	   16384	Iters:	    437	Avg:	 60.9836	Min:	 60.9822	Max:	 60.9855	Comm: MPI_COMM_WORLD	Ranks: 128
Singularity no xpmem
Bcast               	Bytes:	   16384	Iters:	    150	Avg:	274.9853	Min:	274.9809	Max:	274.9888	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoall            	Bytes:	   16384	Iters:	      8	Avg:	6572.4461	Min:	6572.0379	Max:	6572.8426	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoallv           	Bytes:	   16384	Iters:	     18	Avg:	2707.5527	Min:	2707.4152	Max:	2707.7066	Comm: MPI_COMM_WORLD	Ranks: 128
Allgather           	Bytes:	   16384	Iters:	      8	Avg:	5966.5311	Min:	5966.3951	Max:	5966.6634	Comm: MPI_COMM_WORLD	Ranks: 128
Allgatherv          	Bytes:	   16384	Iters:	     15	Avg:	3261.3333	Min:	3261.2801	Max:	3261.3754	Comm: MPI_COMM_WORLD	Ranks: 128
Gather              	Bytes:	   16384	Iters:	     74	Avg:	476.5916	Min:	476.5762	Max:	476.6052	Comm: MPI_COMM_WORLD	Ranks: 128
Gatherv             	Bytes:	   16384	Iters:	    116	Avg:	350.3050	Min:	350.3006	Max:	350.3253	Comm: MPI_COMM_WORLD	Ranks: 128
Scatter             	Bytes:	   16384	Iters:	     68	Avg:	604.5004	Min:	604.4858	Max:	604.5278	Comm: MPI_COMM_WORLD	Ranks: 128
Allreduce           	Bytes:	   16384	Iters:	    113	Avg:	327.7516	Min:	327.7475	Max:	327.7686	Comm: MPI_COMM_WORLD	Ranks: 128
Reduce              	Bytes:	   16384	Iters:	    427	Avg:	 55.0977	Min:	 55.0959	Max:	 55.0993	Comm: MPI_COMM_WORLD	Ranks: 128
Singularity xpmem
Bcast               	Bytes:	   16384	Iters:	    317	Avg:	124.3842	Min:	124.3823	Max:	124.3861	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoall            	Bytes:	   16384	Iters:	     27	Avg:	1785.1379	Min:	1785.1105	Max:	1785.1812	Comm: MPI_COMM_WORLD	Ranks: 128
Alltoallv           	Bytes:	   16384	Iters:	     51	Avg:	905.5899	Min:	905.5605	Max:	905.6260	Comm: MPI_COMM_WORLD	Ranks: 128
Allgather           	Bytes:	   16384	Iters:	      7	Avg:	5993.3745	Min:	5993.2981	Max:	5993.5706	Comm: MPI_COMM_WORLD	Ranks: 128
Allgatherv          	Bytes:	   16384	Iters:	     15	Avg:	3131.0068	Min:	3130.9764	Max:	3131.0240	Comm: MPI_COMM_WORLD	Ranks: 128
Gather              	Bytes:	   16384	Iters:	     92	Avg:	458.2367	Min:	458.2301	Max:	458.2405	Comm: MPI_COMM_WORLD	Ranks: 128
Gatherv             	Bytes:	   16384	Iters:	    130	Avg:	336.4190	Min:	336.4123	Max:	336.4251	Comm: MPI_COMM_WORLD	Ranks: 128
Scatter             	Bytes:	   16384	Iters:	    118	Avg:	377.9327	Min:	377.9258	Max:	377.9702	Comm: MPI_COMM_WORLD	Ranks: 128
Allreduce           	Bytes:	   16384	Iters:	    198	Avg:	190.4637	Min:	190.4603	Max:	190.4651	Comm: MPI_COMM_WORLD	Ranks: 128
Reduce              	Bytes:	   16384	Iters:	    469	Avg:	 62.3386	Min:	 62.3376	Max:	 62.3442	Comm: MPI_COMM_WORLD	Ranks: 128
~~~

It can be seen that the no-xpmem executable run inside the container is generally slower than the native Cray version, whilst the xpmem version run inside the container has comparable speeds to the native version.

The MPI benchmark was run on 8 nodes, and again the xpmem version of the executable had similar speeds to the natively compiled version.

### CRAY compiler
It is possible to run a GNU compiled containerised executable was CRAY compiled MPI libraries. In the submission script, in `SINGULARITYENV_LD_LIBRARY_PATH` change `/opt/cray/pe/mpich/8.0.16/ofi/gnu/9.1/lib-abi-mpich` to `/opt/cray/pe/mpich/8.0.16/ofi/cray/9.1/lib-abi-mpich` and append `/opt/cray/pe/cce/10.0.4/cce/x86_64/lib` to it. ie
~~~
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/mpich/8.0.16/ofi/cray/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64:/etc/alternatives/cray-xpmem/lib64:/opt/cray/pe/cce/10.0.4/cce/x86_64/lib
~~~
The benchmark was repeated on 1 node and 8 nodes, compiling directly with the CRAY compiler, and using the containerised GNU compiled executable with CRAY MPI libraries, and no significant differences with respect to the GNU MPI version seen.

### NetCDF

The following is a definition file for a container with MPICH and parallel HDF5/NetCDF and a Netcdf benchmark ​[https://github.com/joobog/netcdf-bench](https://github.com/joobog/netcdf-bench)
~~~
Bootstrap: docker
From: ubuntu:20.04

%files
      mpich-3.3.2.tgz /opt  
      netcdf.tgz /opt  

%environment
    export MPICH_VERSION=3.3.2
    export MPICH_DIR=/opt/mpich-$MPICH_VERSION
    export SINGULARITY_MPICH_DIR=$MPICH_DIR
    export SINGULARITYENV_APPEND_PATH=$MPICH_DIR/bin
    export SINGULAIRTYENV_APPEND_LD_LIBRARY_PATH=$MPICH_DIR/lib
    
%post
    apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get -y install build-essential libfabric-dev libibverbs-dev gfortran wget git m4 zlib1g-dev cmake
    export MPICH_VERSION=3.3.2
    export MPICH_DIR=/opt/mpich-$MPICH_VERSION
    export MPICH_URL="http://www.mpich.org/static/downloads/$MPICH_VERSION/mpich-$MPICH_VERSION.tar.gz"

#MPICH
    echo "Configuring and building MPICH..."
    mkdir -p /tmp/mpich
    cd /tmp/mpich && wget -O mpich-$MPICH_VERSION.tar.gz $MPICH_URL && tar xzf mpich-$MPICH_VERSION.tar.gz
    cd /tmp/mpich/mpich-$MPICH_VERSION && ./configure --prefix=$MPICH_DIR --with-device=ch3:nemesis:ofi && make -j8 && make install

# Set env variables so we can compile our application
    export PATH=$MPICH_DIR/bin:$PATH
    export LD_LIBRARY_PATH=$MPICH_DIR/lib:$LD_LIBRARY_PATH
    export MANPATH=$MPICH_DIR/share/man:$MANPATH

#Install netcdf
    INSTALL_DIR=/opt/netcdf
    HDF5=1.12.0
    NETCDF4=4.7.4
    NETCDF_FORTRAN=4.5.3
    BUILD_DIR=/tmp/build_netcdf
    mkdir -p $BUILD_DIR

#HDF5
    cd $BUILD_DIR
    wget http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-$HDF5/src/hdf5-$HDF5.tar.gz
    tar -xzf hdf5-$HDF5.tar.gz
    cd $BUILD_DIR/hdf5-$HDF5
    CC=mpicc FC=mpif90 ./configure --prefix=$INSTALL_DIR --enable-static --enable-fortran --enable-parallel
    make clean && make -j$NCORES && make install

    export NETCDF_DIR=$INSTALL_DIR
    export CPPFLAGS=-I$INSTALL_DIR/include
    export FFLAGS=-I$INSTALL_DIR/include
    export LDFLAGS=-L$INSTALL_DIR/lib 
    export PATH=$INSTALL_DIR/bin:$PATH
    export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH

#NetCDF
    cd $BUILD_DIR
    wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-$NETCDF4.tar.gz
    tar -xzf netcdf-c-$NETCDF4.tar.gz
    cd $BUILD_DIR/netcdf-c-$NETCDF4
    CC=mpicc CXX=mpicxx FF=mpif90 FC=mpif90 ./configure --prefix=$INSTALL_DIR --disable-dap
    make clean && make -j$NCORES && make install

#Required for parallel NetCDF-fortran
    export LIBS="-lnetcdf -lhdf5_hl -lhdf5 -ldl -lm -lz"

#netcdf-fortran
    cd $BUILD_DIR
    wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-$NETCDF_FORTRAN.tar.gz
    tar -xzf netcdf-fortran-$NETCDF_FORTRAN.tar.gz
    cd $BUILD_DIR/netcdf-fortran-$NETCDF_FORTRAN
    CC=mpicc CXX=mpicxx FF=mpif90 FC=mpif90 ./configure --prefix=$INSTALL_DIR
    make clean && make -j$NCORES && make install

#Install netcdf-bench
    cd $BUILD_DIR
    rm -fr netcdf-bench
    git clone https://github.com/joobog/netcdf-bench
    cd netcdf-bench
    mkdir -p build && cd build
    unset LDFLAGS #cmake can't cope, otherwise.
    cmake -DNETCDF_INCLUDE_DIR=$NETCDF_DIR/include -DNETCDF_LIBRARY=$NETCDF_DIR/lib/libnetcdf.so ..
    make clean&& make
    cp src/benchtool /opt/benchtool_con
~~~
The benchmark submission script:
~~~
#!/bin/bash --login

# Slurm job options (name, compute nodes, job time)

#SBATCH --job-name=singmpitest
#SBATCH --nodes=6
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00

#SBATCH --account=n02
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the batch environment
module load epcc-job-env

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically 
#   using threading.
export OMP_NUM_THREADS=1

SDIR=/work/n02/n02/simon/sing
SIF=netcdf.sif
EXEC=benchtool

cd $SDIR
# Run the executable

echo cray gnu compiler
for i in {1..5}
do
   rm -f testfn.nc
   srun $SDIR/${EXEC}_gnu -d='200:1024:768:85'
done

echo cray cray compiler
for i in {1..5}
do
   rm -f testfn.nc
   srun $SDIR/${EXEC}_cray -d='200:1024:768:85'
done

echo Singularity
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/mpich/8.0.16/ofi/gnu/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64
singopts="-B /opt/cray,/usr/lib64:/usr/lib64/host,/usr/lib64/tcl,/var/spool/slurmd/mpi_cray_shasta"
singularity exec $singopts $SDIR/$SIF ldd  /opt/${EXEC}_con
for i in {1..5}
do
  rm -f testfn.nc
  srun --cpu-bind=cores singularity exec $singopts $SDIR/$SIF /opt/${EXEC}_con  -d='200:1024:768:85'
done

echo Singularity cray gnu NetCDF
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/netcdf-hdf5parallel/4.7.4.2/GNU/9.1/lib:/opt/cray/pe/hdf5-parallel/1.12.0.2/GNU/9.1/lib:/opt/cray/pe/mpich/8.0.16/ofi/gnu/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64:/etc/alternatives/cray-xpmem/lib64
singopts="-B /opt/cray,/usr/lib64:/usr/lib64/host,/usr/lib64/tcl,/var/spool/slurmd/mpi_cray_shasta,/etc/alternatives/cray-xpmem"
singularity exec $singopts $SDIR/$SIF ldd  /opt/${EXEC}_con
for i in {1..5}
do
  rm -f testfn.nc 
  srun --cpu-bind=cores singularity exec $singopts $SDIR/$SIF /opt/${EXEC}_con  -d='200:1024:768:85'
done

echo Singularity cray cray NetCDF
export SINGULARITYENV_LD_LIBRARY_PATH=/opt/cray/pe/netcdf-hdf5parallel/4.7.4.2/crayclang/9.1/lib:/opt/cray/pe/hdf5-parallel/1.12.0.2/crayclang/9.1/lib:/opt/cray/pe/mpich/8.0.16/ofi/cray/9.1/lib-abi-mpich:/usr/lib/x86_64-linux-gnu/libibverbs:/opt/cray/pe/pmi/6.0.7/lib:/opt/cray/libfabric/1.11.0.0.233/lib64:/usr/lib64/host:/.singularity.d/libs:/opt/cray/pe/lib64:/etc/alternatives/cray-xpmem/lib64:/opt/cray/pe/cce/10.0.4/cce/x86_64/lib
singopts="-B /opt/cray,/usr/lib64:/usr/lib64/host,/usr/lib64/tcl,/var/spool/slurmd/mpi_cray_shasta,/etc/alternatives/cray-xpmem"
singularity exec $singopts $SDIR/$SIF ldd  /opt/${EXEC}_con
for i in {1..5}
do
  rm -f testfn.nc 
  srun --cpu-bind=cores singularity exec $singopts $SDIR/$SIF /opt/${EXEC}_con  -d='200:1024:768:85'
done
~~~

The NetCDF benchmark was configured for writing 200 N512L85 like fields with the `-d='200:1024:768:85` option and configured to run use a single core. This produced an output file of 50GB. Note that the natively compiled executables were compiled offline.

It was run on ARCHER2 5 different ways.

1. Benchmark compiled on ARCHER using GNU.
2. Benchmark compiled on ARCHER using CRAY.
3. Benchmark compiled in conatiner using GNU, using containerisaed NetCDF libraries.
4. Benchmark compiled in conatiner using GNU, using ARCHER2 GNU compiled NetCDF libraries.
5. Benchmark compiled in conatiner using GNU, using ARCHER2 CRAY compiled NetCDF libraries.

Each benchmark was run five times. Results in MiB/s:
~~~
  Mean SD
1 1453 43
2 1434 26
3 1458 24
4 1465 22
5 1464 08
~~~
There is no significant differences in the timings. This tells us a number things:

* I/O timings are consistent over different runs on ARCHER2.
* There is no difference in NetCDF IO timings GNU vs CRAY compilers.
* There is no significant slow-down using containerised NetCDF libraries over ones provided by CRAY.
* Executables built in the container using containerised NetCDF libraries are able to utilise the local machine's NetCDF libraries. This can be useful if the local machine's libraries are bespoke to the local storage system.
* Executables built in the container using containerised NetCDF libraries are able to run with either GNU or CRAY built local NetCDF libraries. This isn't too surprising as the CRAY compiler uses the CLANG backend, which has been designed to be a like for like replacement for GNU.

Simon Wilson <br>
March 2021

