load structure.pdb, prot
load PahP__pyrene__autodock-vina__v1.pdbqt, pyrL
load PahP__phenanthrene__autodock-vina__v1.pdbqt, phnL
split_states pyrL, 1, 1
split_states phnL, 1, 1
delete pyrL
delete phnL
set_name pyrL_0001, pyrene
set_name phnL_0001, phenanthrene
alter pyrene, elem="C"
alter phenanthrene, elem="C"
rebuild

hide everything
bg_color white
set ray_opaque_background, 1
set ray_shadows, 0
set antialias, 2
set specular, 0.2
set label_size, 19
set label_color, black
set label_font_id, 7
set label_position, (0, 2.6, 1.5)

select lining, prot and resi 123+243+245+246+247+250+270+271+272+273+274+306+307 and sidechain
select arom, prot and resi 123+271+274+306 and sidechain
select ligs, pyrene or phenanthrene

color grey70, prot
show sticks, lining
color palecyan, lining
color grey50, lining and elem N
color salmon, lining and elem O
show sticks, arom
color deepteal, arom
show sticks, ligs
color tv_blue, pyrene
color orange, phenanthrene
set stick_radius, 0.13, lining
set stick_radius, 0.16, arom
set stick_radius, 0.26, ligs
hide everything, hydro
label arom and name CZ, "%s%s" % (resn, resi)

# (1) context: whole protein, pocket highlighted
set cartoon_transparency, 0.0
show cartoon, prot
orient prot
turn y, 90
png fig_pocket4_context.png, width=1800, height=1800, dpi=300, ray=1

# (2) pocket view
set cartoon_transparency, 0.45
orient lining
zoom lining, 1.5
turn y, 12
png fig_pocket4_poses.png, width=2200, height=1550, dpi=300, ray=1

# (3) close-up on the two poses
hide cartoon, prot
show cartoon, byres (prot within 10 of ligs)
set cartoon_transparency, 0.65
orient ligs
zoom ligs, 3.5
turn x, -8
png fig_pocket4_closeup.png, width=2200, height=1550, dpi=300, ray=1
