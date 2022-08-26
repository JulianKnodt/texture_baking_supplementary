import os

for sub in os.listdir("3D_single_tex"):
  if not os.path.isdir(os.path.join("3D_single_tex/", sub)): continue

  hp = os.path.join("3D_single_tex/", sub, "hp.obj")
  if not os.path.exists(hp): continue

  tr = 1000
  tgt_dir = os.path.join(f"3D_simplygon{tr}", sub)
  os.makedirs(tgt_dir, exist_ok=True)
  tgt = os.path.join(tgt_dir, "hp.obj")

  os.system(f"python simplygon_remeshing.py --input {hp} --output {tgt} --triangle-ratio {tr}")
