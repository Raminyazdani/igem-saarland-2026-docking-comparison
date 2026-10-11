# run from tools/autodock-vina/ :  pymol -cq md/analysis/figures.pml
reinitialize
set ray_opaque_background, 1
bg_color white
set cartoon_transparency, 0.55
set ray_shadows, 0
set antialias, 2
set ray_trace_mode, 0

load inputs/PahP_fixed.pdb, apo
load results/poses/PahP__pyrene__autodock-vina__v1.pdbqt, dock_pyr
load results/poses/PahP__phenanthrene__autodock-vina__v1.pdbqt, dock_phn
load md/analysis/pyrene_75ns.pdb, md_pyr
load md/analysis/phenanthrene_75ns.pdb, md_phn

set_name dock_pyr, dock_pyr
split_states dock_pyr, 1, 1
split_states dock_phn, 1, 1
delete dock_pyr
delete dock_phn
set_name dock_pyr_0001, pose_pyr
set_name dock_phn_0001, pose_phn

align md_pyr and name CA, apo and name CA
align md_phn and name CA, apo and name CA

select p4, apo and resi 123+243+245+246+247+250+270+271+272+273+274+306+307
select arom4, apo and resi 123+271+274+306
select site_pyr, apo and resi 10+40+41+44+45+48+51
select site_phn, apo and resi 136+139+140+142+143+194+195+223+225+237+284+289+290+291+292
select lig_md_pyr, md_pyr and resn PYR
select lig_md_phn, md_phn and resn PHN

hide everything
show cartoon, apo
color grey80, apo
show sticks, p4 and not (name C+N+O)
color skyblue, p4 and elem C
show sticks, arom4 and not (name C+N+O)
color marine, arom4 and elem C
show sticks, pose_pyr
color orange, pose_pyr and elem C
show sticks, lig_md_pyr
color firebrick, lig_md_pyr and elem C
show sticks, site_pyr and not (name C+N+O)
color palegreen, site_pyr and elem C
util.cnc("elem N+O+S")
set stick_radius, 0.16
orient apo
turn x, -15
ray 1600, 1200
png md/analysis/fig_pyrene_migration.png, dpi=300

hide everything
show cartoon, apo
color grey80, apo
show sticks, p4 and not (name C+N+O)
color skyblue, p4 and elem C
show sticks, arom4 and not (name C+N+O)
color marine, arom4 and elem C
show sticks, pose_pyr
color orange, pose_pyr and elem C
util.cnc("elem N+O+S")
orient p4
zoom p4, 4
ray 1600, 1200
png md/analysis/fig_pocket4_docked.png, dpi=300

hide everything
show cartoon, apo
color grey80, apo
show sticks, site_phn and not (name C+N+O)
color palegreen, site_phn and elem C
show sticks, lig_md_phn
color firebrick, lig_md_phn and elem C
util.cnc("elem N+O+S")
orient site_phn
zoom site_phn, 4
ray 1600, 1200
png md/analysis/fig_phenanthrene_finalsite.png, dpi=300
