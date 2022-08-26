import os

for sub in os.listdir("3D_single_tex"):
  if not os.path.isdir(os.path.join("3D_single_tex/", sub)): continue
  hp = os.path.join("3D_single_tex/", sub, "hp.obj")
  if not os.path.exists(hp): continue
  tgt_dir = os.path.join("3D_alpha_wrapped", sub)
  os.makedirs(tgt_dir, exist_ok=True)
  tgt = os.path.join(tgt_dir, "hp.obj")

  os.system(f"alpha-wrap {hp} {tgt} 60 200")
