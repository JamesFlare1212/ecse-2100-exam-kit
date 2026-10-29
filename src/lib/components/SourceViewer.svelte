<script lang="ts">
  import { tick } from 'svelte';
  import * as Dialog from '#lib/components/ui/dialog';
  import { Button } from '#lib/components/ui/button';
  import { Input } from '#lib/components/ui/input';
  import SourceOverview from './SourceOverview.svelte';
  import ChevronLeft from '@lucide/svelte/icons/chevron-left';
  import ChevronRight from '@lucide/svelte/icons/chevron-right';
  import ArrowUpRight from '@lucide/svelte/icons/arrow-up-right';
  import ZoomIn from '@lucide/svelte/icons/zoom-in';
  import ZoomOut from '@lucide/svelte/icons/zoom-out';
  import Download from '@lucide/svelte/icons/download';
  import type { SourceRef, Locale, SourceDocument } from '#lib/types';
  let {source,locale,documents,onclose,onCloseAutoFocus}: {source:SourceRef|null;locale:Locale;documents:Record<string,SourceDocument>;onclose:()=>void;onCloseAutoFocus?:(event:Event)=>void}=$props();
  let requestedPage=$state(1);
  let zoom=$state(100);
  let pageInput=$state('1');
  let failed=$state(false);
  let retry=$state(0);
  let stage=$state<HTMLDivElement>();
  let paper=$state<HTMLDivElement>();
  let content=$state<HTMLDivElement|null>(null);
  const doc=$derived(source?documents[source.doc]:undefined);
  const page=$derived(Math.max(1,Math.min(doc?.pages??1,requestedPage)));
  const size=$derived(doc?.sizes[page-1]??[1,1]);
  const region=$derived(source&&page===source.page?source.region:undefined);
  $effect(()=>{if(source){requestedPage=source.page;zoom=100;pageInput=String(source.page);failed=false;retry=0;}});
  $effect(()=>{pageInput=String(page);failed=false;});
  function go(n:number){if(doc&&Number.isFinite(n)){requestedPage=Math.max(1,Math.min(doc.pages,Math.round(n)));pageInput=String(requestedPage);}}
  function commitPage(){const value=String(pageInput??'').trim();if(value)go(Number(value));pageInput=String(page);}
  $effect(()=>{zoom;page;void tick().then(focusRegion);});
  function focusRegion(){
    if(stage&&paper){
      stage.scrollTop=0;stage.scrollLeft=0;
      if(region){
        const frame=stage.getBoundingClientRect(), sheet=paper.getBoundingClientRect();
        stage.scrollTop=sheet.top-frame.top+(region[1]+region[3]/2)*sheet.height-stage.clientHeight/2;
        stage.scrollLeft=sheet.left-frame.left+(region[0]+region[2]/2)*sheet.width-stage.clientWidth/2;
      }
    }
  }
</script>
<Dialog.Root open={Boolean(source)} onOpenChange={(value)=>{if(!value)onclose();}}>
  <Dialog.Content bind:ref={content} {onCloseAutoFocus} onOpenAutoFocus={(event)=>{event.preventDefault();content?.querySelector<HTMLInputElement>('input')?.focus();}} closeLabel={locale==='zh'?'关闭':'Close'} class="source-dialog sm:max-w-5xl">
    <Dialog.Header>
      <Dialog.Title>{source?.label[locale]??(locale==='zh'?'原始资料':'Original source')}</Dialog.Title>
      <Dialog.Description>{doc?.title} · {locale==='zh'?'页码按 PDF 页序；橙框标记引用区域。':'PDF page numbering; the orange box marks the cited region.'}</Dialog.Description>
    </Dialog.Header>
    {#if doc&&source}
      <div class="source-toolbar">
        <div class="source-page-controls">
          <Button variant="outline" size="icon" disabled={page<=1} onclick={()=>go(page-1)} aria-label={locale==='zh'?'上一页':'Previous page'}><ChevronLeft aria-hidden="true"/></Button>
          <label for="source-page" class="sr-only">{locale==='zh'?'PDF 页码':'PDF page'}</label><Input id="source-page" class="w-14" type="number" min={1} max={doc.pages} bind:value={pageInput} onchange={commitPage} onkeydown={(e)=>{if(e.key==='Enter')commitPage();}}/>
          <span class="source-page-total">/ {doc.pages}</span>
          <Button variant="outline" size="icon" disabled={page>=doc.pages} onclick={()=>go(page+1)} aria-label={locale==='zh'?'下一页':'Next page'}><ChevronRight aria-hidden="true"/></Button>
        </div>
        <div class="source-zoom-controls"><Button size="icon" variant="outline" onclick={()=>zoom=Math.max(70,zoom-20)} disabled={zoom<=70} aria-label={locale==='zh'?'缩小':'Zoom out'}><ZoomOut aria-hidden="true"/></Button><span class="zoom-label">{zoom}%</span><Button size="icon" variant="outline" onclick={()=>zoom=Math.min(200,zoom+20)} disabled={zoom>=200} aria-label={locale==='zh'?'放大':'Zoom in'}><ZoomIn aria-hidden="true"/></Button></div>
      </div>
      <div class="source-viewer-layout">
      <!-- svelte-ignore a11y_no_noninteractive_tabindex (The source reading region must support keyboard scrolling.) -->
      <div class="source-stage" bind:this={stage} role="region" tabindex="0" aria-label={locale==='zh'?'原页阅读区，方向键滚动':'Source reading area; use arrow keys to scroll'}>
        {#if failed}<p class="source-failed">{locale==='zh'?'预览暂不可用，可重试或打开原始 PDF。':'Preview unavailable. Retry or open the original PDF below.'}</p><Button variant="outline" onclick={()=>{retry++;failed=false;}}>{locale==='zh'?'重试预览':'Retry preview'}</Button>{:else}
          <div class="source-paper" bind:this={paper} style:width={`${zoom}%`} style:aspect-ratio={`${size[0]} / ${size[1]}`}>
            <img src={`${doc.pageBase}/${page}.webp${retry?'?retry='+retry:''}`} alt={locale==='zh'?`${doc.title}，第 ${page} 页`:`${doc.title}, page ${page}`} onload={focusRegion} onerror={()=>failed=true}/>
            {#if region}<div class="source-highlight" data-source-highlight style:left={`${region[0]*100}%`} style:top={`${region[1]*100}%`} style:width={`${region[2]*100}%`} style:height={`${region[3]*100}%`} role="img" aria-label={locale==='zh'?'引用区域':'Cited region'}></div>{/if}
          </div>
        {/if}
      </div>
      {#if !failed}<SourceOverview {stage} {paper} {doc} {page} {source} {locale} onpage={go}/>{/if}
      </div>
      <Dialog.Footer class="source-footer">
        <span class="source-origin">{locale==='zh'?'原始课程资料':'Original course material'} · {doc.kind==='lecture'?'LECTURE':'PDF'}</span>
        <Button variant="outline" href={doc.pdf} download><Download data-icon="inline-start" aria-hidden="true"/>{locale==='zh'?'下载':'Download'}</Button>
        <Button href={`${doc.pdf}#page=${page}`} target="_blank" rel="noopener noreferrer"><ArrowUpRight data-icon="inline-start" aria-hidden="true"/>{locale==='zh'?'打开原始 PDF':'Open original PDF'}</Button>
      </Dialog.Footer>
    {/if}
  </Dialog.Content>
</Dialog.Root>
