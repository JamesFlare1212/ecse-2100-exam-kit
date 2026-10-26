<script lang="ts">
  import { parseText, formulaReference, hasFormulaReference, type TextNode } from '../../../content/text';
  import FormulaLink from './FormulaLink.svelte';
  import RichText from './RichText.svelte';
  import { formulaById } from '#lib/catalog';
  import type { Locale, SourceDocument, SourceRef } from '#lib/types';

  let {text,locale,documents,onsource}: {
    text:string; locale:Locale; documents:Record<string,SourceDocument>; onsource:(source:SourceRef)=>void;
  } = $props();
  const tree = $derived(parseText(text));
  const source = (node:TextNode) => text.slice(node.position?.start.offset, node.position?.end.offset);
</script>

{#snippet render(node:TextNode)}
  {@const id = formulaReference(node)}
  {#if node.type === 'text'}
    {#each node.value.split('\n') as line,i}{#if i}<br/>{/if}{line}{/each}
  {:else if id && formulaById[id]}
    <FormulaLink formula={formulaById[id]} {locale} {documents} {onsource} inline>
      {#if 'children' in node}{#each node.children as child}{@render render(child)}{/each}{/if}
    </FormulaLink>
  {:else if !hasFormulaReference(node)}
    <RichText text={source(node)}/>
  {:else if node.type === 'emphasis'}
    <em>{#each node.children as child}{@render render(child)}{/each}</em>
  {:else if node.type === 'strong' || node.type === 'heading'}
    <strong>{#each node.children as child}{@render render(child)}{/each}</strong>
  {:else if node.type === 'list'}
    <span class="markdown-list" role="list">{#each node.children as item,i}<span class="markdown-list-item" role="listitem"><span aria-hidden="true">{node.ordered ? `${(node.start ?? 1) + i}.` : '•'}</span><span>{@render render(item)}</span></span>{/each}</span>
  {:else if node.type === 'blockquote'}
    <span class="markdown-quote">{#each node.children as child,i}{#if i}<br/><br/>{/if}{@render render(child)}{/each}</span>
  {:else if 'children' in node}
    {#each node.children as child}{@render render(child)}{/each}
  {/if}
{/snippet}

<span class="rich-text">{#each tree.children as node,i}{#if i}<br/><br/>{/if}{@render render(node)}{/each}</span>
