_hashbang = "#!/usr/bin/env bash"

_prefix = """#!/usr/bin/env bash
#SBATCH -J {project_name}
#SBATCH -p high
#SBATCH -N 1
#SBATCH -n {cpu}
#SBATCH --mem-per-cpu {mem_per_cpu}
#SBATCH -C intel

#SBATCH --workdir=/homedtic/{user}/{project_dir}
#SBATCH -o /homedtic/{user}/{project_dir}/jobs/%N.%J.out # STDOUT
#SBATCH -e /homedtic/{user}/{project_dir}/jobs/%N.%J.err # STDOUT
"""

_sweep = """
wandb sweep $1 -p $PROJECT_NAME &>sweep_id.log
SWEEP_ID=$(grep -o 'ID: .*' sweep_id.log | cut -f2 --d ' ')
SWEEP_ADDR=$WANDB_USER/$PROJECT_NAME/$SWEEP_ID
echo $SWEEP_ADDR
for i in $(seq 0 $CPU); do
    echo "starting machine $i for $SWEEP_ADDR"
    sleep 5
    sbatch sweep.sh $SWEEP_ADDR
  done
"""

__create = """
echo "create env for $PROJECT_NAME"
python -m venv $ENV_DIR
source $ENV_DIR/bin/activate
cd $PROJECT_DIR
pip install -r requirements.txt
"""

clean = """
echo "Clean old jobs"
CUR_DIR=${PWD##*/}
rm ~/$CUR_DIR/jobs/*
rm ~/$CUR_DIR/*.{err,out}
rm ~/$CUR_DIR/log.out
"""
