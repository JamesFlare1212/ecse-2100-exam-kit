<script lang="ts">
  import * as ToggleGroup from '#lib/components/ui/toggle-group';
  import * as Dialog from '#lib/components/ui/dialog';
  import { Button } from '#lib/components/ui/button';
  import Expand from '@lucide/svelte/icons/expand';
  import FileSearch from '@lucide/svelte/icons/file-search';
  import SphericalFigure from './SphericalFigure.svelte';
  import type { Locale, Localized, SourceRef } from '#lib/types';
  let {name,locale,dark=false,caption,original,onsource,interactive=false}: {name:string;locale:Locale;dark?:boolean;caption?:Localized;original?:{doc:string;page:number;region:[number,number,number,number]};onsource?:(s:SourceRef)=>void;interactive?:boolean}=$props();
  let view=$state('recreated');
  let zoom=$state(false);
  let error=$state(false);
  let dimensions=$state<{name:string;ratio:number}|null>(null);
  const spherical=$derived(interactive&&name==='e2-f25-q1');
  const vectorSrc=$derived(`/figures/${name}${dark?'-dark':''}.svg`);
  const aspectRatio=$derived(dimensions?.name===name?dimensions.ratio:undefined);
  const src=$derived(view==='original' ? `/original-figures/${name}.webp` : `/figures/${name}${dark?'-dark':''}.svg`);
  $effect(()=>{name;view=spherical?'3d':'recreated';});
  $effect(()=>{src;error=false;});
  function rememberDimensions(event:Event) {
    const img=event.currentTarget as HTMLImageElement;
    if(view==='recreated'&&img.naturalHeight) dimensions={name,ratio:img.naturalWidth/img.naturalHeight};
  }
</script>
<figure class="study-figure" class:spatial-figure={spherical} data-figure={name}>
  <div class="figure-toolbar">
    <span class="figure-label">{spherical?(locale==='zh'?'3D 空间结构':'3D GEOMETRY'):(locale==='zh'?'图示':'FIGURE')} <span>↗</span></span>
    <div class="flex items-center gap-2">
      {#if original}
        <ToggleGroup.Root type="single" variant="outline" size="sm" value={view} onValueChange={(v)=>{if(v)view=v;}} aria-label={locale==='zh'?'图像版本':'Figure version'}>
          {#if spherical}<ToggleGroup.Item value="3d">{locale==='zh'?'3D 模型':'3D model'}</ToggleGroup.Item>{/if}
          <ToggleGroup.Item value="recreated">{locale==='zh'?'矢量复刻':'Recreated SVG'}</ToggleGroup.Item>
          <ToggleGroup.Item value="original">{locale==='zh'?'原始插图':'Original'}</ToggleGroup.Item>
        </ToggleGroup.Root>
      {/if}
      <Button size="icon-sm" variant="ghost" onclick={()=>zoom=true} aria-label={locale==='zh'?'放大图示':'Enlarge figure'}><Expand aria-hidden="true" /></Button>
    </div>
  </div>
  <div class:original-figure={view==='original'} class="figure-image">
    <div class="figure-canvas" class:spatial-canvas={spherical} class:measured={spherical||!!aspectRatio} style:aspect-ratio={spherical?1.6:aspectRatio}>
      {#if view==='3d'&&spherical}<SphericalFigure {locale} {dark} fallback={vectorSrc}/>{:else if error}<p>{locale==='zh'?'图示加载失败，请查看原卷。':'Figure could not load. Please view the source exam.'}</p>{:else}<img {src} alt={caption?.[locale]??(locale==='zh'?'解题图示':'Solution diagram')} onload={rememberDimensions} onerror={()=>error=true} />{/if}
    </div>
  </div>
  {#if original&&onsource}
    <div class="figure-source">
      <Button size="xs" variant="ghost" onclick={()=>onsource?.({...original,label:{zh:'原始插图',en:'Original figure'}})}><FileSearch data-icon="inline-start" aria-hidden="true" />{locale==='zh'?'在原始试卷中定位':'Locate in the source exam'} · p.{original.page}</Button>
    </div>
  {/if}
</figure>
<Dialog.Root bind:open={zoom}>
  <Dialog.Content closeLabel={locale==='zh'?'关闭':'Close'} class={spherical?'figure-dialog sphere-dialog sm:max-w-5xl':'figure-dialog sm:max-w-5xl'}>
    <Dialog.Header><Dialog.Title>{locale==='zh'?'图示详情':'Figure detail'}</Dialog.Title><Dialog.Description>{spherical?(locale==='zh'?'球对称几何的三维剖切辅助视图，比例仅为示意。':'Interactive cutaway of the spherical geometry, with schematic proportions.'):(caption?.[locale]??name)}</Dialog.Description></Dialog.Header>
    {#if view==='3d'&&spherical}<div class="figure-enlarged sphere-enlarged"><SphericalFigure {locale} {dark} fallback={vectorSrc}/></div>{:else}<div class:original-figure={view==='original'} class="figure-enlarged"><img {src} alt={caption?.[locale]??name}/></div>{/if}
    <Dialog.Footer><Button variant="secondary" onclick={()=>zoom=false}>{locale==='zh'?'返回解题':'Back to problem'}</Button></Dialog.Footer>
  </Dialog.Content>
</Dialog.Root>
