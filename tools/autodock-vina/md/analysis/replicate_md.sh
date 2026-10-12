#!/usr/bin/env bash
# Independent replicate of the 100 ns production run: fresh velocities from a new
# seed, started from npt.gro. Not a continuation of the original trajectory.
set -euo pipefail
SEED=${SEED:-20261011}
J=~/divyashree/pahp_md/jobs
MDP=~/divyashree/pahp_md/mdp/md.mdp
run () {
  local dir=$1 lig=$2
  local grp="Protein_$lig"
  cd "$dir"
  grep -q "\[ $grp \]" index.ndx || { echo "$dir: group $grp not in index.ndx" >&2; return 1; }
  mkdir -p rep2
  sed -e "s/^continuation.*/continuation    = no/" \
      -e "s/^gen_vel.*/gen_vel         = yes/" \
      -e "s/^tc-grps.*/tc-grps         = $grp Water_and_ions/" "$MDP" > rep2/md_rep2.mdp
  printf 'gen_temp        = 310\ngen_seed        = %s\nld_seed         = %s\n' "$SEED" "$SEED" >> rep2/md_rep2.mdp
  gmx grompp -f rep2/md_rep2.mdp -c npt.gro -p topol.top -n index.ndx -o rep2/md_rep2.tpr -maxwarn 2 > rep2/grompp.log 2>&1
  echo "=== $(basename $dir) replicate, seed $SEED, start $(date +%H:%M) ==="
  gmx mdrun -s rep2/md_rep2.tpr -deffnm rep2/md_rep2 -ntmpi 1 -ntomp 12 -nb gpu >> rep2/mdrun.log 2>&1
  echo "=== $(basename $dir) done $(date +%H:%M) ==="
  cd - >/dev/null
}
run $J/pyrene_run PYR
run $J/phenanthrene_run PHN
echo "both replicates finished $(date +%H:%M)"
