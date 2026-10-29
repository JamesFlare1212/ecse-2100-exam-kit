// Cold-load layout and startup fallbacks, without a persistent browser profile.
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE??'playwright');
const b=await chromium.launch({headless:true,...(process.env.QA_CHROMIUM?{executablePath:process.env.QA_CHROMIUM}:{}),args:['--no-sandbox']});
const base=process.env.QA_URL??'http://127.0.0.1:4188',checks=[];
const pass=(name,data={})=>{checks.push({name,...data});console.log('PASS',name,JSON.stringify(data));};
const ids=['e1-f25','e1-f26','e1-s26','e2-f25','e2-s26'].flatMap(p=>[1,2,3,4].map(n=>`${p}-q${n}`));
try{
 for(const locale of ['zh','en'])for(const width of [375,1280]){
  const c=await b.newContext({viewport:{width,height:812},reducedMotion:'reduce'});
  await c.addInitScript(locale=>{
   if(location.protocol==='http:')localStorage.setItem('ecse2100-fieldnotes-v1',JSON.stringify({version:1,locale}));
   window.layoutEntries=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.layoutEntries.push({value:e.value,sources:e.sources.map(s=>s.node?.parentElement?.closest('.app-shell')?s.node?.parentElement?.className:'startup')});}).observe({type:'layout-shift',buffered:true});
  },locale);
  const p=await c.newPage();let shifts=0;
  for(const id of ids){
   await p.goto(`${base}/problems/${id}/`,{waitUntil:'domcontentloaded'});
   await p.waitForFunction(()=>document.querySelector('[data-study-ready=true]')&&!document.documentElement.hasAttribute('data-render-pending'));
   await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(80);
   const entries=await p.evaluate(()=>window.layoutEntries);
   const reading=entries.filter(e=>e.sources.some(s=>s!=='startup'));shifts+=reading.length;
   assert.equal(reading.length,0,`${id} ${locale} ${width}: `+JSON.stringify(reading));
   assert.ok(await p.locator('#problem-title').isVisible());
  }
  pass('L1: all 20 initial pages settle fonts and locale before displaying the reading document',{locale,width,readingShiftEvents:shifts});await c.close();
 }
 // Artificially slow fonts must keep a visible, usable loading state.
 const c=await b.newContext({viewport:{width:375,height:812}}),p=await c.newPage();
 await p.route('**/*.woff2',async r=>{await new Promise(resolve=>setTimeout(resolve,1500));await r.continue();});
 await p.goto(`${base}/problems/e2-s26-q3/`,{waitUntil:'domcontentloaded'});
 assert.ok(await p.locator('#startup-status').isVisible());await p.waitForFunction(()=>!document.documentElement.hasAttribute('data-render-pending'));assert.ok(await p.locator('#problem-title').isVisible());pass('L1: slow fonts show recovery controls and then reveal a settled document');
 await p.unroute('**/*.woff2');
 // Both canonical and no-slash destinations must resolve to the application.
 for(const id of ids){const response=await p.request.get(`${base}/problems/${id}`);assert.equal(response.status(),200);assert.ok((await response.text()).includes(`data-problem="${id}"`));}pass('I27: all 20 no-slash problem URLs resolve successfully');
 await p.goto(`${base}/problems/e2-s26-q3/`);await p.waitForFunction(()=>!document.documentElement.hasAttribute('data-render-pending'));
 await p.getByRole('button',{name:'搜索题目与公式',exact:true}).click();await p.locator('#global-search').fill('高频下微带线的电阻');await p.locator('#global-search').press('Tab');await p.keyboard.press('Enter');await p.waitForURL('**/e2-s26-q1/');assert.ok(await p.locator('#problem-title').evaluate(e=>e===document.activeElement&&e.matches(':focus-visible')&&getComputedStyle(e).outlineStyle!=='none'));pass('I6: keyboard search destinations have a visible heading focus ring');
 await c.close();
}finally{await mkdir('artifacts',{recursive:true});await writeFile('artifacts/startup-qa.json',JSON.stringify({checks},null,2));await b.close();}
