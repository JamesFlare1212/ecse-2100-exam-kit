import {
  ACESFilmicToneMapping, Color, DirectionalLight, HemisphereLight, Mesh,
  PerspectiveCamera, Raycaster, Scene, Spherical, Vector3, WebGLRenderer,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { renderMath } from '#lib/math';
import { createSphereModel, sphereLabels } from './sphere-geometry';

export interface SphereController {
  theme:(dark:boolean)=>void;
  zoom:(factor:number)=>void;
  rotate:(theta:number,phi:number)=>void;
  reset:()=>void;
  dispose:()=>void;
}
export function createSphereScene(
  host:HTMLDivElement,dark:boolean,onchange:(pose:string)=>void,onfailure:()=>void,
):SphereController {
  const canvas=document.createElement('canvas');
  const context=canvas.getContext('webgl2',{alpha:true,antialias:true});
  if(!context)throw new Error('WebGL2 unavailable');
  const renderer=new WebGLRenderer({canvas,context,alpha:true,antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.toneMapping=ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;
  renderer.setClearColor(new Color('#000000'),0);
  canvas.setAttribute('aria-hidden','true');host.append(canvas);
  const scene=new Scene(), camera=new PerspectiveCamera(36,1,.1,100);
  const model=createSphereModel(dark);scene.add(model.root);
  scene.add(new HemisphereLight(0xffffff,0x5c6d78,1.6));
  const key=new DirectionalLight(0xffffff,3.8);key.position.set(-4,6,8);scene.add(key);
  const fill=new DirectionalLight(0xc7e8ff,.8);fill.position.set(6,2,-3);scene.add(fill);
  const controls=new OrbitControls(camera,canvas);
  controls.enablePan=false;controls.enableDamping=false;controls.minDistance=7.7;controls.maxDistance=17;
  controls.minPolarAngle=.12;controls.maxPolarAngle=Math.PI-.12;controls.rotateSpeed=.7;
  // Keep normal wheel scrolling available to the surrounding reading page.
  const wheel=(event:WheelEvent)=>{if(!event.ctrlKey&&!event.metaKey)event.stopImmediatePropagation();};
  canvas.addEventListener('wheel',wheel,{capture:true,passive:true});
  const lost=(event:Event)=>{event.preventDefault();onfailure();};
  canvas.addEventListener('webglcontextlost',lost);
  const labels=sphereLabels.map(spec=>{
    const element=document.createElement('span');element.className='sphere-label';
    element.dataset.symbol=spec.tex;element.innerHTML=renderMath('\\boldsymbol{'+spec.tex+'}');element.setAttribute('aria-hidden','true');
    host.append(element);return {...spec,element};
  });
  const ray=new Raycaster(), projected=new Vector3(), direction=new Vector3();
  let width=1,height=1,disposed=false;
  function render(){
    if(disposed)return;
    renderer.render(scene,camera);
    for(const label of labels){
      projected.copy(label.position).project(camera);
      direction.subVectors(label.position,camera.position);
      const distance=direction.length();
      ray.set(camera.position,direction.normalize());
      const hit=ray.intersectObjects(model.occluders,false)[0];
      const visible=projected.z>-1&&projected.z<1&&Math.abs(projected.x)<1.1&&Math.abs(projected.y)<1.1&&(!hit||hit.distance>=distance-.05);
      label.element.style.display=visible?'block':'none';
      label.element.style.left=((projected.x*.5+.5)*width+label.dx)+'px';
      label.element.style.top=((-projected.y*.5+.5)*height+label.dy)+'px';
    }
    const pose=new Spherical().setFromVector3(camera.position);
    onchange([pose.theta,pose.phi,pose.radius].map(v=>v.toFixed(3)).join(','));
  }
  function reset(){
    camera.position.set(8.2,4.4,4.6);controls.target.set(0,0,0);controls.update();render();
  }
  function resize(){
    width=host.clientWidth;height=host.clientHeight;
    if(!width||!height)return;
    camera.aspect=width/height;
    // Keep the entire sphere visible even in a narrow phone frame.
    camera.fov=camera.aspect<1.25?44:36;camera.updateProjectionMatrix();
    renderer.setSize(width,height,false);render();
  }
  function zoom(factor:number){
    const length=Math.max(controls.minDistance,Math.min(controls.maxDistance,camera.position.length()*factor));
    camera.position.setLength(length);controls.update();render();
  }
  function rotate(theta:number,phi:number){
    const pose=new Spherical().setFromVector3(camera.position);
    pose.theta+=theta;pose.phi=Math.max(.12,Math.min(Math.PI-.12,pose.phi+phi));
    camera.position.setFromSpherical(pose);controls.update();render();
  }
  controls.addEventListener('change',render);
  const observer=new ResizeObserver(resize);observer.observe(host);
  reset();resize();
  return {
    theme:(isDark)=>{model.theme(isDark);render();},zoom,rotate,reset,
    dispose:()=>{
      disposed=true;observer.disconnect();controls.removeEventListener('change',render);controls.dispose();
      canvas.removeEventListener('wheel',wheel,{capture:true});canvas.removeEventListener('webglcontextlost',lost);
      const geometries=new Set(),materials=new Set();
      scene.traverse(object=>{
        if(object instanceof Mesh||'geometry' in object){
          const item=object as Mesh;geometries.add(item.geometry);
          for(const material of Array.isArray(item.material)?item.material:[item.material])materials.add(material);
        }
      });
      for(const geometry of geometries) (geometry as {dispose:()=>void}).dispose();
      for(const material of materials) (material as {dispose:()=>void}).dispose();
      renderer.dispose();renderer.forceContextLoss();canvas.remove();for(const label of labels)label.element.remove();
    },
  };
}
