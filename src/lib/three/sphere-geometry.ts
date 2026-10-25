import {
  ArrowHelper, BufferGeometry, DoubleSide, Group, Line, LineBasicMaterial,
  Mesh, MeshStandardMaterial, Shape, ShapeGeometry, SphereGeometry, Vector3,
} from 'three';

// Rendering proportions only. The exam specifies symbols a < b, not a ratio.
export const INNER_RADIUS = 0.88;
export const OUTER_RADIUS = 2.55;
export const OPEN_PHI = Math.PI;
export const RETAINED_PHI = 1.5 * Math.PI;
export const radiusDirections = {
  a: new Vector3(1, -.15, 0).normalize(),
  b: new Vector3(0, .6, 1).normalize(),
};

export function sphericalSurface(radius:number) {
  // Three's convention: x=-r cos(phi)sin(theta), z=r sin(phi)sin(theta).
  // Remove x>0,z>0. Both cut planes then pass through the same center.
  return new SphereGeometry(radius,96,64,OPEN_PHI,RETAINED_PHI);
}
export function halfSection(inner:number,outer:number) {
  const shape=new Shape();
  shape.moveTo(0,-outer);
  shape.absarc(0,0,outer,-Math.PI/2,Math.PI/2,false);
  if(inner>0){
    shape.lineTo(0,inner);
    shape.absarc(0,0,inner,Math.PI/2,-Math.PI/2,true);
  }else shape.lineTo(0,0);
  shape.closePath();
  return new ShapeGeometry(shape,64);
}
export function createSphereModel(dark:boolean) {
  const root=new Group();
  root.name='concentric-spherical-cutaway';
  const shell=new MeshStandardMaterial({side:DoubleSide,roughness:.63,metalness:.25});
  const core=new MeshStandardMaterial({side:DoubleSide,roughness:.65});
  const dielectric=new MeshStandardMaterial({side:DoubleSide,roughness:1,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1});
  const coreSection=new MeshStandardMaterial({side:DoubleSide,roughness:1,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1});
  const edge=new LineBasicMaterial({transparent:true,opacity:.75});
  const occluders:Mesh[]=[];
  function addMesh(geometry:BufferGeometry,material:MeshStandardMaterial,name:string,turn=false){
    const mesh=new Mesh(geometry,material);mesh.name=name;
    if(turn)mesh.rotation.y=-Math.PI/2;
    root.add(mesh);occluders.push(mesh);return mesh;
  }
  addMesh(sphericalSurface(OUTER_RADIUS),shell,'conducting-shell');
  addMesh(sphericalSurface(INNER_RADIUS),core,'charged-sphere');
  for(const turn of [false,true]){
    addMesh(halfSection(INNER_RADIUS,OUTER_RADIUS),dielectric,'dielectric-section',turn);
    addMesh(halfSection(0,INNER_RADIUS),coreSection,'charged-section',turn);
    for(const radius of [INNER_RADIUS,OUTER_RADIUS]){
      const points=Array.from({length:129},(_,i)=>{
        const theta=-Math.PI/2+i*Math.PI/128;
        return new Vector3(radius*Math.cos(theta),radius*Math.sin(theta),0);
      });
      const line=new Line(new BufferGeometry().setFromPoints(points),edge);
      if(turn)line.rotation.y=-Math.PI/2;
      root.add(line);
    }
  }
  const a=new ArrowHelper(radiusDirections.a,new Vector3(),INNER_RADIUS,0x187c78,.12,.065);
  const b=new ArrowHelper(radiusDirections.b,new Vector3(),OUTER_RADIUS,0xb65c3b,.16,.075);
  a.name='radius-a';b.name='radius-b';root.add(a,b);
  const center=new Mesh(new SphereGeometry(.025,12,8),coreSection);center.name='shared-center';root.add(center);
  function theme(isDark:boolean){
    shell.color.set(isDark?'#728c9b':'#a5bac4');
    core.color.set(isDark?'#568fa6':'#6b9eaf');
    dielectric.color.set(isDark?'#3a5762':'#d6e6e9');
    coreSection.color.set(isDark?'#78acb9':'#8ebdca');
    edge.color.set(isDark?'#dbe5e9':'#263746');
    a.setColor(isDark?'#86d7c9':'#187c78');
    b.setColor(isDark?'#f0a075':'#b65c3b');
  }
  theme(dark);
  return {root,occluders,theme};
}

export const sphereLabels = [
  {tex:'a',position:radiusDirections.a.clone().multiplyScalar(INNER_RADIUS*.68),dx:10,dy:-12},
  {tex:'b',position:radiusDirections.b.clone().multiplyScalar(OUTER_RADIUS*.72),dx:-12,dy:-7},
  {tex:'\\rho_0',position:new Vector3(.012,INNER_RADIUS*.15,INNER_RADIUS*.43),dx:0,dy:0},
  {tex:'\\varepsilon_0',position:new Vector3(OUTER_RADIUS*.62,-OUTER_RADIUS*.22,.012),dx:0,dy:0},
  {tex:'\\rho_{sb}',position:new Vector3(-.52,.72,.46).normalize().multiplyScalar(OUTER_RADIUS*1.05),dx:-4,dy:-10},
];
