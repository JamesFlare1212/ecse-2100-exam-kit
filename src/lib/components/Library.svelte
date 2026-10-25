<script lang="ts">
  import * as Dialog from '#lib/components/ui/dialog';
  import * as Tabs from '#lib/components/ui/tabs';
  import * as Empty from '#lib/components/ui/empty';
  import { Button } from '#lib/components/ui/button';
  import { Input } from '#lib/components/ui/input';
  import BookOpen from '@lucide/svelte/icons/book-open';
  import Bookmark from '@lucide/svelte/icons/bookmark';
  import FileText from '@lucide/svelte/icons/file-text';
  import ArrowUpRight from '@lucide/svelte/icons/arrow-up-right';
  import { formulas, documents, lectureTitles, problemEntries } from '#lib/catalog';
  import FormulaLink from './FormulaLink.svelte';
  import Math from './Math.svelte';
  import type { SourceRef } from '#lib/types';
  import type { StudyState } from '#lib/study.svelte';
  let {open=$bindable(false),kind=$bindable('crib'),study,onsource,onselect}: {open?:boolean;kind?:string;study:StudyState;onsource:(s:SourceRef)=>void;onselect:(id:string)=>void}=$props();
  let query=$state('');
  const filtered=$derived(formulas.filter(f=>(f.title.zh+' '+f.title.en+' '+f.math).toLowerCase().includes(query.toLowerCase())));
  const bookmarks=$derived(problemEntries.filter(({problem})=>study.bookmarks[problem.id]));
</script>
<Dialog.Root bind:open>
  <Dialog.Content closeLabel={study.locale==='zh'?'关闭':'Close'} class="library-dialog sm:max-w-4xl">
    <Dialog.Header><Dialog.Title>{study.locale==='zh'?'课程资料库':'The course library'}</Dialog.Title><Dialog.Description>{study.locale==='zh'?'原始公式、15 讲课件与收藏题目，随时回到出处。':'Original formulas, all 15 lectures and your saved problems.'}</Dialog.Description></Dialog.Header>
    <Tabs.Root bind:value={kind}>
      <Tabs.List><Tabs.Trigger value="crib"><FileText aria-hidden="true"/>{study.locale==='zh'?'公式表':'Crib sheet'}</Tabs.Trigger><Tabs.Trigger value="lectures"><BookOpen aria-hidden="true"/>{study.locale==='zh'?'课件':'Lecture notes'}</Tabs.Trigger><Tabs.Trigger value="bookmarks"><Bookmark aria-hidden="true"/>{study.locale==='zh'?'收藏':'Saved'}</Tabs.Trigger></Tabs.List>
      <Tabs.Content value="crib">
        <div class="library-formula-toolbar"><label for="formula-search" class="sr-only">{study.locale==='zh'?'搜索公式':'Search formulas'}</label><Input id="formula-search" bind:value={query} placeholder={study.locale==='zh'?'搜索公式，例如 高斯 / Gauss / impedance…':'Search formulas, e.g. Gauss, impedance…'}/><Button variant="outline" onclick={()=>onsource({doc:'crib',page:1,label:{zh:'完整公式表',en:'Full crib sheet'}})}>{study.locale==='zh'?'完整 10 页':'All 10 pages'}<ArrowUpRight data-icon="inline-end" aria-hidden="true"/></Button></div>
        <div class="library-scroll">
          {#each filtered as formula(formula.id)}<div class="library-formula"><FormulaLink {formula} locale={study.locale} {onsource}/><Math tex={formula.math} display/>{#if formula.note}<p>{formula.note[study.locale]}</p>{/if}</div>
          {:else}<Empty.Root><Empty.Header><Empty.Title>{study.locale==='zh'?'未找到公式':'No formulas found'}</Empty.Title><Empty.Description>{study.locale==='zh'?'试试中文或英文的物理量名称。':'Try a physical quantity in English or Chinese.'}</Empty.Description></Empty.Header></Empty.Root>{/each}
        </div>
      </Tabs.Content>
      <Tabs.Content value="lectures"><div class="library-scroll lecture-library">
        {#each Object.entries(lectureTitles) as [number,title](number)}{@const doc=documents[`lecture-${number.padStart(2,'0')}`]}<Button variant="ghost" class="library-lecture" onclick={()=>onsource({doc:doc.id,page:1,label:title})}><span class="library-lecture-number">{number.padStart(2,'0')}</span><span><strong>{title[study.locale]}</strong><small>Lecture {number} · {doc.pages} {study.locale==='zh'?'页':'pages'}</small></span><ArrowUpRight aria-hidden="true"/></Button>{/each}
      </div></Tabs.Content>
      <Tabs.Content value="bookmarks"><div class="library-scroll">
        {#each bookmarks as {problem,exam}(problem.id)}<Button variant="ghost" class="saved-problem" onclick={()=>{onselect(problem.id);open=false;}}><Bookmark data-icon="inline-start" aria-hidden="true"/><span><strong>{problem.title[study.locale]}</strong><small>Exam {exam.number} · {exam.term[study.locale]} {exam.year} · Q{problem.number}</small></span><ArrowUpRight aria-hidden="true"/></Button>
        {:else}<Empty.Root><Empty.Header><Empty.Media variant="icon"><Bookmark aria-hidden="true"/></Empty.Media><Empty.Title>{study.locale==='zh'?'把值得再做的题留下':'Keep the problems worth revisiting'}</Empty.Title><Empty.Description>{study.locale==='zh'?'点击题目标题旁的收藏按钮，即可在这里找到。':'Use the bookmark button next to a problem title to save it here.'}</Empty.Description></Empty.Header></Empty.Root>{/each}
      </div></Tabs.Content>
    </Tabs.Root>
  </Dialog.Content>
</Dialog.Root>
