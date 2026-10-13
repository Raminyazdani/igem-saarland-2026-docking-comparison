load structure.pdb, dock
load PahP__pyrene__autodock-vina__v1.pdbqt, pyrL
split_states pyrL, 1, 1
delete pyrL
set_name pyrL_0001, pyr_dock
alter pyr_dock, elem="C"
load md_pyr.pdb, mdpyr
align mdpyr and resi 123+250+270+271+272+274+306 and name CA, dock and resi 123+250+270+271+272+274+306 and name CA, cycles=0
create pyr_md, mdpyr and resn PYR
rebuild

hide everything
bg_color white
set ray_opaque_background, 1
set ray_shadows, 0
set antialias, 2
set specular, 0.2
set label_size, 18
set label_color, black
set label_font_id, 7
set label_position, (0, 3.2, 2.0)

select p4, mdpyr and resi 123+271+274+306 and sidechain
select deeper, mdpyr and resi 102+124+125+244 and sidechain
select ligs, pyr_dock or pyr_md

show cartoon, mdpyr
color grey75, mdpyr
set cartoon_transparency, 0.55
show sticks, p4
color palecyan, p4
show sticks, deeper
color deepteal, deeper
show sticks, pyr_dock
show sticks, pyr_md
color grey40, pyr_dock
color tv_blue, pyr_md
set stick_radius, 0.15, p4
set stick_radius, 0.15, deeper
set stick_radius, 0.26, ligs
hide everything, hydro
label mdpyr and resi 123+271+274+306+102+124+125+244 and name CA, "%s%s" % (resn, resi)

orient ligs
zoom ligs, 5.5
png fig_docked_vs_relaxed.png, width=2200, height=1550, dpi=300, ray=1
turn y, 70
png fig_docked_vs_relaxed_b.png, width=2200, height=1550, dpi=300, ray=1
