<script lang="ts">
  import { untrack } from 'svelte';
  import * as Tabs from '#lib/components/ui/tabs';
  import * as Accordion from '#lib/components/ui/accordion';
  import { Button } from '#lib/components/ui/button';
  import { Badge } from '#lib/components/ui/badge';
  import { Separator } from '#lib/components/ui/separator';
  import { Progress } from '#lib/components/ui/progress';
  import Waves from '@lucide/svelte/icons/waves';
  import BookOpen from '@lucide/svelte/icons/book-open';
  import FileText from '@lucide/svelte/icons/file-text';
  import Bookmark from '@lucide/svelte/icons/bookmark';
  import Check from '@lucide/svelte/icons/check';
  import ShieldCheck from '@lucide/svelte/icons/shield-check';
  import { DEFAULT_PROBLEM_ID, problemPath, followProblemLink } from '#lib/problem-navigation';
  import type { StudyState } from '#lib/study.svelte';
  let {study,onselect,onlibrary,openExam=$bindable<string|undefined>()}: {study:StudyState;openExam?:string;onselect:(id:string)=>void;onlibrary:(kind:string)=>void}=$props();
  const selected=$derived(study.catalog.findProblem(study.selected));
  if(openExam===undefined)openExam=untrack(()=>study.catalog.findProblem(study.selected).exam.id);
  let lastSelected=untrack(()=>study.selected);
  const exams=$derived(study.catalog.exams.filter(exam=>exam.number===selected.exam.number));
  const partIds=$derived(exams.flatMap(exam=>exam.problems.flatMap(problem=>problem.parts.map(part=>part.id))));
  const progress=$derived(study.count(partIds));
  const examNumbers=$derived([...new Set(study.catalog.exams.map(exam=>exam.number))]);
  const home=$derived(study.catalog.findProblem(DEFAULT_PROBLEM_ID).problem.id);
  $effect(()=>{if(study.selected!==lastSelected){lastSelected=study.selected;openExam=selected.exam.id;}});
</script>
<div class="navigation-content">
  <a href={problemPath(home)} class="brand" aria-label="Fieldnotes · ECSE 2100" onclick={(event)=>followProblemLink(event,()=>onselect(home))}><span class="brand-mark"><Waves aria-hidden="true"/></span><span><strong>fieldnotes<span class="brand-dot">.</span></strong><small>ECSE 2100 · FIELDS & WAVES I</small></span></a>
  <div class="nav-body">
    <div class="nav-section-label">{study.locale==='zh'?'历年试卷':'THE EXAM ARCHIVE'}<Badge variant="outline">{study.catalog.exams.length}</Badge></div>
    <Tabs.Root value={String(selected.exam.number)} onValueChange={(v)=>{if(v&&v!==String(selected.exam.number))onselect(study.catalog.exams.filter(exam=>exam.number===Number(v)).at(-1)!.problems[0].id);}}>
      <Tabs.List class="w-full">{#each examNumbers as number(number)}<Tabs.Trigger value={String(number)}>Exam {number}</Tabs.Trigger>{/each}</Tabs.List>
    </Tabs.Root>
    <Accordion.Root type="single" value={openExam??''} onValueChange={(v)=>openExam=v} class="exam-list">
      {#each exams.toReversed() as exam(exam.id)}
        <Accordion.Item value={exam.id}>
          <Accordion.Trigger class="exam-trigger"><span class="exam-season">{exam.term[study.locale]} {exam.year}<small>{exam.points} {study.locale==='zh'?'分':'pts'} · {exam.problems.length} {study.locale==='zh'?'题':'problems'}</small></span></Accordion.Trigger>
          <Accordion.Content>
            <nav aria-label={`${exam.term[study.locale]} ${exam.year}`} class="question-navigation">
              {#each exam.problems as q(q.id)}
                {@const done=study.count(q.parts.map(p=>p.id))}
                <Button variant={q.id===study.selected?'secondary':'ghost'} class="question-link" href={problemPath(q.id)} onclick={(event)=>followProblemLink(event,()=>onselect(q.id))} aria-current={q.id===study.selected?'page':undefined}>
                  <span class="question-number">{#if done===q.parts.length}<Check aria-label={study.locale==='zh'?'已完成':'Complete'}/>{:else}{String(q.number).padStart(2,'0')}{/if}</span>
                  <span class="question-link-title">{q.title[study.locale]}<small>{done}/{q.parts.length} {study.locale==='zh'?'小问':'parts'}</small></span>
                  {#if study.bookmarks[q.id]}<Bookmark class="nav-bookmark" aria-label={study.locale==='zh'?'已收藏':'Bookmarked'}/>{/if}
                </Button>
              {/each}
            </nav>
          </Accordion.Content>
        </Accordion.Item>
      {/each}
    </Accordion.Root>
    <Separator />
    <div class="nav-section-label resource-label">{study.locale==='zh'?'学习资料':'YOUR RESOURCES'}</div>
    <div class="resource-navigation">
      <Button variant="ghost" class="resource-link" onclick={()=>onlibrary('crib')}><FileText data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?'公式表':'Crib sheet'}<span class="resource-shortcut">10 p.</span></Button>
      <Button variant="ghost" class="resource-link" onclick={()=>onlibrary('lectures')}><BookOpen data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?'课程讲义':'Lecture notes'}<span class="resource-shortcut">01–15</span></Button>
      <Button variant="ghost" class="resource-link" onclick={()=>onlibrary('bookmarks')}><Bookmark data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?'我的收藏':'Saved problems'}<span class="resource-shortcut">{study.catalog.problemEntries.filter(({problem})=>study.bookmarks[problem.id]).length}</span></Button>
    </div>
  </div>
  <div class="nav-progress">
    <div class="progress-summary"><span>{study.locale==='zh'?'学习进度':'Your progress'}</span><strong>{progress}<span> / {partIds.length}</span></strong></div>
    <Progress value={progress} max={partIds.length} aria-label={`Exam ${selected.exam.number} · ${study.locale==='zh'?'已掌握的小问':'Parts marked mastered'}`}/>
    <div class="local-status"><ShieldCheck aria-hidden="true"/>{study.storageError?(study.locale==='zh'?'更改尚未保存':'Changes not saved'):(study.locale==='zh'?'学习进度保存在此浏览器':'Progress saved in this browser')}</div>
  </div>
</div>
