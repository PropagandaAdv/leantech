"""Vista ravvicinata di un prodotto con colori CAD. Uso: prodview.py FILE PRODOTTO out.png az el distfac [cx cy cz in mm blender frame]"""
import sys; sys.path.insert(0,"scripts")
from lib import *
code,pname,out=sys.argv[1:4]; az,el,df=[float(x) for x in sys.argv[4:7]]
reset(); sc=setup_cycles(32,(1280,720))
d=load(code); V,N,F,FP,FC,prods,cols=[d[k] for k in("V","N","F","FP","FC","prods","cols")]
pi=list(prods).index(pname); m=FP==pi
vi=np.unique(F[m].ravel()); pv=V[vi]; lo,hi=pv.min(0),pv.max(0); c=(lo+hi)/2
if len(sys.argv)>7: c=np.array([float(x) for x in sys.argv[7:10]])/1000
for ci,col in enumerate(cols):
    mm=m&(FC==ci)
    if mm.any():
        ob=mesh_obj(f"c{ci}",V,N,F[mm]); rgb=tuple((np.array(col)/255.0)**2.2) if col[0]>=0 else (.5,.5,.5)
        ob.data.materials.append(flat_mat(f"c{ci}",rgb,0.5))
w=bpy.data.worlds.new("w"); w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.9,0.9,0.9,1); sc.world=w
r=np.linalg.norm(hi-lo)/2*df; a=math.radians(az); e=math.radians(el)
camera((c[0]+r*math.cos(e)*math.sin(a), c[1]-r*math.cos(e)*math.cos(a), c[2]+r*math.sin(e)),tuple(c),35)
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
