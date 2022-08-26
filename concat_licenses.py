import os

all_licenses = []
for r in os.listdir("raw"):
    license_file = os.path.join("raw", r, "license.txt")
    if not os.path.exists(license_file): continue
    with open(license_file, "r") as f:
        all_licenses.extend(f.readlines())
    all_licenses.append("\n")

with open("all_licenses.txt", "w") as f:
    f.writelines(all_licenses)

kinds = [l for l in all_licenses if "CC" in l and "under" not in l]
print("License Kinds:")
for k in set(kinds): print(k)
