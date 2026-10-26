<script lang="ts">
  import { onDestroy } from 'svelte';
  import * as HoverCard from '#lib/components/ui/hover-card';
  import { Button } from '#lib/components/ui/button';
  import BookOpen from '@lucide/svelte/icons/book-open';
  import ArrowUpRight from '@lucide/svelte/icons/arrow-up-right';
  import Math from './Math.svelte';
  import { useFormulaPreviews } from '#lib/formula-preview.svelte';
  import type { Formula, Locale, SourceRef, SourceDocument } from '#lib/types';
  let {formula,locale,documents,onsource,compact = false}: {formula: Formula; locale: Locale; documents:Record<string,SourceDocument>; onsource:(s:SourceRef)=>void; compact?:boolean} = $props();
  const previews = useFormulaPreviews();
  const previewId = Symbol();
  const open = $derived(previews.active === previewId);
  onDestroy(() => previews.setOpen(previewId, false));
  function showSource() {
    previews.active = null;
    onsource(formula.source);
  }
</script>
<HoverCard.Root bind:open={() => open, (value) => previews.setOpen(previewId, value)} openDelay={180} closeDelay={160}>
  <HoverCard.Trigger href={`${documents[formula.source.doc].pdf}#page=${formula.source.page}`} class="formula-link" onclick={(e) => {e.preventDefault(); showSource();}} aria-label={`${formula.title[locale]} · ${formula.source.label[locale]}`}>
    <BookOpen aria-hidden="true" />
    <span>{formula.title[locale]}</span>
    {#if !compact}<span class="reference-page">p.{formula.source.page}</span>{/if}
  </HoverCard.Trigger>
  <HoverCard.Content hidden={!open} class="w-80 max-w-[calc(100vw-2rem)]">
    <div class="excerpt-heading"><strong>{formula.title[locale]}</strong><span>{formula.source.doc === 'crib' ? 'CRIB' : 'LECTURE 04'} / {formula.source.page}</span></div>
    <div class="excerpt-equation"><Math tex={formula.math} display /></div>
    <div class="original-excerpt"><img src={`/excerpts/${formula.id}.webp`} alt={formula.source.label[locale]} loading="lazy" /></div>
    <p class="excerpt-description">{locale === 'zh' ? '来自原始 PDF 的公式区域' : 'Excerpt from the original PDF'}</p>
    <Button size="sm" variant="secondary" onclick={showSource}><ArrowUpRight data-icon="inline-start" aria-hidden="true" />{locale === 'zh' ? '打开原页并定位' : 'Locate on original page'}</Button>
  </HoverCard.Content>
</HoverCard.Root>
