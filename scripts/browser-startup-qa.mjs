// Reading must not wait for fonts or hydration. Run against a production build.
import assert from 'node:assert/strict';
import {mkdir,readdir,writeFile} from 'node:fs/promises';
import {course} from '../content/course.ts';
import {checkHoverContrast} from './browser-hover-qa.mjs';
import {checkStudyUX} from './browser-study-ux-qa.mjs';
import {checkNavigationStability} from './browser-navigation-qa.mjs';
import {checkFigureSegments} from './browser-figure-qa.mjs';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE??'playwright');
const browser=await chromium.launch({headless:true,...(process.env.QA_CHROMIUM?{executablePath:process.env.QA_CHROMIUM}:{}),args:['--no-sandbox']});
const base=process.env.QA_URL??'http://127.0.0.1:4173',checks=[];
const ids=(await readdir(new URL('../build/problems/',import.meta.url))).sort();
const sampleId=ids.includes(course.defaultProblemId)?course.defaultProblemId:ids[0];
assert.ok(sampleId,'At least one complete paper is required');
const pass=(name,data={})=>{checks.push({name,...data});console.log('PASS',name,JSON.stringify(data));};
const ready=p=>p.waitForFunction(()=>document.querySelector('[data-study-ready=true]'));
async function context(locale,width){
 const c=await browser.newContext({viewport:{width,height:812},reducedMotion:'reduce'});
 await c.addInitScript(({locale,storageKey})=>{
  if(location.protocol==='http:')localStorage.setItem(storageKey,JSON.stringify({version:1,locale}));
  window.readingAt=null;window.layoutShifts=[];
  const visible=selector=>{const node=document.querySelector(selector);if(!node)return false;const style=getComputedStyle(node);return node.getClientRects().length>0&&style.visibility==='visible'&&style.opacity!=='0';};
  const measure=()=>{if(visible('#problem-title')&&visible('[data-original-statement]'))window.readingAt=performance.now();else requestAnimationFrame(measure);};
  requestAnimationFrame(measure);
  new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.layoutShifts.push({at:e.startTime,value:e.value});}).observe({type:'layout-shift',buffered:true});
 },{locale,storageKey:course.storageKey});
 return c;
}
async function readable(p){
 await p.waitForFunction(()=>window.readingAt!==null,null,{timeout:2000});
 const elapsed=await p.evaluate(()=>window.readingAt-performance.getEntriesByType('navigation')[0].responseStart);
 assert.ok(elapsed<2000,`Reading took ${elapsed}ms after the HTML response`);
 return Math.round(elapsed);
}
try{
 await checkHoverContrast(browser,base,sampleId,pass);
 await checkStudyUX(browser,base,sampleId,pass);
 await checkFigureSegments(browser,base,sampleId,pass);
 await checkNavigationStability(browser,base,pass);
 for(const locale of ['zh','en'])for(const width of [375,1280]){
  let maxReadingMs=0,maxCLS=0;
  // Each destination gets an empty cache, rather than warming fonts across pages.
  for(const id of ids){
   const c=await context(locale,width),p=await c.newPage();
   try{
    await p.goto(`${base}/problems/${id}/`,{waitUntil:'commit'});
    maxReadingMs=Math.max(maxReadingMs,await readable(p));await ready(p);
    assert.equal(await p.locator('html').getAttribute('lang'),locale==='zh'?'zh-CN':'en');
    await p.evaluate(()=>document.fonts.ready);
    maxCLS=Math.max(maxCLS,await p.evaluate(()=>window.layoutShifts.reduce((sum,e)=>sum+e.value,0)));
   }finally{await c.close();}
  }
  // Report initial locale/layout shifts separately from time to readable content.
  pass('Cold pages expose their question promptly',{locale,width,pages:ids.length,maxReadingMs,maxCLS});
 }
 for(const locale of ['zh','en'])for(const width of [375,1280]){
  const c=await context(locale,width),p=await c.newPage();
  let releaseFonts,releaseScripts;
  const fonts=new Promise(resolve=>releaseFonts=resolve),scripts=new Promise(resolve=>releaseScripts=resolve);
  const fontRequests=[];
  p.on('request',r=>{if(r.resourceType()==='font')fontRequests.push(r.url());});
  await c.route('**/*',async route=>{
   if(route.request().resourceType()==='font')await fonts;
   if(route.request().resourceType()==='script')await scripts;
   await route.continue().catch(()=>{});
  });
  try{
   await p.goto(`${base}/problems/${sampleId}/`,{waitUntil:'commit'});
   const readingMs=await readable(p);
   assert.equal(await p.locator('main').getAttribute('data-study-ready'),'false');
   assert.ok(await p.locator('#problem-title').isVisible());
   releaseScripts();await ready(p);
   // Study controls work while every font stays pending.
   await p.locator('.solution-section-heading button').click();
   assert.equal(await p.locator('.part-trigger[aria-expanded=true]').count(),await p.locator('.part-trigger').count());
   await p.waitForTimeout(3100);
   assert.ok(await p.locator('[data-original-statement]').isVisible());
   assert.equal(await p.locator('#startup-status').isVisible(),false);
   assert.ok(fontRequests.length>0,'The test actually held a font request');
   assert.ok(fontRequests.every(url=>!url.includes('noto-sans-sc')),'No CJK webfont payload in either locale');
   const releaseAt=await p.evaluate(()=>performance.now());
   releaseFonts();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(100);
   const fontCLS=await p.evaluate(at=>window.layoutShifts.filter(e=>e.at>=at).reduce((sum,e)=>sum+e.value,0),releaseAt);
   assert.ok(fontCLS<=0.1,`Late font swap shifts the page: ${fontCLS}`);
   const fontBytes=await p.evaluate(()=>performance.getEntriesByType('resource').filter(e=>/\.woff2?(?:\?|$)/.test(e.name)).reduce((sum,e)=>sum+e.decodedBodySize,0));
   assert.ok(fontBytes<=200*1024,`Reading fonts exceeded 200 KiB: ${fontBytes}`);
   pass('Delayed fonts and scripts do not block reading; font transfer and late shifts stay bounded',{locale,width,readingMs,fontBytes,fontCLS});
  }finally{releaseScripts();releaseFonts();await c.close();}
 }
 const c=await context('zh',1280),p=await c.newPage();
 try{
  for(const id of ids){const response=await p.request.get(`${base}/problems/${id}`);assert.equal(response.status(),200);assert.ok((await response.text()).includes(`data-problem="${id}"`));}
  pass('All discovered no-slash destinations resolve',{pages:ids.length});
  await p.goto(`${base}/problems/${sampleId}/`);await ready(p);
  await p.getByRole('button',{name:'搜索题目与公式',exact:true}).click();
  await p.locator('#global-search').fill('');
  await p.locator(`.search-result[href="/problems/${ids[0]}/"]`).focus();
  await p.keyboard.press('Enter');await p.waitForURL(`**/problems/${ids[0]}/`);
  assert.ok(await p.locator('#problem-title').evaluate(e=>e===document.activeElement&&e.matches(':focus-visible')&&getComputedStyle(e).outlineStyle!=='none'));
  pass('Keyboard search destinations retain visible heading focus');
 }finally{await c.close();}
}finally{await mkdir('artifacts',{recursive:true});await writeFile('artifacts/startup-qa.json',JSON.stringify({checks},null,2));await browser.close();}
