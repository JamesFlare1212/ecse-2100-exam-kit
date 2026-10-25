<script lang="ts">
  import { onMount } from 'svelte';
  import { Button } from '#lib/components/ui/button';
  import RotateCcw from '@lucide/svelte/icons/rotate-ccw';
  import Plus from '@lucide/svelte/icons/plus';
  import Minus from '@lucide/svelte/icons/minus';
  import type { Locale } from '#lib/types';
  import type { SphereController } from '#lib/three/sphere-scene';
  let {locale,dark,fallback}: {locale:Locale;dark:boolean;fallback:string}=$props();
  let host=$state<HTMLDivElement>();
  let controller=$state.raw<SphereController>();
  let status=$state('loading');
  let pose=$state('');
  $effect(()=>{controller?.theme(dark);});
  onMount(()=>{
    let disposed=false;
    import('#lib/three/sphere-scene').then(({createSphereScene})=>{
      if(disposed||!host)return;
      controller=createSphereScene(host,dark,value=>pose=value,()=>status='failed');status='ready';
    }).catch(()=>{if(!disposed)status='failed';});
    return()=>{disposed=true;controller?.dispose();};
  });
  function key(event:KeyboardEvent){
    if(!controller)return;
    if(event.key==='ArrowLeft')controller.rotate(-.12,0);
    else if(event.key==='ArrowRight')controller.rotate(.12,0);
    else if(event.key==='ArrowUp')controller.rotate(0,-.1);
    else if(event.key==='ArrowDown')controller.rotate(0,.1);
    else if(event.key==='+'||event.key==='=')controller.zoom(.9);
    else if(event.key==='-')controller.zoom(1.1);
    else if(event.key==='Home')controller.reset();
    else return;
    event.preventDefault();
  }
</script>

<div class="sphere-view" data-sphere-ready={status==='ready'} data-camera={pose}>
  <!-- svelte-ignore a11y_no_noninteractive_tabindex, a11y_no_noninteractive_element_interactions (This 3D application implements keyboard camera navigation; Tab exits to the native controls.) -->
  <div class="sphere-stage" bind:this={host} role="application" tabindex="0" onkeydown={key} aria-label={locale==='zh'?'同心球三维剖切模型：拖动或方向键旋转，双指缩放，Home 重置。内球半径 a，外导体壳半径 b；比例仅为示意。':'Interactive concentric-sphere cutaway: drag or use arrow keys to rotate, pinch to zoom, Home to reset. Inner radius a, outer shell radius b; schematic proportions.'}></div>
  {#if status!=='ready'}<img class="sphere-fallback" src={fallback} alt={locale==='zh'?'同心球矢量剖切示意图':'Vector cutaway of the concentric spheres'}/>{/if}
  <div class="sphere-controls">
    <span role="status">{status==='failed'?(locale==='zh'?'3D 暂不可用，显示矢量图':'3D unavailable; showing the vector figure'):status==='loading'?(locale==='zh'?'载入 3D 模型…':'Loading 3D…'):(locale==='zh'?'比例示意 · 拖动旋转':'Schematic scale · drag to rotate')}</span>
    <div class="flex items-center gap-1">
      <Button size="icon" variant="ghost" disabled={status!=='ready'} onclick={()=>controller?.zoom(1.12)} aria-label={locale==='zh'?'缩小三维模型':'Zoom out 3D model'}><Minus aria-hidden="true"/></Button>
      <Button size="icon" variant="ghost" disabled={status!=='ready'} onclick={()=>controller?.zoom(.89)} aria-label={locale==='zh'?'放大三维模型':'Zoom in 3D model'}><Plus aria-hidden="true"/></Button>
      <Button size="icon" variant="ghost" disabled={status!=='ready'} onclick={()=>controller?.reset()} aria-label={locale==='zh'?'重置三维视角':'Reset 3D view'}><RotateCcw aria-hidden="true"/></Button>
    </div>
  </div>
</div>
