#!/bin/bash -e
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=02:00:00
#SBATCH --job-name=jobName
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err
#SBATCH --chdir=/scratch/sca321/research/llm/myscrape
#SBATCH --mem-per-cpu=24G
#SBATCH --gres=gpu:1

module purge

singularity exec --nv \
  --overlay /scratch/sca321/drl/Group-Preference-Alignment/conda/overlay-50G-10M.ext3:ro \
  --overlay /vast/work/public/ml-datasets/coco/coco-2014.sqf:ro \
  --overlay /vast/work/public/ml-datasets/coco/coco-2015.sqf:ro \
  --overlay /vast/work/public/ml-datasets/coco/coco-2017.sqf:ro \
  /scratch/work/public/singularity/cuda11.8.86-cudnn8.7-devel-ubuntu22.04.2.sif \
  /bin/bash -c "source /ext3/env.sh; python "