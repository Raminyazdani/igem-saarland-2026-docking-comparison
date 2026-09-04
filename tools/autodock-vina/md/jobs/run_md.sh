#!/bin/bash
#SBATCH --job-name=pahp_md
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

set -e

LIG=${1:?usage: sbatch run_md.sh <pyrene|phenanthrene>}
case $LIG in
  pyrene)       RES=PYR ;;
  phenanthrene) RES=PHN ;;
  *) echo "unknown ligand $LIG"; exit 1 ;;
esac

module load gromacs || echo "adjust module name for this cluster"

SYS=../systems/${LIG}_complex
MDP=../mdp/${LIG}
WORK=${LIG}_run
mkdir -p $WORK && cd $WORK

[ -f topol.top ] || cp ${SYS}.top topol.top
[ -f conf.gro ] || cp ${SYS}.gro conf.gro

[ -f index.ndx ] || printf "\"Protein\" | \"${RES}\"\nq\n" | gmx make_ndx -f conf.gro -o index.ndx

[ -f em.gro ] || { gmx grompp -f ${MDP}/em.mdp -c conf.gro -p topol.top -n index.ndx -o em.tpr -maxwarn 2 || exit 1; gmx mdrun -deffnm em -ntomp $SLURM_CPUS_PER_TASK || exit 1; }

[ -f nvt.gro ] || { gmx grompp -f ${MDP}/nvt.mdp -c em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 2 || exit 1; gmx mdrun -deffnm nvt -ntomp $SLURM_CPUS_PER_TASK || exit 1; }

[ -f npt.gro ] || { gmx grompp -f ${MDP}/npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -n index.ndx -o npt.tpr -maxwarn 2 || exit 1; gmx mdrun -deffnm npt -ntomp $SLURM_CPUS_PER_TASK || exit 1; }

if [ ! -f md.tpr ]; then
  gmx grompp -f ${MDP}/md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md.tpr -maxwarn 2
fi

if [ -f md.cpt ]; then
  gmx mdrun -deffnm md -cpi md.cpt -maxh 23.5 -ntomp $SLURM_CPUS_PER_TASK
else
  gmx mdrun -deffnm md -maxh 23.5 -ntomp $SLURM_CPUS_PER_TASK
fi

if [ ! -f md.gro ]; then
  echo "production incomplete - resubmit this script to continue from checkpoint"
  exit 0
fi

echo "done: $LIG"
