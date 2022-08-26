#!/bin/python3

import trimesh
import xatlas
import argparse

def as_mesh(scene):
    if isinstance(scene, trimesh.Scene):
        if len(scene.geometry) == 0: return None
        return trimesh.util.concatenate([
            trimesh.Trimesh(vertices=g.vertices, faces=g.faces,
                vertex_normals=g.vertex_normals, face_normals=g.face_normals)
            for g in scene.geometry.values()
        ])

    assert(isinstance(scene, trimesh.Trimesh))
    return scene

def arguments():
    a = argparse.ArgumentParser()
    a.add_argument("--mesh", required=True, type=str, help="Mesh to recompute UV coordinates for")
    a.add_argument("--output", default="output.obj", help="Output OBJ name")
    a.add_argument(
        "--use-face-normals", action="store_true",
        help="Use face normals instead of vertex normals"
    )
    return a.parse_args()

def main():
    args = arguments()
    mesh = as_mesh(trimesh.load_mesh(args.mesh, force="mesh", skip_texture=True))
    n = mesh.vertex_normals
    if args.use_face_normals: n = mesh.face_normals

    atlas = xatlas.Atlas()
    atlas.add_mesh(mesh.vertices, mesh.faces, n)
    co = xatlas.ChartOptions()
    # These options are designed to reduce the number of total charts
    # as well as prevent any UV flipping. By reducing the number of charts,
    # it increases the amount of compression, which makes it easier to show
    # optimization within the chart.
    co.fix_winding = True
    #co.max_boundary_length = 1e30
    #co.max_chart_area = 1e30
    #co.max_cost = 20
    #co.max_iterations = 10000
    #co.straightness_weight = 0.01
    #co.roundness_weight = 0
    po = xatlas.PackOptions()
    po.rotate_charts = False
    po.padding = 1
    atlas.generate(co, po)

    vmap, idxs, uvs = atlas[0]

    xatlas.export(args.output, mesh.vertices[vmap], idxs, uvs, normals=n[vmap])

if __name__ == "__main__": main()
