import {expect,test} from 'bun:test';
import {ArrowHelper,Mesh,Vector3} from 'three';
import {
  INNER_RADIUS,OUTER_RADIUS,sphericalSurface,halfSection,createSphereModel,radiusDirections,
} from '../src/lib/three/sphere-geometry';

test('spherical meshes retain the correct radii and the same open quadrant',()=>{
  for(const radius of [INNER_RADIUS,OUTER_RADIUS]){
    const geometry=sphericalSurface(radius),p=geometry.getAttribute('position');
    let worstRadiusError=0,wrongQuadrant=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
      worstRadiusError=Math.max(worstRadiusError,Math.abs(Math.hypot(x,y,z)-radius));
      if(x>1e-5&&z>1e-5)wrongQuadrant++;
    }
    expect(worstRadiusError).toBeLessThan(1e-5);expect(wrongQuadrant).toBe(0);
    geometry.computeBoundingSphere();expect(geometry.boundingSphere!.center.length()).toBeLessThan(1e-5);
    geometry.dispose();
  }
});
test('section geometry ends exactly on its concentric spherical boundaries',()=>{
  for(const inner of [0,INNER_RADIUS]){
    const g=halfSection(inner,inner===0?INNER_RADIUS:OUTER_RADIUS),p=g.getAttribute('position');
    let min=Infinity,max=0,offPlane=0,negativeHalf=0;
    for(let i=0;i<p.count;i++){
      const r=Math.hypot(p.getX(i),p.getY(i));
      min=Math.min(min,r);max=Math.max(max,r);
      offPlane=Math.max(offPlane,Math.abs(p.getZ(i)));
      if(p.getX(i)<-1e-5)negativeHalf++;
    }
    expect(min).toBeCloseTo(inner,5);expect(max).toBeCloseTo(inner===0?INNER_RADIUS:OUTER_RADIUS,5);
    expect(offPlane).toBe(0);expect(negativeHalf).toBe(0);g.dispose();
  }
});
test('radius arrows share the actual sphere center and end on a and b',()=>{
  const model=createSphereModel(false);model.root.updateMatrixWorld(true);
  for(const [symbol,radius] of [['a',INNER_RADIUS],['b',OUTER_RADIUS]] as const){
    const arrow=model.root.getObjectByName('radius-'+symbol) as ArrowHelper;
    expect(arrow.position.length()).toBe(0);
    const tip=arrow.cone.getWorldPosition(new Vector3());
    expect(tip.length()).toBeCloseTo(radius,5);
    expect(tip.distanceTo(radiusDirections[symbol].clone().multiplyScalar(radius))).toBeLessThan(1e-5);
  }
  for(const mesh of model.occluders){
    expect(mesh).toBeInstanceOf(Mesh);
    for(const material of Array.isArray(mesh.material)?mesh.material:[mesh.material]){
      expect(material.transparent).toBe(false);
      expect(material.depthWrite).toBe(true);
    }
  }
  model.root.traverse(obj=>{if('geometry' in obj)(obj.geometry as {dispose:()=>void}).dispose();});
});
