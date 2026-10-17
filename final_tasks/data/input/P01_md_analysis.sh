#!/usr/bin/env bash
set -euo pipefail
RUN=${1:?usage: md_analysis.sh <run_dir> <ligand_resname>}
LIG=${2:?usage: md_analysis.sh <run_dir> <ligand_resname>}
RES="123 250 270 271 272 274 306"
GRP="r_$(echo $RES | tr ' ' '_')"
OUT=$(echo "$LIG" | tr 'A-Z' 'a-z')_p4.xvg
cd "$RUN"
gmx make_ndx -f md.tpr -o p4.ndx >/dev/null 2>&1 <<EOF
r $RES
q
EOF
grep -q "$GRP" p4.ndx || { echo "group $GRP not created; check residue numbering" >&2; exit 1; }
gmx mindist -s md.tpr -f md.xtc -n p4.ndx -od "$OUT" -xvg none <<EOF
$LIG
$GRP
EOF
awk -v l="$LIG" '$2<0.5{last=$1;n++}{t++} END{printf "%s: bound %.1f%% of run, last contact %.1f ns\n", l, 100*n/t, last/1000}' "$OUT"
for T in 0 10000 25000 50000 75000 100000; do
  printf "1\n17\n" | gmx trjconv -s md.tpr -f md.xtc -o frame_$T.pdb -dump $T -pbc mol -center >/dev/null 2>&1
  awk -v t=$T -v l="$LIG" '
  $1=="ATOM"||$1=="HETATM"{
    x=substr($0,31,8)+0; y=substr($0,39,8)+0; z=substr($0,47,8)+0
    rn=substr($0,18,3); ri=substr($0,23,4)+0
    if(rn==l){lx[++L]=x; ly[L]=y; lz[L]=z} else {px[++P]=x; py[P]=y; pz[P]=z; pr[P]=rn" "ri}
  }
  END{printf "%7s ps: ", t
    for(i=1;i<=P;i++){b=1e9
      for(j=1;j<=L;j++){d=(px[i]-lx[j])^2+(py[i]-ly[j])^2+(pz[i]-lz[j])^2; if(d<b)b=d}
      if(sqrt(b)<4.5) m[pr[i]]=1}
    n=0; for(k in m){printf "%s ", k; n++}
    printf " (%d)\n", n}' frame_$T.pdb
done
