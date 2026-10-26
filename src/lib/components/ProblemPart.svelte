<script lang="ts">
  import * as Accordion from '#lib/components/ui/accordion';
  import * as Alert from '#lib/components/ui/alert';
  import { Button } from '#lib/components/ui/button';
  import { Badge } from '#lib/components/ui/badge';
  import Check from '@lucide/svelte/icons/check';
  import Info from '@lucide/svelte/icons/info';
  import FileText from '@lucide/svelte/icons/file-text';
  import Math from './Math.svelte';
  import RichText from './RichText.svelte';
  import FormulaLink from './FormulaLink.svelte';
  import Figure from './Figure.svelte';
  import { formulaById } from '#lib/catalog';
  import { conclusionMath } from '#lib/answer-math';
  import type { Part, SourceRef, ExamInfo } from '#lib/types';
  import type { StudyState } from '#lib/study.svelte';
  let {part,study,exam,dark,assetBase,onsource}: {assetBase:string;part:Part;study:StudyState;exam:ExamInfo;dark:boolean;onsource:(s:SourceRef)=>void}=$props();
  const done=$derived(Boolean(study.completed[part.id]));
  const conclusion=$derived(conclusionMath(part.steps.at(-1)?.math,part.answer));
  function source(solution=false){onsource({doc:solution?exam.solutionDoc:exam.doc,page:solution?part.solutionPage:part.sourcePage,label:{zh:solution?'官方解答原页':'原始试题',en:solution?'Official solution page':'Original question'}});}
</script>
<Accordion.Item value={part.id} class="problem-part" data-part={part.id}>
  <Accordion.Trigger class="part-trigger" level={3}><span class:complete={done} class="part-letter">{#if done}<Check aria-label={study.locale==='zh'?'已掌握':'Mastered'}/>{:else}{part.label}{/if}</span><span class="part-prompt" lang={study.locale==='zh'?'zh-CN':'en'} data-original-prompt><RichText text={part.prompt[study.locale]}/></span>{#if part.points>0}<Badge variant="outline">{part.points} {study.locale==='zh'?'分':'pts'}</Badge>{/if}</Accordion.Trigger>
  {#if part.questionFigure}<div class="part-question-figure"><Figure {assetBase} name={part.questionFigure.name} locale={study.locale} {dark} caption={part.questionFigure.caption} original={part.questionFigure.source} {onsource}/></div>{/if}
  <Accordion.Content class="part-content">
      <div class="solution-steps">
        {#each part.steps as step,i(i)}
          <div class="solution-step" data-answer={i===part.steps.length-1?part.id:undefined}><span class="step-number">{String(i+1).padStart(2,'0')}</span><div class="step-content"><p><RichText text={step.text[study.locale]}/></p>{#if i===part.steps.length-1}{#if conclusion.calculation}<Math tex={conclusion.calculation} display/>{/if}<Math tex={conclusion.result} display/>{#if part.answerText}<p><RichText text={part.answerText[study.locale]}/></p>{/if}{:else if step.math}<Math tex={step.math} display/>{/if}{#if step.refs.length}<div class="step-references">{#each step.refs as id(id)}<FormulaLink documents={study.catalog.documents} formula={formulaById[id]} locale={study.locale} {onsource} compact/>{/each}</div>{/if}</div></div>
        {/each}
      </div>
      {#if part.figure}<Figure {assetBase} name={part.figure} locale={study.locale} {dark} caption={part.figureCaption}/>{/if}
      {#if part.note}<Alert.Root class="solution-note"><Info aria-hidden="true"/><Alert.Title>{study.locale==='zh'?'核对说明':'Source check'}</Alert.Title><Alert.Description><RichText text={part.note[study.locale]}/></Alert.Description></Alert.Root>{/if}
    <div class="part-actions">
      <div class="flex flex-wrap items-center gap-2">
        <Button variant={done?'secondary':'outline'} size="sm" onclick={()=>study.completed[part.id]=!done}><Check data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?(done?'已掌握 · 撤销':'标记已掌握'):(done?'Mastered · undo':'Mark as mastered')}</Button>
      </div>
      <div class="flex items-center gap-1"><Button size="sm" variant="ghost" onclick={()=>source()} aria-label={study.locale==='zh'?'查看本问原题':'View original question'}><FileText data-icon="inline-start" aria-hidden="true"/>p.{part.sourcePage}</Button><Button size="sm" variant="link" onclick={()=>source(true)}>{study.locale==='zh'?'官方解答':'Official solution'}</Button></div>
    </div>
  </Accordion.Content>
</Accordion.Item>
