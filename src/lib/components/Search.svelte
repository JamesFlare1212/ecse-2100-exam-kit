<script lang="ts">
  import * as Dialog from '#lib/components/ui/dialog';
  import * as Empty from '#lib/components/ui/empty';
  import * as Field from '#lib/components/ui/field';
  import { Button } from '#lib/components/ui/button';
  import { Input } from '#lib/components/ui/input';
  import SearchIcon from '@lucide/svelte/icons/search';
  import ArrowUpRight from '@lucide/svelte/icons/arrow-up-right';
  import { problemEntries, formulas } from '#lib/catalog';
  import type {Locale,SourceRef} from '#lib/types';
  let {open=$bindable(false),locale,onselect,onsource}: {open?:boolean;locale:Locale;onselect:(id:string,part?:string)=>void;onsource:(s:SourceRef)=>void}=$props();
  let query=$state('');
  const normalized=$derived(query.trim().toLowerCase());
  const matches=$derived(problemEntries.filter(({problem,exam})=>!normalized||[problem.title.zh,problem.title.en,problem.topic.zh,problem.topic.en,problem.statement.zh,problem.statement.en,`exam ${exam.number}`,String(exam.year),...problem.parts.flatMap(p=>[p.prompt.zh,p.prompt.en])].join(' ').toLowerCase().includes(normalized)).slice(0,12));
  const formulaMatches=$derived(normalized?formulas.filter(f=>(f.title.zh+' '+f.title.en+' '+f.math).toLowerCase().includes(normalized)).slice(0,5):[]);
</script>
<Dialog.Root bind:open>
  <Dialog.Content closeLabel={locale==='zh'?'关闭':'Close'} class="search-dialog sm:max-w-2xl">
    <Dialog.Header><Dialog.Title>{locale==='zh'?'找到下一个理解的起点':'Find your next starting point'}</Dialog.Title><Dialog.Description>{locale==='zh'?'搜索全部 20 题、93 个小问与公式，中英文都可以。':'Search all 20 problems, 93 subparts and formulas in either language.'}</Dialog.Description></Dialog.Header>
    <Field.Group><Field.Field><Field.Label class="sr-only" for="global-search">{locale==='zh'?'搜索题目或公式':'Search problems or formulas'}</Field.Label><Input id="global-search" bind:value={query} placeholder={locale==='zh'?'例如：高斯定律、同轴、Smith…':'Try Gauss, coaxial, Smith…'}/></Field.Field></Field.Group>
    <div class="search-results" role="region" aria-label={locale==='zh'?'搜索结果':'Search results'}>
      {#if formulaMatches.length}<p class="search-group-label">{locale==='zh'?'公式':'FORMULAS'}</p>{/if}
      {#each formulaMatches as f(f.id)}<Button variant="ghost" class="search-result" onclick={()=>{open=false;onsource(f.source);}}><SearchIcon data-icon="inline-start" aria-hidden="true"/><span><strong>{f.title[locale]}</strong><small>{f.source.label[locale]}</small></span><ArrowUpRight aria-hidden="true"/></Button>{/each}
      {#if matches.length}<p class="search-group-label">{locale==='zh'?'题目':'PROBLEMS'}</p>{/if}
      {#each matches as {exam,problem}(problem.id)}<Button variant="ghost" class="search-result" onclick={()=>{const part=normalized?problem.parts.find(p=>(p.prompt.zh+' '+p.prompt.en).toLowerCase().includes(normalized)):undefined;onselect(problem.id,part?.id);open=false;}}><span class="search-question-number">{String(problem.number).padStart(2,'0')}</span><span><strong>{problem.title[locale]}</strong><small>Exam {exam.number} · {exam.term[locale]} {exam.year} · {problem.parts.length} {locale==='zh'?'小问':'parts'}</small></span><ArrowUpRight aria-hidden="true"/></Button>{/each}
      {#if !matches.length&&!formulaMatches.length}<Empty.Root><Empty.Header><Empty.Media variant="icon"><SearchIcon aria-hidden="true"/></Empty.Media><Empty.Title>{locale==='zh'?'暂时没有匹配结果':'No matching results'}</Empty.Title><Empty.Description>{locale==='zh'?'试试较短的关键词，或换一种语言搜索。':'Try a shorter keyword or search in the other language.'}</Empty.Description></Empty.Header></Empty.Root>{/if}
    </div>
    <p class="search-hint">{locale==='zh'?'使用 Tab 选择结果，Enter 打开，Esc 关闭。':'Tab to a result, Enter to open, Esc to close.'}</p>
  </Dialog.Content>
</Dialog.Root>
