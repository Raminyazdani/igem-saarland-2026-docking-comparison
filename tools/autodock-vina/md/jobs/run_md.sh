#!/bin/bash
set -e
LIG=${1:?usage: ./run_md.sh <pyrene|phenanthrene>}
case $LIG in
  pyrene)       RES=PYR ;;
  phenanthrene) RES=PHN ;;
  *) echo "unknown ligand $LIG"; exit 1 ;;
esac

NT=$(nproc)
SYS=../../${LIG}_complex
MDP=../../mdp/${LIG}
mkdir -p ${LIG}_run && cd ${LIG}_run

[ -f topol.top ] || cp ${SYS}.top topol.top
[ -f conf.gro ]  || cp ${SYS}.gro conf.gro
[ -f index.ndx ] || printf "\"Protein\" | \"${RES}\"\n\"Water\" | \"Cl-\"\nname 19 Water_and_ions\nq\n" | gmx make_ndx -f conf.gro -o index.ndx

[ -f em.gro ]  || { gmx grompp -f ${MDP}/em.mdp  -c conf.gro -p topol.top -n index.ndx -o em.tpr  -maxwarn 2 || exit 1; gmx mdrun -deffnm em  -ntmpi 1 -ntomp $NT || exit 1; }
[ -f nvt.gro ] || { gmx grompp -f ${MDP}/nvt.mdp -c em.gro   -p topol.top -n index.ndx -o nvt.tpr -maxwarn 2 || exit 1; gmx mdrun -deffnm nvt -ntmpi 1 -ntomp $NT || exit 1; }
[ -f npt.gro ] || { gmx grompp -f ${MDP}/npt.mdp -c nvt.gro -t nvt.cpt -p topol.top -n index.ndx -o npt.tpr -maxwarn 2 || exit 1; gmx mdrun -deffnm npt -ntmpi 1 -ntomp $NT || exit 1; }

[ -f md.tpr ] || gmx grompp -f ${MDP}/md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md.tpr -maxwarn 2

if [ -f md.cpt ]; then
  gmx mdrun -deffnm md -cpi md.cpt -ntmpi 1 -ntomp $NT
else
  gmx mdrun -deffnm md -ntmpi 1 -ntomp $NT
fi

[ -f md.gro ] || { echo "incomplete - rerun to continue"; exit 0; }
echo "done: $LIG"
