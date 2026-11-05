import numpy as np, bpy, math, mathutils

def load(code):
    d = np.load(f"work/{code}.npz")
    d = {k: d[k] for k in d.files}
    # glTF (Y su, lunghezza Z) -> Blender (Z su): (x,y,z) -> (x,-z,y)
    for k in ("V", "N"):
        a = d[k]; d[k] = np.ascontiguousarray(np.stack([a[:, 0], -a[:, 2], a[:, 1]], 1))
    return d

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def mesh_obj(name, V, N, F, collection=None):
    """V,N per-vertex arrays (full), F (n,3) faces subset -> compacted object with custom split normals."""
    vi, inv = np.unique(F.ravel(), return_inverse=True)
    co = V[vi].astype(np.float32); nr = N[vi].astype(np.float32); fl = inv.reshape(-1, 3).astype(np.int32)
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(co)); me.vertices.foreach_set("co", co.ravel())
    nf = len(fl)
    me.loops.add(nf * 3); me.loops.foreach_set("vertex_index", fl.ravel())
    me.polygons.add(nf); me.polygons.foreach_set("loop_start", np.arange(nf, dtype=np.int32) * 3)
    me.update(calc_edges=True)
    me.polygons.foreach_set("use_smooth", np.ones(nf, bool))
    try:
        me.normals_split_custom_set_from_vertices(nr)
    except Exception as e:
        print("custom normals failed", e)
    ob = bpy.data.objects.new(name, me)
    (collection or bpy.context.scene.collection).objects.link(ob)
    return ob

def setup_cycles(samples=32, res=(960, 540), denoise=True):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
    sc.cycles.use_denoising = denoise
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.cycles.max_bounces = 6
    sc.render.threads_mode = "AUTO"
    return sc

def camera(loc, target, lens=35):
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.scene.collection.objects.link(cam); bpy.context.scene.camera = cam
    cam.data.lens = lens; cam.data.clip_start = 0.01; cam.data.clip_end = 200
    d = mathutils.Vector(target) - mathutils.Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler(); cam.location = loc
    return cam

def flat_mat(name, rgb, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    return m
