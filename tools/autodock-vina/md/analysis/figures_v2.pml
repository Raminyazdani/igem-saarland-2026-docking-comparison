# run from tools/autodock-vina/ :  pymol md/analysis/figures_v2.pml
reinitialize
bg_color white
set ray_opaque_background, 1
set ray_shadows, 0
set antialias, 2
set cartoon_transparency, 0.35
set stick_radius, 0.20
set sphere_scale, 0.22
set dash_width, 3
set dash_gap, 0.35
set dash_color, black
set label_size, 22
set label_color, black
set label_font_id, 7

load inputs/PahP_fixed.pdb, apo
load results/poses/PahP__pyrene__autodock-vina__v1.pdbqt, dock_pyr
load md/analysis/pyrene_75ns.pdb, md_pyr
load md/analysis/phenanthrene_75ns.pdb, md_phn
split_states dock_pyr, 1, 1
delete dock_pyr
set_name dock_pyr_0001, pose_pyr
align md_pyr and name CA, apo and name CA
align md_phn and name CA, apo and name CA

remove hydrogens
select p4, apo and resi 123+243+245+246+247+250+270+271+272+273+274+306+307
select arom4, apo and resi 123+271+274+306
select site_pyr, apo and resi 10+40+41+44+45+48+51
select site_phn, apo and resi 136+139+140+142+143+194+195+223+225+237+284+289+290+291+292
select lig_pyr, md_pyr and resn PYR
select lig_phn, md_phn and resn PHN
deselect

# ---------- figure 1 : migration ----------
hide everything
show cartoon, apo
color grey70, apo
show sticks, p4 and sidechain
color skyblue, p4 and elem C
show sticks, arom4 and sidechain
color marine, arom4 and elem C
show sticks, site_pyr and sidechain
color palegreen, site_pyr and elem C
show sticks, pose_pyr
show spheres, pose_pyr
color orange, pose_pyr and elem C
show sticks, lig_pyr
show spheres, lig_pyr
color firebrick, lig_pyr and elem C
util.cnc("elem N+O+S")
pseudoatom c_dock, selection=pose_pyr
pseudoatom c_md, selection=lig_pyr
distance migration, c_dock, c_md
hide labels, migration
hide everything, c_dock c_md
orient pose_pyr or lig_pyr
zoom apo, -6
turn y, 20
ray 1800, 1350
png md/analysis/fig_pyrene_migration.png, dpi=300

# ---------- figure 2 : docked pose in pocket 4 ----------
hide everything
show cartoon, apo
color grey70, apo
show sticks, p4 and sidechain
color skyblue, p4 and elem C
show sticks, arom4 and sidechain
color marine, arom4 and elem C
show sticks, pose_pyr
color orange, pose_pyr and elem C
util.cnc("elem N+O+S")
orient p4
zoom p4, 3
ray 1800, 1350
png md/analysis/fig_pocket4_docked.png, dpi=300

# ---------- figure 3 : phenanthrene final site ----------
hide everything
show cartoon, apo
color grey70, apo
show sticks, site_phn and sidechain
color palegreen, site_phn and elem C
show sticks, lig_phn
color firebrick, lig_phn and elem C
util.cnc("elem N+O+S")
orient site_phn
zoom site_phn, 3
ray 1800, 1350
png md/analysis/fig_phenanthrene_finalsite.png, dpi=300
