# 3D model dataset

A collection of 3D models for use with experimenting.
Currently private since lacking artist attribution.

# Pipeline

`raw`:
- GLTF files with a file called `scene.gltf`
ISSUE: NVDiffmod needs OBJ files with 1 texture
Fix by using Blender->
This is done by running the script in `process_dataset.blend`.


`objs`:
- High-Poly OBJ file called `hp.obj`
ISSUE: Multiple texture files, need to combine them
Fix by reparameterizing and raycasting->

This is done by calling `python3 unify_texs.py`

`processed`:
- High-Poly OBJ file called `hp.obj`

Then from the high-poly files can derive low-poly files using Alpha Wrapping, Simplygon, etc.

This can be done by calling `python3 reduction.py` with Simplygon installed,
or by calling `python3 alpha_wrap.py && post_alpha_wrap_retex.py` with CGAL installed.

Each of those scripts usually shells out to another script with some parameters set.
