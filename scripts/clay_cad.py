"""Clay con colori CAD originali. Uso: clay_cad.py CODICE out.png az el [dist_factor]"""
import sys; sys.path.insert(0,"scripts")
from lib import *
code,out=sys.argv[1],sys.argv[2]; az=math.radians(float(sys.argv[3])); el=math.radians(float(sys.argv[4]))
df=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
reset(); sc=setup_cycles(24,(1280,720))
d=load(code); V,N,F,FC,cols=d["V"],d["N"],d["F"],d["FC"],d["cols"]
for ci,c in enumerate(cols):
    m=FC==ci
    if not m.any(): continue
    rgb=tuple((np.array(c)/255.0)**2.2) if c[0]>=0 else (0.5,0.5,0.5)
    ob=mesh_obj(f"c{ci}",V,N,F[m]); ob.data.materials.append(flat_mat(f"c{ci}",rgb,0.5))
lo,hi=V.min(0),V.max(0); ctr=(lo+hi)/2; r=np.linalg.norm(hi-lo)/2*df
w=bpy.data.worlds.new("w"); w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.9,0.9,0.9,1); w.node_tree.nodes["Background"].inputs[1].default_value=1.0; sc.world=w
loc=(ctr[0]+r*2.2*math.cos(el)*math.sin(az), ctr[1]-r*2.2*math.cos(el)*math.cos(az), ctr[2]+r*2.2*math.sin(el))
camera(loc,tuple(ctr),35)
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
