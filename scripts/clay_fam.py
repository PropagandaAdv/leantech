"""Clay per famiglia materiale. Uso: clay_fam.py CODICE out.png az el distfac [cx cy cz mm, frame glTF->blender]"""
import sys; sys.path.insert(0,"scripts")
from lib import *
import facemat
PAL={"ALU6061":(0.75,0.85,1.0),"INOX":(0.9,0.55,0.1),"INOX_VITE":(1,0.9,0.1),"RETE_STD":(0.25,0.25,0.28),"RETE_ACC":(0.1,0.3,1.0),"RETE_FRE":(0.7,0.7,0.7),
"FRECCIA":(1,1,1),"MOTORE":(0.9,0.05,0.05),"GOMMA":(0.02,0.02,0.02),"PL_NERO":(0.25,0.05,0.4),"PL_GRIGIO":(0.4,0.4,0.4),"PL_BLU":(0.0,0.7,1.0),
"PL_NAVY":(0.0,0.05,0.4),"PL_ROSSO":(1,0.2,0.4),"PL_VERDE":(0.1,0.8,0.1),"PL_CAVO":(0.9,0.9,0.9),"PL_PIGNONE":(0.6,0.9,0.4),"PL_SENSORE":(0.5,0.1,0.1)}
code,out=sys.argv[1],sys.argv[2]; az,el,df=[float(x) for x in sys.argv[3:6]]
reset(); sc=setup_cycles(24,(1280,720))
d=load(code); V,N,F=d["V"],d["N"],d["F"]
fams,fid,_=facemat.face_families(code, {k:d[k] for k in d})
for i,f in enumerate(fams):
    m=fid==i; ob=mesh_obj(f,V,N,F[m]); ob.data.materials.append(flat_mat(f,tuple(np.array(PAL.get(f,(1,0,1)))**2.2),0.5))
lo,hi=V.min(0),V.max(0); c=(lo+hi)/2
if len(sys.argv)>6: c=np.array([float(x) for x in sys.argv[6:9]])/1000
r=np.linalg.norm(hi-lo)/2*df; a=math.radians(az); e=math.radians(el)
w=bpy.data.worlds.new("w"); w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.9,0.9,0.9,1); sc.world=w
camera((c[0]+r*2.2*math.cos(e)*math.sin(a), c[1]-r*2.2*math.cos(e)*math.cos(a), c[2]+r*2.2*math.sin(e)),tuple(c),35)
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
