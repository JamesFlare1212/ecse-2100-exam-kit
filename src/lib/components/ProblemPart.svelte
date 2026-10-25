<script lang="ts">
  import * as Accordion from '#lib/components/ui/accordion';
  import * as Alert from '#lib/components/ui/alert';
  import { Button } from '#lib/components/ui/button';
  import { Badge } from '#lib/components/ui/badge';
  import ArrowRight from '@lucide/svelte/icons/arrow-right';
  import Check from '@lucide/svelte/icons/check';
  import Info from '@lucide/svelte/icons/info';
  import FileText from '@lucide/svelte/icons/file-text';
  import Eye from '@lucide/svelte/icons/eye';
  import Math from './Math.svelte';
  import RichText from './RichText.svelte';
  import FormulaLink from './FormulaLink.svelte';
  import Figure from './Figure.svelte';
  import { formulaById } from '#lib/catalog';
  import { conclusionMath } from '#lib/answer-math';
  import type { Part, SourceRef, Exam } from '#lib/types';
  import type { StudyState } from '#lib/study.svelte';
  let {part,study,exam,dark,onsource}: {part:Part;study:StudyState;exam:Exam;dark:boolean;onsource:(s:SourceRef)=>void}=$props();
  const visible=$derived(study.revealed[`${part.id}`]??(study.mode==='practice'?0:1));
  const done=$derived(Boolean(study.completed[part.id]));
  const conclusion=$derived(conclusionMath(part.steps.at(-1)?.math,part.answer));
  let explorationOpen=$state(false);
  function show(n:number){study.revealed[part.id]=n;}
  function source(solution=false){onsource({doc:solution?exam.solutionDoc:exam.doc,page:solution?part.solutionPage:part.sourcePage,label:{zh:solution?'官方解答原页':'原始试题',en:solution?'Official solution page':'Original question'}});}
</script>
<Accordion.Item value={part.id} class="problem-part" data-part={part.id}>
  <Accordion.Trigger class="part-trigger" level={3}><span class:complete={done} class="part-letter">{#if done}<Check aria-label={study.locale==='zh'?'已掌握':'Mastered'}/>{:else}{part.label}{/if}</span><span class="part-prompt" lang={study.locale==='zh'?'zh-CN':'en'} data-original-prompt><RichText text={part.prompt[study.locale]}/></span>{#if part.points>0}<Badge variant="outline">{part.points} {study.locale==='zh'?'分':'pts'}</Badge>{/if}</Accordion.Trigger>
  {#if part.questionFigure}<div class="part-question-figure"><Figure name={part.questionFigure.name} locale={study.locale} {dark} caption={part.questionFigure.caption} original={part.questionFigure.source} {onsource}/></div>{/if}
  <Accordion.Content class="part-content">
    {#if visible>0}
      <div class="solution-steps">
        {#each part.steps.slice(0,visible) as step,i(i)}
          <div class="solution-step" data-answer={i===part.steps.length-1&&visible>part.steps.length?part.id:undefined}><span class="step-number">{String(i+1).padStart(2,'0')}</span><div class="step-content"><p><RichText text={step.text[study.locale]}/></p>{#if i===part.steps.length-1&&visible>part.steps.length}{#if conclusion.calculation}<Math tex={conclusion.calculation} display/>{/if}<Math tex={conclusion.result} display/>{#if part.answerText}<p><RichText text={part.answerText[study.locale]}/></p>{/if}{:else if step.math}<Math tex={step.math} display/>{/if}{#if step.refs.length}<div class="step-references">{#each step.refs as id(id)}<FormulaLink formula={formulaById[id]} locale={study.locale} {onsource} compact/>{/each}</div>{/if}</div></div>
        {/each}
      </div>
    {/if}
    {#if visible>part.steps.length}
      {#if part.figure}<Figure name={part.figure} locale={study.locale} {dark} caption={part.figureCaption}/>{/if}
      {#if part.spatialFigure}
        <div class="solution-exploration">
          <Button variant="outline" size="sm" aria-expanded={explorationOpen} onclick={()=>explorationOpen=!explorationOpen}><Eye data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?(explorationOpen?'收起 3D 工具':'查看 3D 空间结构'):(explorationOpen?'Hide 3D tool':'Explore the geometry in 3D')}</Button>
          {#if explorationOpen}<Figure name={part.spatialFigure} locale={study.locale} {dark} interactive/>{/if}
        </div>
      {/if}
      {#if part.note}<Alert.Root class="solution-note"><Info aria-hidden="true"/><Alert.Title>{study.locale==='zh'?'核对说明':'Source check'}</Alert.Title><Alert.Description><RichText text={part.note[study.locale]}/></Alert.Description></Alert.Root>{/if}
    {/if}
    <div class="part-actions">
      <div class="flex flex-wrap items-center gap-2">
        {#if visible<=part.steps.length}
          <Button size="sm" onclick={()=>show(visible+1)}>{#if visible===0}<Eye data-icon="inline-start" aria-hidden="true"/>{/if}{study.locale==='zh'?(visible===0?'开始分步推导':visible<part.steps.length?'下一步':'查看最终答案'):(visible===0?'Begin solution':visible<part.steps.length?'Next step':'Reveal final answer')}<ArrowRight data-icon="inline-end" aria-hidden="true"/></Button>
          <Button size="sm" variant="ghost" onclick={()=>show(part.steps.length+1)}>{study.locale==='zh'?'展开本问解答':'Reveal this solution'}</Button>
        {:else}<Button variant={done?'secondary':'outline'} size="sm" onclick={()=>study.completed[part.id]=!done}><Check data-icon="inline-start" aria-hidden="true"/>{study.locale==='zh'?(done?'已掌握 · 撤销':'标记已掌握'):(done?'Mastered · undo':'Mark as mastered')}</Button>{/if}
      </div>
      <div class="flex items-center gap-1"><Button size="sm" variant="ghost" onclick={()=>source()} aria-label={study.locale==='zh'?'查看本问原题':'View original question'}><FileText data-icon="inline-start" aria-hidden="true"/>p.{part.sourcePage}</Button><Button size="sm" variant="link" onclick={()=>source(true)}>{study.locale==='zh'?'官方解答':'Official solution'}</Button></div>
    </div>
  </Accordion.Content>
</Accordion.Item>
