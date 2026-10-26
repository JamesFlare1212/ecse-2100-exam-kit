// Optional end-to-end QA. Install Playwright separately, or point PLAYWRIGHT_MODULE
// at an isolated install. Run against `bun run preview --host 127.0.0.1`.
import assert from 'node:assert/strict';
import {mkdir,readFile,readdir,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import {checkI18n} from './browser-i18n-qa.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE??'playwright');
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const destination=process.env.QA_ARTIFACTS??resolve(root,'artifacts');
const base=process.env.QA_URL??'http://localhost:4173';
const examDirectory=resolve(root,'content');
const exams=await Promise.all((await readdir(examDirectory)).filter(name=>/^exam[1-9]\d*_[fs]\d{2}$/.test(name)).sort().map(async name=>JSON.parse(await readFile(resolve(examDirectory,name,'paper.json'),'utf8'))));
await mkdir(destination,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'light',reducedMotion:'reduce'});
const page=await context.newPage();
page.setDefaultTimeout(12000);
const errors=[],failures=[],checks=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('requestfailed',r=>failures.push({url:r.url(),error:r.failure()?.errorText}));
const record=(name,data={})=>{checks.push({name,...data});console.log('PASS',name);};
const stored=()=>page.evaluate(()=>JSON.parse(localStorage.getItem('ecse2100-fieldnotes-v1')));
async function selected(id){await page.waitForFunction(id=>document.querySelector('[data-study-ready="true"]')?.getAttribute('data-problem')===id&&JSON.parse(localStorage.getItem('ecse2100-fieldnotes-v1')??'{}').selected===id,id);}
async function goto(id){await page.goto(`${base}/problems/${id}/`,{waitUntil:'domcontentloaded',timeout:45000});await selected(id);}
async function noOverflow(){const metrics=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth}));assert.ok(metrics.documentWidth<=metrics.width+1,JSON.stringify(metrics));}
async function revealAll(){
  const button=page.locator('.solution-section-heading button');
  assert.equal(await button.count(),1);
  if(await button.getAttribute('aria-expanded')==='true'){
    await button.click();
    await page.waitForFunction(()=>[...document.querySelectorAll('#worked-parts [data-slot="accordion-content"]')].every(e=>e.hidden||getComputedStyle(e).display==='none'));
  }
  await button.click();
}
try {
  await checkI18n(browser,base,record);
  const staticContext=await browser.newContext({javaScriptEnabled:false,viewport:{width:1440,height:1000}});
  try {
    const staticPage=await staticContext.newPage();
    await staticPage.goto(base+'/');
    await staticPage.waitForURL('**/problems/e2-s26-q3/');
    const exam=exams.find(e=>e.id==='e1-f25'),question=exam.problems[1],next=exam.problems[2];
    await staticPage.goto(`${base}/problems/${question.id}/`);
    assert.equal(await staticPage.locator('#problem-title').innerText(),question.title.zh);
    assert.equal(await staticPage.locator('[data-original-prompt]').count(),question.parts.length);
    assert.equal(await staticPage.locator('main').getAttribute('data-study-ready'),'false');
    await staticPage.locator(`a.question-link[href="/problems/${next.id}/"]`).click();
    await staticPage.waitForURL(`**/problems/${next.id}/`);
    assert.equal(await staticPage.locator('#problem-title').innerText(),next.title.zh);
    await staticPage.setViewportSize({width:375,height:812});
    assert.ok(await staticPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    record('Static root redirect, deep links and sidebar links work without JavaScript; phone question text remains readable');
  } finally {await staticContext.close();}

  await goto('e2-s26-q3');
  await page.evaluate(()=>window.__fieldnotesDocument='same-page');
  await page.locator('a.question-link[href="/problems/e2-s26-q4/"]').click();
  await selected('e2-s26-q4');
  assert.ok(page.url().endsWith('/problems/e2-s26-q4/'));
  assert.equal(await page.evaluate(()=>window.__fieldnotesDocument),'same-page');
  await page.goBack();await selected('e2-s26-q3');
  await page.goForward();await selected('e2-s26-q4');
  await page.evaluate(()=>{
    const data=JSON.parse(localStorage.getItem('ecse2100-fieldnotes-v1'));
    data.selected='e1-f25-q1';
    data.completed['e9-f99-q1-a']=true;data.bookmarks['e9-f99-q1']=true;
    data.revealed['e9-f99-q1-a']=2;data.notes={'e9-f99-q1':'Preserved legacy record'};
    localStorage.setItem('ecse2100-fieldnotes-v1',JSON.stringify(data));
  });
  await page.reload();await selected('e2-s26-q4');
  assert.ok(page.url().endsWith('/problems/e2-s26-q4/'));
  assert.equal((await stored()).completed['e9-f99-q1-a'],true);
  assert.equal((await stored()).bookmarks['e9-f99-q1'],true);
  assert.equal((await stored()).revealed['e9-f99-q1-a'],2);
  assert.equal((await stored()).notes['e9-f99-q1'],'Preserved legacy record');
  assert.ok((await page.locator('.progress-summary strong').innerText()).replace(/\s+/g,'').startsWith('0/'));
  record('Unplugged paper records survive without affecting active progress');
  record('Problem links use client navigation and browser history; a direct path overrides the saved selection');
  await goto('e2-s26-q3');
  await page.evaluate(()=>document.fonts.ready);
  assert.ok(await page.evaluate(()=>[...document.fonts].some(f=>f.family.includes('Noto')&&f.status==='loaded')));
  record('Self-hosted Chinese glyphs loaded');
  const navigationToggle=page.locator('[data-sidebar-toggle="navigation"]');
  const referencesToggle=page.locator('[data-sidebar-toggle="references"]');
  async function sidebars(navigation,references){
    if((await navigationToggle.getAttribute('aria-expanded')==='true')!==navigation)await navigationToggle.click();
    if((await referencesToggle.getAttribute('aria-expanded')==='true')!==references)await referencesToggle.click();
    await page.waitForFunction(({navigation,references})=>{
      const nav=document.getElementById('exam-navigation'),ref=document.getElementById('reference-sidebar');
      return (navigation?nav.getBoundingClientRect().width>180:nav.getBoundingClientRect().width===0)&&
        (references?ref.getBoundingClientRect().width>200:ref.getBoundingClientRect().width===0);
    },{navigation,references});
  }
  const readingWidth=await page.locator('#main-content').evaluate(e=>e.getBoundingClientRect().width);
  await page.locator('#reference-sidebar').getByRole('tab',{name:'Lecture notes',exact:true}).click();
  for(const [navigation,references] of [[false,true],[true,false],[false,false],[true,true]]){
    await sidebars(navigation,references);await noOverflow();
    assert.equal(await page.locator('#exam-navigation').evaluate(e=>e.inert),!navigation);
    assert.equal(await page.locator('#reference-sidebar').evaluate(e=>e.inert),!references);
    assert.equal((await stored()).selected,'e2-s26-q3');
    if(!navigation||!references)assert.ok(await page.locator('#main-content').evaluate(e=>e.getBoundingClientRect().width)>=readingWidth);
  }
  assert.equal(await page.locator('#reference-sidebar').getByRole('tab',{name:'Lecture notes',exact:true}).getAttribute('aria-selected'),'true');
  await page.locator('#reference-sidebar').getByRole('tab',{name:'公式表',exact:true}).click();
  record('Both sidebars collapse independently, release reading width and preserve the selected reference tab');
  await sidebars(false,false);
  await page.reload({waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.documentElement.dataset.navigation==='closed'&&document.documentElement.dataset.references==='closed');
  assert.equal(await navigationToggle.getAttribute('aria-expanded'),'false');
  assert.equal(await referencesToggle.getAttribute('aria-expanded'),'false');
  assert.deepEqual((await stored()).sidebars,{navigation:false,references:false});
  record('Sidebar preferences persist after reload and are restored before the reading layout opens');
  await navigationToggle.focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.getElementById('exam-navigation').getBoundingClientRect().width>180);
  await page.locator('#exam-navigation [aria-current="page"]').focus();
  await page.keyboard.press('Control+b');
  assert.equal(await navigationToggle.getAttribute('aria-expanded'),'false');
  assert.ok(await navigationToggle.evaluate(e=>document.activeElement===e));
  await referencesToggle.focus();await page.keyboard.press('Enter');
  assert.equal(await referencesToggle.getAttribute('aria-expanded'),'true');
  await page.keyboard.press('Space');
  assert.equal(await referencesToggle.getAttribute('aria-expanded'),'false');
  record('Native sidebar buttons support keyboard activation and move focus out of collapsed content');
  await page.setViewportSize({width:375,height:812});
  await page.getByRole('button',{name:'打开试卷导航',exact:true}).click();
  await page.locator('#mobile-exam-navigation').waitFor({state:'visible'});
  await page.keyboard.press('Escape');await page.locator('#mobile-exam-navigation').waitFor({state:'detached'});
  await page.getByRole('button',{name:'打开公式与课件',exact:true}).click();
  await page.locator('#mobile-reference-sidebar').waitFor({state:'visible'});
  await page.keyboard.press('Escape');await page.locator('#mobile-reference-sidebar').waitFor({state:'detached'});
  await noOverflow();await page.setViewportSize({width:1440,height:1000});
  assert.deepEqual((await stored()).sidebars,{navigation:false,references:false});
  await sidebars(true,true);
  record('Phone drawers remain available with both desktop sidebars collapsed');
  // Inspect every question and every answer in the rendered application.
  let partCount=0,stepCount=0;
  for(const exam of exams)for(const q of exam.problems){
    await goto(q.id);await revealAll();
    assert.equal(await page.locator('#problem-title').innerText(),q.title.zh);
    assert.equal(await page.locator('[data-problem-guide]').count(),1);
    assert.equal(await page.locator('.overview-concept').innerText(),q.guide.concept.zh);
    assert.equal(await page.locator('.overview-references button').count(),q.lectures.length);
    assert.ok(await page.locator('[data-problem-guide]').evaluate(e=>Boolean(e.compareDocumentPosition(document.querySelector('#worked-parts'))&Node.DOCUMENT_POSITION_FOLLOWING)));
    assert.equal(await page.locator('[data-original-statement][lang="zh-CN"]').count(),1);
    assert.equal(await page.locator('[data-original-prompt][lang="zh-CN"]').count(),q.parts.length);
    await page.getByRole('button',{name:'Switch to English',exact:true}).click();
    assert.equal(await page.locator('#problem-title').innerText(),q.title.en);
    assert.equal(await page.locator('.overview-concept').innerText(),q.guide.concept.en);
    assert.equal(await page.locator('[data-original-statement][lang="en"]').count(),1);
    assert.equal(await page.locator('[data-original-prompt][lang="en"]').count(),q.parts.length);
    await page.getByRole('button',{name:'切换为中文',exact:true}).click();
    assert.equal(await page.locator('#problem-title').innerText(),q.title.zh);
    assert.equal(await page.locator('[data-part]').count(),q.parts.length);
    assert.equal(await page.locator('[data-answer]').count(),q.parts.length);
    assert.equal(await page.locator('.final-answer,.answer-heading,.problem-pagination').count(),0);
    assert.equal(await page.locator('.solution-step[data-answer]').count(),q.parts.length);
    const renderedSteps=await page.locator('[data-part]').evaluateAll(nodes=>nodes.map(node=>({
      id:node.dataset.part,
      count:node.querySelectorAll('.solution-step').length,
      firstEquation:node.querySelector('.solution-step .math-display annotation')?.textContent
    })));
    for(const part of q.parts){
      const actual=renderedSteps.find(item=>item.id===part.id);
      assert.equal(actual.count,part.steps.length,part.id);
      assert.equal(actual.firstEquation,part.steps[0].math,part.id);
      stepCount+=actual.count;
    }
    for(const result of await page.locator('[data-answer]').evaluateAll(nodes=>nodes.map(node=>({box:Boolean(node.querySelector('.fbox')),background:getComputedStyle(node).backgroundColor,border:getComputedStyle(node).borderTopWidth})))) {
      assert.equal(result.box,true);assert.equal(result.background,'rgba(0, 0, 0, 0)');assert.equal(result.border,'0px');
    }
    assert.equal(await page.locator('.katex-error').count(),0);
    await page.locator('.figure-image img').evaluateAll(imgs=>Promise.all(imgs.map(img=>img.decode())));
    await noOverflow();partCount+=q.parts.length;
    await page.setViewportSize({width:375,height:812});
    await noOverflow();
    assert.equal(await page.locator('.solution-step').count(),q.parts.reduce((total,part)=>total+part.steps.length,0));
    await page.setViewportSize({width:1440,height:1000});
    await page.getByRole('button',{name:'收起全部推导',exact:true}).click();
    await page.waitForFunction(()=>[...document.querySelectorAll('#worked-parts [data-slot="accordion-content"]')].every(e=>e.hidden||getComputedStyle(e).display==='none'));
    assert.equal(await page.locator('.part-trigger[aria-expanded="true"]').count(),0);
    assert.equal(await page.locator('[data-original-prompt]').count(),q.parts.length);
    assert.equal(await page.locator('[data-answer]:visible').count(),0);
  }
  record('All 20 problems and 93 worked parts render',{parts:partCount});
  record('Every subpart displays its opening equation and all intermediate steps',{steps:stepCount});
  record('All detailed solutions fit the 375px phone reading layout',{parts:partCount,steps:stepCount});
  record('All 20 bilingual introductions precede the derivation and link to lecture pages');
  record('One global toggle tracks open parts across all 20 original problems');
  await goto('e2-f25-q1');
  await revealAll();
  const questionSphere=page.locator('.study-figure[data-figure="e2-f25-q1"]');
  assert.equal(await questionSphere.locator('canvas').count(),0);
  assert.ok((await questionSphere.locator('img').getAttribute('src')).endsWith('.svg'));
  assert.equal(await page.locator('.solution-exploration,.spatial-figure,.sphere-view').count(),0);
  const sphereHeight=await questionSphere.locator('.figure-canvas').evaluate(e=>e.getBoundingClientRect().height);
  await questionSphere.getByRole('radio',{name:'原始插图',exact:true}).click();
  await questionSphere.locator('.figure-canvas img').evaluate(img=>img.decode());
  await questionSphere.getByRole('radio',{name:'矢量复刻',exact:true}).click();
  await questionSphere.locator('.figure-canvas img').evaluate(img=>img.decode());
  assert.equal(await questionSphere.locator('.figure-canvas').evaluate(e=>e.getBoundingClientRect().height),sphereHeight);
  record('Spherical question and solutions use static SVGs with no interactive 3D tool');
  await goto('e2-s26-q3');
  const chineseText=await page.locator('[data-original-statement]').innerText();
  assert.ok(chineseText.startsWith('右侧同轴电缆的电介质质量较差'));
  assert.equal(await page.locator('.translation-toggle,.statement-translation').count(),0);
  assert.equal(await page.getByRole('switch',{name:'显示中文翻译',exact:true}).count(),0);
  await page.getByRole('button',{name:'Switch to English',exact:true}).click();
  assert.ok((await page.locator('[data-original-statement]').innerText()).startsWith('The coaxial cable to the right has a poor dielectric'));
  await page.getByRole('button',{name:'切换为中文',exact:true}).click();
  assert.equal(await page.locator('[data-original-statement]').innerText(),chineseText);
  record('Global language directly switches original wording and its faithful Chinese translation');
  await revealAll();
  const ref=page.locator('a.formula-link[aria-label*="高斯定律"]').first();
  await ref.hover();await page.locator('[data-slot="hover-card-content"]').waitFor({state:'visible'});
  await page.locator('[data-slot="hover-card-content"] img').evaluate(img=>img.decode());
  record('Formula hover shows the original excerpt');
  await ref.click();await page.locator('[data-source-highlight]').waitFor();
  assert.equal(await page.locator('#source-page').inputValue(),'4');
  assert.ok((await page.locator('.source-paper img').getAttribute('src')).includes('/crib/4.webp'));
  const controls=await page.locator('.source-toolbar button,.source-toolbar input').evaluateAll(nodes=>nodes.map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,button:e.tagName==='BUTTON'})));
  assert.ok(controls.every(c=>c.height===36&&(!c.button||c.width===36)));
  record('Source navigation, page input and zoom controls use consistent 36px sizing');
  const map=page.locator('.source-page-map[aria-current="page"]');
  const thumbnailList=page.locator('.source-thumbnail-list');
  async function selectedThumbnailVisible(){
    await page.waitForFunction(()=>{
      const list=document.querySelector('.source-thumbnail-list').getBoundingClientRect();
      const active=document.querySelector('.source-thumbnail[data-current]').getBoundingClientRect();
      return active.top>=list.top-1&&active.bottom<=list.bottom+1;
    });
  }
  await map.waitFor({state:'visible'});
  await map.locator('img').evaluate(img=>img.decode());
  await selectedThumbnailVisible();
  assert.equal(await page.locator('.source-thumbnail').count(),10);
  const layout=await thumbnailList.evaluate(list=>{
    const items=[...list.children].map(el=>el.getBoundingClientRect()),frame=list.getBoundingClientRect();
    return {scrollable:list.scrollHeight>list.clientHeight,vertical:items.every((item,index)=>!index||(item.top>items[index-1].bottom&&Math.abs(item.left-items[0].left)<1)),visible:items.filter(item=>item.top<frame.bottom&&item.bottom>frame.top).length};
  });
  assert.ok(layout.scrollable&&layout.vertical&&layout.visible>=2,JSON.stringify(layout));
  record('Page overview lists every PDF page vertically in a bounded scrolling rail');
  const readingPosition=await page.locator('.source-stage').evaluate(el=>el.scrollTop);
  await thumbnailList.evaluate(el=>el.scrollTop=0);
  await thumbnailList.hover();await page.mouse.wheel(0,320);
  await page.waitForFunction(()=>document.querySelector('.source-thumbnail-list').scrollTop>0);
  assert.equal(await page.locator('.source-stage').evaluate(el=>el.scrollTop),readingPosition);
  assert.equal(await page.locator('#source-page').inputValue(),'4');
  record('Scrolling thumbnails leaves the main page and its reading position unchanged');
  assert.equal(await page.locator('[data-source-map-highlight]').count(),1);
  await map.focus();await page.keyboard.press('Home');
  assert.equal(await page.locator('.source-stage').evaluate(e=>e.scrollTop),0);
  const mapBox=await map.boundingBox();
  await map.click({position:{x:mapBox.width/2,y:mapBox.height*.9}});
  const bottom=await page.locator('.source-stage').evaluate(e=>e.scrollTop);
  assert.ok(bottom>0);
  await map.focus();await page.keyboard.press('ArrowUp');
  assert.ok(await page.locator('.source-stage').evaluate(e=>e.scrollTop)<bottom);
  await page.getByRole('button',{name:'放大',exact:true}).click();
  await page.waitForFunction(()=>parseFloat(document.querySelector('[data-source-map-viewport]').style.width)<99);
  assert.equal((await map.boundingBox()).width,mapBox.width);
  await page.getByRole('button',{name:'缩小',exact:true}).click();
  record('Current thumbnail tracks scrolling and zoom, supports pointer and keyboard positioning');
  await page.getByRole('button',{name:'下一页',exact:true}).click();
  assert.equal(await page.locator('#source-page').inputValue(),'5');
  assert.equal(await page.locator('[data-source-highlight]').count(),0);
  assert.equal(await map.locator('[data-source-map-highlight]').count(),0);
  assert.equal(await page.locator('[data-thumbnail-page="4"] [data-source-map-highlight]').count(),1);
  assert.ok((await map.locator('img').getAttribute('src')).endsWith('/5.webp'));
  await selectedThumbnailVisible();
  await page.getByRole('button',{name:'上一页',exact:true}).click();
  assert.equal(await page.locator('[data-source-highlight]').count(),1);
  await page.locator('#source-page').fill('9');await page.locator('#source-page').press('Enter');
  await selectedThumbnailVisible();
  assert.ok((await map.locator('img').getAttribute('src')).endsWith('/9.webp'));
  await page.locator('[data-thumbnail-page="10"] button').click();
  assert.equal(await page.locator('#source-page').inputValue(),'10');
  assert.ok((await page.locator('.source-paper img').getAttribute('src')).endsWith('/10.webp'));
  assert.equal(await page.getByRole('button',{name:'下一页',exact:true}).isDisabled(),true);
  await page.locator('[data-thumbnail-page="1"] button').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#source-page').inputValue(),'1');
  assert.equal(await page.getByRole('button',{name:'上一页',exact:true}).isDisabled(),true);
  await selectedThumbnailVisible();
  await page.locator('#source-page').fill('4');await page.locator('#source-page').press('Enter');
  await selectedThumbnailVisible();
  assert.equal(await map.locator('[data-source-map-highlight]').count(),1);
  record('Thumbnail clicks and keyboard activation change pages; toolbar and page input reveal the selected thumbnail');
  await page.keyboard.press('Escape');record('PDF page navigation and exact formula highlight');
  await page.getByRole('button',{name:'Lecture 10',exact:true}).click();
  assert.equal(await page.locator('#source-page').inputValue(),'32');
  assert.ok((await page.locator('.source-paper img').getAttribute('src')).includes('/lecture-10/32.webp'));
  assert.equal(await page.locator('.source-thumbnail').count(),36);
  await selectedThumbnailVisible();
  await page.locator('[data-thumbnail-page="36"] button').click();
  assert.equal(await page.locator('#source-page').inputValue(),'36');
  await page.locator('.source-paper img').evaluate(img=>img.decode());
  assert.ok((await page.locator('.source-paper img').getAttribute('src')).endsWith('/lecture-10/36.webp'));
  await selectedThumbnailVisible();
  await page.keyboard.press('Escape');record('Long lecture PDFs show every page and open the cited or selected thumbnail');
  await page.getByRole('radio',{name:'原始插图',exact:true}).click();
  assert.ok((await page.locator('.figure-image img').first().getAttribute('src')).includes('/original-figures/'));
  await page.getByRole('radio',{name:'矢量复刻',exact:true}).click();
  assert.ok((await page.locator('.figure-image img').first().getAttribute('src')).endsWith('.svg'));
  record('Original figure / Matplotlib SVG switch');
  await page.getByRole('radio',{name:'练习',exact:true}).click();
  assert.equal(await page.locator('[data-answer]').count(),0);
  assert.equal(await page.locator('.solution-step').count(),0);
  assert.equal(await page.locator('.worked-solution textarea').count(),0);
  assert.equal(await page.locator('[id^="attempt-"]').count(),0);
  record('Practice uses a notebook workflow with no per-part text entry');
  await page.getByRole('button',{name:'开始分步推导',exact:true}).first().click();
  assert.equal(await page.locator('[data-part="e2-s26-q3-a"] .solution-step').count(),1);
  assert.equal(await page.locator('[data-answer]').count(),0);
  const practicePart=page.locator('[data-part="e2-s26-q3-a"]');
  const expectedPracticeSteps=exams.flatMap(e=>e.problems).find(q=>q.id==='e2-s26-q3').parts[0].steps.length;
  for(let count=2;count<=expectedPracticeSteps;count++){
    await practicePart.getByRole('button',{name:'下一步',exact:true}).click();
    assert.equal(await practicePart.locator('.solution-step').count(),count);
    assert.equal(await practicePart.locator('[data-answer]').count(),0);
  }
  await page.getByRole('button',{name:'查看最终答案',exact:true}).first().click();
  await page.getByRole('button',{name:'标记已掌握',exact:true}).first().click();
  record('Practice hides answers; reveal and mastery advance independently');
  assert.equal(await page.getByRole('tab',{name:'我的笔记',exact:true}).count(),0);
  assert.equal(await page.locator('textarea').count(),0);
  await page.getByRole('button',{name:'收藏此题',exact:true}).click();
  await page.getByRole('button',{name:'Switch to English',exact:true}).click();
  await page.getByRole('button',{name:'Switch to dark mode',exact:true}).click();
  await page.reload({waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.documentElement.lang==='en');
  // The bootstrap restores <html> before Svelte hydrates the SVG's theme.
  await page.waitForFunction(()=>document.querySelector('.figure-image img')?.getAttribute('src')?.endsWith('-dark.svg'));
  const data=await stored();assert.equal(data.theme,'dark');assert.equal(data.locale,'en');assert.equal(data.completed['e2-s26-q3-a'],true);assert.equal(data.bookmarks['e2-s26-q3'],true);
  assert.equal(await page.getByRole('tab',{name:'My notes',exact:true}).count(),0);
  assert.ok(await page.locator('html').evaluate(e=>e.classList.contains('dark')));
  assert.ok((await page.locator('.figure-image img').first().getAttribute('src')).endsWith('-dark.svg'));
  record('Locale, theme, mastery and bookmarks persist after reload without a notes UI');
  await page.getByRole('radio',{name:'Learn',exact:true}).click();
  await revealAll();
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:resolve(destination,'desktop-dark-en.png')});
  await page.getByRole('button',{name:'Switch to light mode',exact:true}).click();
  await page.getByRole('button',{name:'切换为中文',exact:true}).click();
  await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:resolve(destination,'desktop-light-zh.png')});
  await page.keyboard.press('Control+k');await page.locator('#global-search').fill('镜像');
  await page.getByRole('dialog').getByRole('link',{name:/导体平面上方的点电荷/}).click();
  await page.waitForURL('**/problems/e2-s26-q4/');
  assert.equal((await stored()).selected,'e2-s26-q4');record('Keyboard search navigates across the bilingual question bank');
  await revealAll();
  for(const viewport of [{width:375,height:812},{width:390,height:844},{width:768,height:1024},{width:667,height:375}]){
    await page.setViewportSize(viewport);await noOverflow();record(`No page overflow at ${viewport.width}×${viewport.height}`);
  }
  await page.setViewportSize({width:375,height:812});
  await page.getByRole('button',{name:'打开试卷导航',exact:true}).click();
  await page.getByRole('dialog').getByRole('tab',{name:'Exam 1',exact:true}).click();
  await page.waitForFunction(()=>JSON.parse(localStorage.getItem('ecse2100-fieldnotes-v1')).selected==='e1-f26-q1');
  await page.getByRole('dialog').waitFor({state:'detached'});
  assert.equal(await page.getByRole('dialog').count(),0);record('Mobile navigation drawer selects an exam and closes');
  await page.getByRole('button',{name:'打开公式与课件',exact:true}).click();
  await page.getByRole('dialog').waitFor();await page.keyboard.press('Escape');record('Mobile formula / lecture drawer works');
  await page.getByRole('button',{name:'Lecture 02',exact:true}).click();
  assert.equal(await page.locator('.source-overview').isVisible(),false);
  await page.locator('.source-dialog').evaluate(el=>Promise.all(el.getAnimations({subtree:true}).map(a=>a.finished.catch(()=>{}))));
  const phoneControls=await page.locator('.source-toolbar button,.source-toolbar input').evaluateAll(nodes=>nodes.map(e=>e.getBoundingClientRect().height));
  assert.ok(phoneControls.every(h=>h===36));await noOverflow();
  await page.keyboard.press('Escape');record('Phone source viewer preserves control sizing and hides the overview when space is limited');
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:resolve(destination,'mobile-light-zh.png'),fullPage:true});
  await page.getByRole('button',{name:'切换深色主题',exact:true}).click();
  await page.screenshot({path:resolve(destination,'mobile-dark-zh.png')});
  await page.setViewportSize({width:667,height:375});
  await page.getByRole('button',{name:'Lecture 02',exact:true}).click();
  const box=await page.getByRole('dialog').boundingBox();assert.ok(box.y>=0&&box.y+box.height<=376);
  await page.keyboard.press('Escape');record('Source viewer remains within a landscape phone viewport');
  assert.deepEqual(errors,[]);record('No uncaught browser errors');
  const report={status:'passed',checks,consoleErrors:errors,failedRequests:failures};
  await writeFile(resolve(destination,'browser-report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:'passed',checks:checks.length,artifacts:destination}));
} catch(error) {
  await writeFile(resolve(destination,'browser-report.json'),JSON.stringify({status:'failed',checks,consoleErrors:errors,failedRequests:failures,error:String(error)},null,2));
  console.log('Failure context',JSON.stringify({url:page.url(),errors,links:await page.locator('.formula-link').evaluateAll(nodes=>nodes.slice(0,5).map(n=>({tag:n.tagName,label:n.getAttribute('aria-label')}))).catch(()=>[])}));
  throw error;
} finally { await browser.close(); }
