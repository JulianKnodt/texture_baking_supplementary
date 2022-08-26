import os

def main():
    for sub in os.listdir("3D_multi_tex/"):
        mesh_dir = os.path.join("3D_multi_tex/", sub)
        if not os.path.isdir(mesh_dir): continue

        new_mesh_dir = os.path.join("3D_single_tex/", sub)
        os.makedirs(new_mesh_dir, exist_ok=True)
        # Do not re-bake already baked models.
        if os.path.exists(os.path.join(new_mesh_dir, "hp_kd.png")): continue

        hp_mtl = os.path.join(mesh_dir, "hp.mtl")
        with open(hp_mtl, 'r') as f:
            mtl = f.read()
        mtl = mtl.replace("\\\\", "/")
        with open(hp_mtl, 'w') as f:
            f.write(mtl)

        mtl.replace("\\\\", "/")
        hp = os.path.join(mesh_dir, "hp.obj")
        out = os.path.join(new_mesh_dir, "hp.obj")
        print(f"[1] Reparameterizing {sub}")
        os.system(f"python3 reparam.py --mesh {hp} --output {out}")
        print(f"[2] Removing Flipped triangles from {out}")
        os.system(f"clean --mesh {out} --output {out}")

        # bake a single texture using raycasting
        print(f"[3] Baking single texture into {out}")
        os.system(f"""
            texture_bake --output-name {out.strip('.obj')} -s {hp} -t {out} \
            --texture-width 2048 --texture-height 2048 --extrude-by 0.001
        """)

if __name__ == "__main__": main()
