bg_color white
set ray_opaque_background, 1
set ray_shadows, 0
set antialias, 2
set specular, 0.3
set sphere_scale, 0.26
set stick_radius, 0.11
load ../../results/poses/PahP__pyrene__autodock-vina__v1.pdbqt, pyrL
split_states pyrL, 1, 1
delete pyrL
set_name pyrL_0001, pyrene
alter pyrene, elem="C"
load ../../results/poses/PahP__phenanthrene__autodock-vina__v1.pdbqt, phnL
split_states phnL, 1, 1
delete phnL
set_name phnL_0001, phenanthrene
alter phenanthrene, elem="C"
rebuild
hide everything
show spheres, pyrene
show sticks, pyrene
color grey25, pyrene
orient pyrene
zoom pyrene, 1.2
png fig1_pyrene.png, width=1400, height=1200, dpi=300, ray=1
hide everything
show spheres, phenanthrene
show sticks, phenanthrene
color grey25, phenanthrene
orient phenanthrene
zoom phenanthrene, 1.2
png fig1_phenanthrene.png, width=1400, height=1200, dpi=300, ray=1
