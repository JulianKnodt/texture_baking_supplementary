import os

def main():
    for sub in os.listdir("3D_simplygon/"):
        mesh_dir = os.path.join("3D_simplygon/", sub)
        if not os.path.isdir(mesh_dir): continue

        hp = os.path.join(mesh_dir, "hp.obj")
        print(f"[1] Reparameterizing {sub}")
        os.system(f"python3 reparam.py --mesh {hp} --output {hp}")

if __name__ == "__main__": main()
