<script lang="ts">
  import {onMount,tick,untrack} from 'svelte';
  import {navigate} from 'astro:transitions/client';
  import {BitsConfig} from 'bits-ui';
  import * as Tabs from '#lib/components/ui/tabs';
  import * as Accordion from '#lib/components/ui/accordion';
  import * as Sheet from '#lib/components/ui/sheet';
  import * as Tooltip from '#lib/components/ui/tooltip';
  import * as Alert from '#lib/components/ui/alert';
  import {Button,buttonVariants} from '#lib/components/ui/button';
  import {Badge} from '#lib/components/ui/badge';
  import {Separator} from '#lib/components/ui/separator';
  import FileText from '@lucide/svelte/icons/file-text';
  import Moon from '@lucide/svelte/icons/moon';
  import Sun from '@lucide/svelte/icons/sun';
  import SearchIcon from '@lucide/svelte/icons/search';
  import Bookmark from '@lucide/svelte/icons/bookmark';
  import BookmarkCheck from '@lucide/svelte/icons/bookmark-check';
  import ArrowUpRight from '@lucide/svelte/icons/arrow-up-right';
  import ChevronRight from '@lucide/svelte/icons/chevron-right';
  import CircleCheck from '@lucide/svelte/icons/circle-check';
  import PanelRight from '@lucide/svelte/icons/panel-right';
  import PanelLeft from '@lucide/svelte/icons/panel-left';
  import GraduationCap from '@lucide/svelte/icons/graduation-cap';
  import Layers from '@lucide/svelte/icons/layers';
  import ChevronsUp from '@lucide/svelte/icons/chevrons-up';
  import Info from '@lucide/svelte/icons/info';
  import Navigation from '#lib/components/Navigation.svelte';
  import ReferenceRail from '#lib/components/ReferenceRail.svelte';
  import SourceViewer from '#lib/components/SourceViewer.svelte';
  import Search from '#lib/components/Search.svelte';
  import Library from '#lib/components/Library.svelte';
  import Figure from '#lib/components/Figure.svelte';
  import RichText from '#lib/components/RichText.svelte';
  import ProblemPart from '#lib/components/ProblemPart.svelte';
  import ProblemOverview from '#lib/components/ProblemOverview.svelte';
  import {StudyState} from '#lib/study.svelte';
  import {provideFormulaPreviews} from '#lib/formula-preview.svelte';
  import {createCatalog} from '#lib/catalog';
  import {problemPath} from '#lib/problem-navigation';
  import type {SourceRef,StudyPageData} from '#lib/types';

  let {data}:{data:StudyPageData}=$props();
  const formulaPreviews=provideFormulaPreviews();
  const catalog=$derived(createCatalog(data.examIndex,data.documents));
  const assetBase=$derived(data.assetBase);
  const documents=$derived(catalog.documents);
  const study=untrack(()=>new StudyState(()=>catalog,data.problem.id));
  let systemDark=$state(false);
  const dark=$derived(study.theme==='dark'||(study.theme==='system'&&systemDark));
  const problem=$derived(data.problem);
  const exam=$derived(data.exam);
  const completed=$derived(study.count(problem.parts.map(p=>p.id)));
  const originalPages=$derived([...new Set(problem.parts.map(p=>p.sourcePage))]);
  let view=$state('learn');
  let openParts=$state<string[]>([]);
  let source=$state<SourceRef|null>(null);
  let searchOpen=$state(false);
  let navOpen=$state(false);
  let railOpen=$state(false);
  let compactNavigation=$state(false);
  let compactReferences=$state(false);
  let libraryOpen=$state(false);
  let libraryKind=$state('crib');
  const t=(zh:string,en:string)=>study.locale==='zh'?zh:en;
  const navigationLabel=$derived(compactNavigation?t('打开试卷导航','Open exam navigation'):t(study.navigationOpen?'收起试卷导航':'展开试卷导航',study.navigationOpen?'Collapse exam navigation':'Expand exam navigation'));
  const referencesLabel=$derived(compactReferences?t('打开公式与课件','Open formulas and lectures'):t(study.referencesOpen?'收起公式与课件侧栏':'展开公式与课件侧栏',study.referencesOpen?'Collapse reference sidebar':'Expand reference sidebar'));

  $effect(()=>{study.selected=problem.id;openParts=[];view='learn';formulaPreviews.active=null;});
  $effect(()=>{const serialized=study.serialize();if(study.ready)study.persist(serialized);});
  $effect(()=>{if(study.ready){document.documentElement.classList.toggle('dark',dark);document.documentElement.lang=study.locale==='zh'?'zh-CN':'en';document.documentElement.style.colorScheme=dark?'dark':'light';document.documentElement.dataset.navigation=study.navigationOpen?'open':'closed';document.documentElement.dataset.references=study.referencesOpen?'open':'closed';}});
  $effect(()=>{
    if(!study.ready)return;
    document.title=`${problem.title[study.locale]} · Fieldnotes · ECSE 2100`;
    document.querySelector('meta[name="description"]')?.setAttribute('content',t(`ECSE 2100 场与波 I：${catalog.exams.length} 份历年试卷、${catalog.totalParts} 个双语详解小问，以及附来源的公式与课程讲义。`,`ECSE 2100 Fields and Waves I: ${catalog.exams.length} back exams, ${catalog.totalParts} bilingual worked subparts, source-linked formulas and lecture notes.`));
    void tick().then(()=>delete document.documentElement.dataset.localePending);
  });

  function library(kind:string){libraryKind=kind;libraryOpen=true;navOpen=false;}
  function openSource(ref:SourceRef){source=ref;railOpen=false;}
  async function select(id:string,part?:string){
    if(!catalog.problemIds.has(id))return;
    navOpen=false;view='learn';
    await navigate(problemPath(id));await tick();
    if(part){openParts=[part];await tick();document.querySelector(`[data-part="${part}"]`)?.scrollIntoView({block:'start',behavior:'instant'});}
    else{window.scrollTo({top:0,behavior:'instant'});document.getElementById('problem-title')?.focus({preventScroll:true});}
  }
  function toggleSolutions(){
    if(openParts.length){openParts=[];return;}
    openParts=problem.parts.map(p=>p.id);
  }
  function focusOutsidePanel(id:string,toggle:string){
    if(document.getElementById(id)?.contains(document.activeElement))
      document.querySelector<HTMLElement>('[data-sidebar-toggle="'+toggle+'"]')?.focus({preventScroll:true});
  }
  function toggleNavigation(){
    if(compactNavigation)navOpen=!navOpen;
    else{if(study.navigationOpen)focusOutsidePanel('exam-navigation','navigation');study.navigationOpen=!study.navigationOpen;}
  }
  function toggleReferences(){
    if(compactReferences)railOpen=!railOpen;
    else{if(study.referencesOpen)focusOutsidePanel('reference-sidebar','references');study.referencesOpen=!study.referencesOpen;}
  }
  onMount(()=>{
    const preference=matchMedia('(prefers-color-scheme: dark)');systemDark=preference.matches;
    const onAppearance=(event:MediaQueryListEvent)=>systemDark=event.matches;preference.addEventListener('change',onAppearance);
    const navLayout=matchMedia('(max-width: 800px)'),refLayout=matchMedia('(max-width: 1180px)');
    compactNavigation=navLayout.matches;compactReferences=refLayout.matches;
    const onNavLayout=(event:MediaQueryListEvent)=>{if(event.matches)focusOutsidePanel('exam-navigation','navigation');compactNavigation=event.matches;if(!event.matches)navOpen=false;};
    const onRefLayout=(event:MediaQueryListEvent)=>{if(event.matches)focusOutsidePanel('reference-sidebar','references');compactReferences=event.matches;if(!event.matches)railOpen=false;};
    navLayout.addEventListener('change',onNavLayout);refLayout.addEventListener('change',onRefLayout);
    study.restore();study.selected=problem.id;study.ready=true;
    const keydown=(event:KeyboardEvent)=>{
      if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){event.preventDefault();searchOpen=!searchOpen;}
      else if((event.metaKey||event.ctrlKey)&&!event.altKey&&!event.shiftKey&&event.key.toLowerCase()==='b'){event.preventDefault();toggleNavigation();}
    };
    window.addEventListener('keydown',keydown);
    return()=>{preference.removeEventListener('change',onAppearance);navLayout.removeEventListener('change',onNavLayout);refLayout.removeEventListener('change',onRefLayout);window.removeEventListener('keydown',keydown);};
  });
</script>

<a class="skip-link" href="#main-content">{t('跳至题目','Skip to problem')}</a>
<BitsConfig defaultPortalTo="#fieldnotes-overlays">
<Tooltip.Provider delayDuration={250}>
  <div class="app-shell" data-navigation={study.navigationOpen?'open':'closed'}>
    <aside id="exam-navigation" class="desktop-navigation" aria-label={t('试卷导航','Exam navigation')} aria-hidden={compactNavigation||!study.navigationOpen} inert={compactNavigation||!study.navigationOpen}><Navigation {study} onselect={select} onlibrary={library}/></aside>
    <div class="workspace">
      <header class="topbar">
        <div class="toolbar-breadcrumb">
          <Tooltip.Root><Tooltip.Trigger class={buttonVariants({variant:'ghost',size:'icon',highlightExpanded:false})} data-sidebar-toggle="navigation" onclick={toggleNavigation} aria-label={navigationLabel} aria-controls={compactNavigation?'mobile-exam-navigation':'exam-navigation'} aria-expanded={compactNavigation?navOpen:study.navigationOpen} aria-keyshortcuts="Control+b Meta+b"><PanelLeft aria-hidden="true"/></Tooltip.Trigger><Tooltip.Content>{navigationLabel}{#if !compactNavigation} · Ctrl / ⌘ B{/if}</Tooltip.Content></Tooltip.Root>
          <Separator orientation="vertical" class="h-5 data-vertical:self-center"/>
          <span class="course-label">ECSE 2100</span><ChevronRight aria-hidden="true"/><span>{t('习题室','Study room')}</span>
        </div>
        <div class="toolbar-actions">
          <Button variant="ghost" class="search-button" onclick={()=>searchOpen=true} aria-label={t('搜索题目与公式','Search problems and formulas')}><SearchIcon data-icon="inline-start" aria-hidden="true"/><span class="search-button-label">{t('搜索','Search')}</span><kbd>⌘ K</kbd></Button>
          <Separator orientation="vertical" class="h-5 data-vertical:self-center"/>
          <Tooltip.Root><Tooltip.Trigger class={buttonVariants({variant:'ghost',size:'sm'})} onclick={()=>study.locale=study.locale==='zh'?'en':'zh'} aria-label={t('Switch to English','切换为中文')}><span class="language-switch">{study.locale==='zh'?'EN':'中文'}</span></Tooltip.Trigger><Tooltip.Content>{t('切换为英文','Switch to Chinese')}</Tooltip.Content></Tooltip.Root>
          <Tooltip.Root><Tooltip.Trigger class={buttonVariants({variant:'ghost',size:'icon'})} onclick={()=>study.theme=dark?'light':'dark'} aria-label={t(dark?'切换浅色主题':'切换深色主题',dark?'Switch to light mode':'Switch to dark mode')}>{#if dark}<Sun aria-hidden="true"/>{:else}<Moon aria-hidden="true"/>{/if}</Tooltip.Trigger><Tooltip.Content>{t(dark?'浅色主题':'深色主题',dark?'Light mode':'Dark mode')}</Tooltip.Content></Tooltip.Root>
          <Tooltip.Root><Tooltip.Trigger class={buttonVariants({variant:'ghost',size:'icon',highlightExpanded:false})} data-sidebar-toggle="references" onclick={toggleReferences} aria-label={referencesLabel} aria-controls={compactReferences?'mobile-reference-sidebar':'reference-sidebar'} aria-expanded={compactReferences?railOpen:study.referencesOpen}><PanelRight aria-hidden="true"/></Tooltip.Trigger><Tooltip.Content>{referencesLabel}</Tooltip.Content></Tooltip.Root>
        </div>
      </header>
      <div class="reading-layout" data-references={study.referencesOpen?'open':'closed'}>
        <main id="main-content" class="main-content" data-problem={problem.id} data-study-ready={study.ready}>
          <div class="course-eyebrow"><span class="eyebrow-line"></span>FIELDS & WAVES I <span class="eyebrow-divider">/</span> {t('学习桌','THE STUDY DESK')}</div>
          <div class="problem-meta"><Badge variant="outline">Exam {exam.number}</Badge><span>{exam.term[study.locale]} {exam.year}</span><span class="metadata-dot">·</span><span>{problem.points} {t('分','points')}</span><span class="metadata-dot">·</span><span>{problem.parts.length} {t('小问','parts')}</span></div>
          <div class="problem-title-row"><div><p class="problem-kicker">{t('题目','PROBLEM')} {String(problem.number).padStart(2,'0')}</p><h1 id="problem-title" lang={study.locale==='zh'?'zh-CN':'en'} tabindex="-1">{problem.title[study.locale]}</h1></div><Tooltip.Root><Tooltip.Trigger class={buttonVariants({variant:'outline',size:'icon'})} onclick={()=>study.bookmarks[problem.id]=!study.bookmarks[problem.id]} aria-label={t(study.bookmarks[problem.id]?'取消收藏':'收藏此题',study.bookmarks[problem.id]?'Remove bookmark':'Bookmark problem')} aria-pressed={Boolean(study.bookmarks[problem.id])}>{#if study.bookmarks[problem.id]}<BookmarkCheck aria-hidden="true"/>{:else}<Bookmark aria-hidden="true"/>{/if}</Tooltip.Trigger><Tooltip.Content>{t(study.bookmarks[problem.id]?'已收藏':'留待再次练习',study.bookmarks[problem.id]?'Saved':'Save for another attempt')}</Tooltip.Content></Tooltip.Root></div>
          <p class="problem-subtitle">{problem.topic[study.locale]}<span>·</span>{t('先写方程，再代入数值。','Start with the equation. Then work through the numbers.')}</p>
          <div class="problem-lectures lecture-badges"><GraduationCap aria-hidden="true"/>{#each [...new Set(problem.lectures.map(l=>Number(l.doc.slice(-2))))] as number(number)}<Button variant="ghost" size="sm" onclick={()=>openSource(problem.lectures.find(l=>Number(l.doc.slice(-2))===number)!)}>Lecture {String(number).padStart(2,'0')}</Button>{/each}</div>
          {#if study.storageError}<Alert.Root><Info aria-hidden="true"/><Alert.Title>{t('浏览器存储暂不可用','Browser storage is unavailable')}</Alert.Title><Alert.Description>{t('本次仍可练习，但学习进度和收藏可能无法保存。','You can keep working, but progress and bookmarks may not be saved.')}</Alert.Description></Alert.Root>{/if}
          <Tabs.Root bind:value={view} class="problem-tabs">
            <Tabs.List variant="line" class="problem-tab-list"><Tabs.Trigger value="learn"><Layers aria-hidden="true"/>{t('题目与推导','Problem & solution')}</Tabs.Trigger><Tabs.Trigger value="source"><FileText aria-hidden="true"/>{t('试卷原页','Source pages')}</Tabs.Trigger></Tabs.List>
            <Tabs.Content value="learn">
              <section class="problem-statement" aria-label={t('题目条件','Problem statement')}><div class="section-label"><span>01</span>{t('试卷原题','THE ORIGINAL QUESTION')}<Badge variant="secondary">{t('原题措辞','Original wording')}</Badge></div><div class="original-statement" lang={study.locale==='zh'?'zh-CN':'en'} data-original-statement><RichText text={problem.statement[study.locale]}/></div></section>
              {#if !problem.figureAtParts}<Figure {assetBase} name={problem.figure} locale={study.locale} {dark} caption={problem.figureCaption} original={problem.originalFigure} onsource={openSource}/>{/if}
              <section class="worked-solution" aria-label={t('分步解答','Worked solution')}><div class="solution-section-heading"><div class="section-label"><span>02</span>{t('一步一步推导','WORK IT THROUGH')}</div><Button variant="ghost" size="sm" onclick={toggleSolutions} aria-controls="worked-parts" aria-expanded={openParts.length>0}>{#if openParts.length}{t('收起全部推导','Collapse all steps')}<ChevronsUp data-icon="inline-end" aria-hidden="true"/>{:else}{t('展开全部推导','Reveal all steps')}<Layers data-icon="inline-end" aria-hidden="true"/>{/if}</Button></div>
                <ProblemOverview {problem} locale={study.locale} onsource={openSource}/>
                <Accordion.Root id="worked-parts" type="multiple" bind:value={openParts}>{#each problem.parts as part(part.id)}<ProblemPart {assetBase} {part} {study} {exam} {dark} onsource={openSource}/>{/each}</Accordion.Root>
              </section>
              {#if problem.note}<Alert.Root class="problem-model-note"><Info aria-hidden="true"/><Alert.Title>{t('模型与原题说明','Model & source note')}</Alert.Title><Alert.Description><RichText text={problem.note[study.locale]}/></Alert.Description></Alert.Root>{/if}
              <div class="problem-completion"><div><CircleCheck aria-hidden="true"/><span>{completed}/{problem.parts.length} {t('小问已掌握','parts mastered')}</span></div><span>{t('掌握后自行标记，进度自动保存。','Mark your understanding; progress saves automatically.')}</span></div>
            </Tabs.Content>
            <Tabs.Content value="source"><div class="source-tab-heading"><p>{t('保留原始试卷版式、插图与题号。点击页面可放大查看。','Original layout, figures and numbering. Open any page to inspect it.')}</p>{#if !exam.questionsOnly}<Alert.Root><Info aria-hidden="true"/><Alert.Description>{t('本地仅有含官方答案版本，原页会显示答案。练习可使用“题目与推导”中的网页原生题目。','Only a combined questions/solutions PDF is available. Source pages show answers; use the native problem view for practice.')}</Alert.Description></Alert.Root>{/if}</div>
              {#each originalPages as page(page)}<div class="original-page-card"><div><strong>PDF · {t('第','Page')} {page} {t('页','')}</strong><Button variant="outline" size="sm" onclick={()=>openSource({doc:exam.doc,page,label:{zh:'原始试题',en:'Original exam'}})}>{t('放大查看','Inspect page')}<ArrowUpRight data-icon="inline-end" aria-hidden="true"/></Button></div><img src={`${documents[exam.doc].pageBase}/${page}.webp`} alt={t(`Exam ${exam.number} · ${exam.term.zh} ${exam.year} · 第 ${page} 页`,`Exam ${exam.number}, ${exam.term.en} ${exam.year}, page ${page}`)} loading="lazy"/></div>{/each}
            </Tabs.Content>
          </Tabs.Root>
          <footer class="reading-footer"><span>fieldnotes<span class="brand-dot">.</span></span><p>{t('把答案连回原理。','Connect the answer to the idea.')}<small>ECSE 2100 · {catalog.totalParts} {t('小问','worked parts')}</small></p></footer>
        </main>
        <aside id="reference-sidebar" class="reference-rail" aria-label={t('公式与课件引用','Formula and lecture references')} aria-hidden={compactReferences||!study.referencesOpen} inert={compactReferences||!study.referencesOpen}><ReferenceRail {documents} {problem} locale={study.locale} onsource={openSource} onlibrary={library}/></aside>
      </div>
    </div>
  </div>
  <Sheet.Root bind:open={navOpen}><Sheet.Content id="mobile-exam-navigation" closeLabel={t('关闭','Close')} side="left" class="mobile-nav-sheet"><Sheet.Header class="sr-only"><Sheet.Title>{t('试卷与资料导航','Exams and resources')}</Sheet.Title><Sheet.Description>{t('选择试卷、题目或学习资料。','Choose an exam, problem or course resource.')}</Sheet.Description></Sheet.Header><Navigation {study} onselect={select} onlibrary={library}/></Sheet.Content></Sheet.Root>
  <Sheet.Root bind:open={railOpen}><Sheet.Content id="mobile-reference-sidebar" closeLabel={t('关闭','Close')} side="right" class="reference-sheet"><Sheet.Header><Sheet.Title>{t('公式与课程连接','Formulas and lectures')}</Sheet.Title><Sheet.Description>{t('查看本题使用的公式与对应讲义。','The equations and lecture pages used in this problem.')}</Sheet.Description></Sheet.Header><ReferenceRail {documents} {problem} locale={study.locale} onsource={openSource} onlibrary={(kind)=>{railOpen=false;library(kind);}}/></Sheet.Content></Sheet.Root>
  <Search bind:open={searchOpen} {catalog} locale={study.locale} onselect={select} onsource={openSource}/>
  <Library bind:open={libraryOpen} bind:kind={libraryKind} {study} onsource={openSource} onselect={select}/>
  <SourceViewer {source} {documents} locale={study.locale} onclose={()=>source=null}/>
</Tooltip.Provider>
</BitsConfig>
