#!/usr/bin/env bash
set -u
J=~/divyashree/pahp_md/jobs
run () {
  local dir=$1 name=$2 start=$3 end=$4
  mkdir -p "$dir/$name"
  cd "$dir/$name" || return 1
  cat > mmpbsa.in <<IN
&general
sys_name = "$(basename $dir)_$name"
startframe = $start
endframe = $end
interval = 1
verbose = 2
temperature = 310
/
&gb
igb = 5
saltcon = 0.150
/
IN
  echo "=== $(basename $dir) $name  frames $start-$end  $(date +%H:%M) ==="
  gmx_MMPBSA -O -i mmpbsa.in -cs ../md.tpr -ct ../md_fit.xtc -ci ../index.ndx -cg 1 13 \
             -cp ../topol.top -o FINAL_RESULTS.dat -eo FINAL_RESULTS.csv > run.log 2>&1
  if [ -f FINAL_RESULTS.dat ]; then
    grep -iE "^(DELTA TOTAL|TOTAL)" FINAL_RESULTS.dat | tail -1
  else
    echo "FAILED - see $PWD/run.log"
  fi
  cd - >/dev/null
}
run $J/pyrene_run       gb_site 251 500
run $J/pyrene_run       gb_p4    11  66
run $J/phenanthrene_run gb_site 251 500
run $J/phenanthrene_run gb_p4     6  36
echo "all done $(date +%H:%M)"
