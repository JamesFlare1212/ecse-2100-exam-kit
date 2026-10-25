<script lang="ts">
  import * as Tooltip from '#lib/components/ui/tooltip';
  import { buttonVariants } from '#lib/components/ui/button';
  import GraduationCap from '@lucide/svelte/icons/graduation-cap';
  import RichText from './RichText.svelte';
  import type { Problem, Locale, SourceRef } from '#lib/types';
  let {problem,locale,onsource}: {problem:Problem;locale:Locale;onsource:(source:SourceRef)=>void}=$props();
</script>

<section class="problem-overview" aria-labelledby="overview-title" data-problem-guide>
  <h2 id="overview-title">{locale==='zh'?'先读懂这道题':'Before the derivation'}</h2>
  <p class="overview-concept"><RichText text={problem.guide.concept[locale]}/></p>
  <dl class="overview-details">
    <div><dt>{locale==='zh'?'已知':'Given'}</dt><dd><RichText text={problem.guide.known[locale]}/></dd></div>
    <div><dt>{locale==='zh'?'所求':'Find'}</dt><dd><RichText text={problem.guide.goal[locale]}/></dd></div>
    <div><dt>{locale==='zh'?'从哪里开始':'Start here'}</dt><dd><RichText text={problem.guide.approach[locale]}/></dd></div>
  </dl>
  <div class="overview-references">
    <span>{locale==='zh'?'讲义回顾':'In the lectures'}</span>
    <div class="flex flex-wrap gap-1">
      {#each problem.lectures as lecture(lecture.doc+'-'+lecture.page)}
        <Tooltip.Root>
          <Tooltip.Trigger class={buttonVariants({variant:'ghost',size:'sm'})} onclick={()=>onsource(lecture)} aria-label={'Lecture '+Number(lecture.doc.slice(-2))+' · p.'+lecture.page+' · '+lecture.label[locale]}>
            <GraduationCap data-icon="inline-start" aria-hidden="true"/>Lecture {Number(lecture.doc.slice(-2))} · p.{lecture.page}
          </Tooltip.Trigger>
          <Tooltip.Content>{lecture.label[locale]}</Tooltip.Content>
        </Tooltip.Root>
      {/each}
    </div>
  </div>
</section>
