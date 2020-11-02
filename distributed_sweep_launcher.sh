#!/usr/bin/env bash
#SBATCH -J ktd
#SBATCH -p high
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem-per-cpu 1024
#SBATCH -C intel

#SBATCH --workdir=/homedtic/stotaro/ktd
#SBATCH -o /homedtic/stotaro/ktd/jobs/%N.%J.ktd.out # STDOUT
#SBATCH -e /homedtic/stotaro/ktd/jobs/%N.%J.ktd.err # STDOUT

set -x
module load PyTorch
source /homedtic/stotaro/ktd_env/bin/activate

PROJECT_NAME='ktd-reboot-sweep'
sh ./cmd/clean.sh
wandb sweep $1 -p $PROJECT_NAME &>sweep_id.log
SWEEP_ID=$(grep -o 'ID: .*' sweep_id.log | cut -f2 --d ' ')
SWEEP_ADDR=d3sm0/$PROJECT_NAME/$SWEEP_ID
echo $SWEEP_ADDR
NUM_PROC=10
for i in $(seq 0 $NUM_PROC)
  do
    echo "starting machine $i for $SWEEP_ADDR"
    sbatch distributed_sweep.sh $SWEEP_ADDR
    sleep 5
  done
