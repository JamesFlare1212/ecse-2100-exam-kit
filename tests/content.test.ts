import {describe,expect,test} from 'bun:test';
import {existsSync,readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import katex from 'katex';
import {exams,examIndex,problemEntries,documents} from '../src/lib/catalog.server';
import {createCatalog,formulas} from '../src/lib/catalog';
import {assetSource} from '../content/papers.server';
import {plainText,renderText} from '../src/lib/math';
import {conclusionMath} from '../src/lib/answer-math';

const root=resolve(import.meta.dir,'..');
const {partIds}=createCatalog(examIndex,documents);
const exists=(path:string)=>existsSync(assetSource(path));
const checkTex=(tex:string)=>katex.renderToString(tex,{throwOnError:true,strict:'ignore',trust:false});
describe('Complete, bilingual and source-addressable content',()=>{
  test('the client index preserves all searchable questions without shipping solutions',()=>{
    expect(examIndex.map(e=>e.id)).toEqual(exams.map(e=>e.id));
    for(const exam of exams){
      const indexed=examIndex.find(e=>e.id===exam.id)!;
      expect(indexed.problems.map(p=>p.id)).toEqual(exam.problems.map(p=>p.id));
      for(const question of exam.problems){
        const summary=indexed.problems.find(p=>p.id===question.id)!;
        expect(summary.title).toEqual(question.title);
        expect(summary.topic).toEqual(question.topic);
        expect(summary.statement).toEqual(question.statement);
        expect(summary.parts).toEqual(question.parts.map(({id,prompt})=>({id,prompt})));
        expect(summary).not.toHaveProperty('guide');
        expect(summary).not.toHaveProperty('givens');
        for(const part of summary.parts){expect(part).not.toHaveProperty('steps');expect(part).not.toHaveProperty('answer');}
      }
    }
  });
  test('every original subpart is represented exactly once',()=>{
    expect(exams.length).toBeGreaterThan(0);
    expect(new Set(problemEntries.map(entry=>entry.problem.id)).size).toBe(problemEntries.length);
    expect(partIds.size).toBe(problemEntries.reduce((n,entry)=>n+entry.problem.parts.length,0));
    const expected:Record<string,number[]>={'e1-f25':[5,4,5,4],'e1-s26':[6,4,4,4],'e1-f26':[4,6,4,5],'e2-f25':[7,4,4,5],'e2-s26':[5,4,4,5]};
    for(const exam of exams)if(expected[exam.id])expect(exam.problems.map(p=>p.parts.length)).toEqual(expected[exam.id]);
    for(const exam of exams){expect(exam.problems.reduce((n,p)=>n+p.points,0)).toBe(exam.points);}
  });
  test('translations contain no accidentally decoded TeX controls or literal Unicode escapes',()=>{
    function visit(v:unknown){
      if(typeof v==='string'){expect(v).not.toMatch(/[\u0000-\u0008\u000b-\u001f]|\\u[\da-f]{4}/i);}
      else if(Array.isArray(v))v.forEach(visit);
      else if(v&&typeof v==='object'){
        const record=v as Record<string,unknown>;
        if('zh' in record||'en' in record){expect(typeof record.zh).toBe('string');expect(typeof record.en).toBe('string');expect(record.zh).toBeTruthy();expect(record.en).toBeTruthy();}
        Object.values(record).forEach(visit);
      }
    }
    visit(exams);visit(formulas);
  });
  test('all equations and boxed answers compile in KaTeX',()=>{
    let count=0;
    function inline(text:string){for(const m of text.matchAll(/\$([^$\n]+)\$/g)){checkTex(m[1]);count++;}}
    for(const {problem:q} of problemEntries){q.givens.forEach(tex=>{checkTex(tex);count++;});inline(q.statement.zh);inline(q.statement.en);for(const text of Object.values(q.guide)){inline(text.zh);inline(text.en);}
      for(const p of q.parts){expect(p.steps.length).toBeGreaterThanOrEqual(2);checkTex(`\\boxed{${p.answer}}`);const conclusion=conclusionMath(p.steps.at(-1)?.math,p.answer);checkTex(conclusion.result);if(conclusion.calculation)checkTex(conclusion.calculation);expect(conclusion.result).toContain('\\boxed{');count++;inline(p.prompt.zh);inline(p.prompt.en);for(const s of p.steps){if(s.math){checkTex(s.math);count++;}for(const ref of s.refs)expect(formulas.some(f=>f.id===ref)).toBe(true);}}
    }
    for(const f of formulas){checkTex(f.math);count++;}
    expect(count).toBeGreaterThanOrEqual(partIds.size*4+formulas.length);
  });
  test('the dielectric comparison displays its final result once',()=>{
    const part=problemEntries.find(({problem})=>problem.id==='e2-f25-q1')?.problem.parts.find(part=>part.label==='g');
    if(!part)return;
    const conclusion=conclusionMath(part.steps.at(-1)?.math,part.answer);
    expect(conclusion.calculation).toBeUndefined();
    expect(conclusion.result.match(/\\boxed\{/g)).toHaveLength(1);
  });
  test('all 93 solutions start with an equation and show intermediate calculation steps',()=>{
    for(const {problem} of problemEntries)for(const part of problem.parts){
      expect(part.steps.length,part.id).toBeGreaterThanOrEqual(3);
      expect(part.steps[0].math,part.id).toBeTruthy();
      expect(part.steps[0].math,part.id).not.toBe(part.answer);
      for(const step of part.steps){
        expect(step.math,part.id).toBeTruthy();
        expect(step.text.zh,part.id).not.toMatch(/待补充|TODO/);
        expect(step.text.en,part.id).not.toMatch(/TODO|placeholder/i);
      }
      if(part.figure){
        expect(part.figureCaption?.zh,part.id).toBeTruthy();
        expect(part.figureCaption?.en,part.id).toBeTruthy();
      }
    }
    const sphere=problemEntries.find(({problem})=>problem.id==='e2-f25-q1')?.problem;
    if(!sphere)return;
    for(const label of ['b','d']){
      const math=sphere.parts.find(p=>p.label===label)!.steps.map(s=>s.math).join('\n');
      expect(math).toContain('\\oiint');
      expect(math).toContain('\\sin\\theta');
      expect(math).toContain('\\int_0^{2\\pi}');
      expect(math).toContain('\\int_0^\\pi');
    }
  });
  test('every problem has a complete bilingual introduction before its derivation',()=>{
    for(const {problem} of problemEntries){
      expect(Object.keys(problem.guide).sort()).toEqual(['approach','concept','goal','known']);
      for(const section of Object.values(problem.guide)){
        expect(section.zh.length).toBeGreaterThan(20);expect(section.en.length).toBeGreaterThan(30);
        expect(section.zh).not.toBe(section.en);
        expect(section.zh+section.en).not.toMatch(/\\boxed|TODO|待补充/);
      }
      expect(problem.lectures.length).toBeGreaterThan(0);
    }
    const strip=problemEntries.find(({problem})=>problem.id==='e2-s26-q1')?.problem;
    if(!strip)return;
    expect(strip.guide.known.zh).toContain('中间区域为零');
    expect(strip.guide.known.zh).not.toContain('0.2');
    expect(strip.lectures.map(ref=>[ref.doc,ref.page])).toEqual([['lecture-14',9],['lecture-14',14]]);
  });
  test('all pages, SVG themes, original figures and formula excerpts exist',()=>{
    for(const doc of Object.values(documents)){expect(exists(doc.pdf)).toBe(true);for(let p=1;p<=doc.pages;p++)expect(exists(`${doc.pageBase}/${p}.webp`)).toBe(true);}
    function source(doc:string,page:number,region?:number[]){expect(documents[doc]).toBeDefined();expect(page).toBeGreaterThan(0);expect(page).toBeLessThanOrEqual(documents[doc].pages);if(region){expect(region).toHaveLength(4);expect(region[0]).toBeGreaterThanOrEqual(0);expect(region[1]).toBeGreaterThanOrEqual(0);expect(region[0]+region[2]).toBeLessThanOrEqual(1);expect(region[1]+region[3]).toBeLessThanOrEqual(1);}}
    for(const {exam,problem:q,paper} of problemEntries){source(q.originalFigure.doc,q.originalFigure.page,q.originalFigure.region);q.lectures.forEach(r=>source(r.doc,r.page));expect(exists(`${paper.assetBase}/original-figures/${q.id}.webp`)).toBe(true);
      for(const figure of [q.figure,...q.parts.flatMap(p=>[p.figure,p.questionFigure?.name]).filter(Boolean)]){for(const suffix of ['','-dark']){const path=`${paper.assetBase}/figures/${figure}${suffix}.svg`;expect(exists(path)).toBe(true);const svg=readFileSync(assetSource(path),'utf8');expect(svg).toContain('<svg');expect(svg).toContain('<text');expect(svg).not.toContain('<image');}}
      q.parts.forEach(p=>{source(exam.doc,p.sourcePage);source(exam.solutionDoc,p.solutionPage);if(p.questionFigure){const r=p.questionFigure.source;source(r.doc,r.page,r.region);expect(exists(`${paper.assetBase}/original-figures/${p.questionFigure.name}.webp`)).toBe(true);}});
    }
    for(const f of formulas){source(f.source.doc,f.source.page,f.source.region);expect(exists(`/excerpts/${f.id}.webp`)).toBe(true);}
  });
  test('original questions retain the source wording, givens and requested explanations',()=>{
    for(const {problem} of problemEntries)expect(problem.wording).toBe('original');
    const leaky=problemEntries.find(({problem})=>problem.id==='e2-s26-q3')?.problem;
    if(leaky){
    expect(leaky.title.en).toBe('Leaky Coaxial Cable Dielectric');
    expect(leaky.statement.en).toContain('The coaxial cable to the right has a poor dielectric, which has allowed some charge to leak');
    expect(leaky.parts[0].prompt.en).toContain('Include a diagram that shows the location of your Gaussian surface.');
    expect(leaky.parts[3].prompt.en).toContain('the capacitance cannot be computed using the usual formulas.');
    }
    const plates=problemEntries.find(({problem})=>problem.id==='e2-f25-q2')?.problem;
    // The printed sign error belongs in the original question; its correction is a solution note.
    if(plates)expect(plates.statement.en).toContain('\\frac{V_1-V_0}{L}');
    const matching=problemEntries.find(({problem})=>problem.id==='e1-f26-q4')?.problem;
    if(matching){
    expect(matching.parts[4].prompt.en).toContain('Circle all that apply.');
    expect(matching.parts[4].prompt.en).toContain('d. No reflections occur anywhere in the system since the feedline is matched to the load.');
    }
    const spring=problemEntries.find(({problem})=>problem.id==='e1-s26-q1')?.problem;
    if(spring)expect(spring.parts.at(-1)?.label).toBe('f');
  });
  test('English prose matches the independently extracted source PDFs',()=>{
    const normalize=(s:string)=>s.normalize('NFKC').toLowerCase().replaceAll('’',"'").replaceAll('–','-').replaceAll('−','-').replace(/[^a-z0-9]+/g,' ').trim();
    // PDF p.7 places dQ above the surrounding sentence, scrambling these two
    // runs in text extraction. They were checked directly against the page image.
    const checkedOnPage=new Set([
      'When a volumetric charge density exists in the region between two conductors, the capacitance cannot be computed using the usual formulas. Instead, it must be defined by ',
      ' is the total charge on one conductor and ',
    ]);
    let checked=0,visualChecks=0;
    for(const exam of exams){
      const source=normalize(readFileSync(resolve(root,`content/${problemEntries.find(entry=>entry.exam.id===exam.id)!.paper.name}/extracted/${exam.doc}.txt`),'utf8'));
      for(const q of exam.problems)for(const [part,text] of [['statement',q.statement.en],...q.parts.map(p=>[p.label,p.prompt.en])]){
        for(const run of text.split(/\$\$[\s\S]*?\$\$|\$[^$\n]+\$/))for(const line of run.split('\n')){
          const prose=normalize(line);if(prose.split(' ').length<4)continue;
          if(q.id==='e2-s26-q3'&&part==='d'&&checkedOnPage.has(line)){visualChecks++;continue;}
          expect(source,`${q.id} ${part}: ${line}`).toContain(prose);checked++;
        }
      }
    }
    expect(checked).toBeGreaterThan(0);
    expect(visualChecks).toBe(problemEntries.some(entry=>entry.problem.id==='e2-s26-q3')?2:0);
  });
  test('text renderer escapes markup while preserving mathematical typesetting',()=>{const html=renderText('<img src=x onerror=alert(1)> $a^2$');expect(html).toContain('&lt;img');expect(html).not.toContain('<img');expect(html).toContain('katex');});
  test('figure text alternatives preserve symbols without exposing TeX or markup',()=>{
    const caption=plainText('高斯面 $a<R<b$，法向 $\\hat r$，电场 $\\vec E$。');
    expect(caption).toContain('a<R<b');
    expect(caption).toContain('E⃗');
    expect(caption).not.toMatch(/\$|\\|<(?:math|span|mi|mo)\b/);
  });
  test('current-density vectors keep the question’s arrow notation throughout the derivation',()=>{
    const strip=problemEntries.find(({problem})=>problem.id==='e2-s26-q1')?.problem;
    if(!strip)return;
    for(const locale of ['zh','en'] as const){
      expect(strip.statement[locale]).toMatch(/\\vec\s*J/);
      expect(strip.parts[0].steps[0].text[locale]).toMatch(/\$\\vec\s*J\$/);
    }
    expect(strip.parts[0].steps[0].math).toContain('\\vec{J}\\cdot d\\vec{S}');
    expect(formulas.find(f=>f.id==='ohm')?.math).toBe('\\vec{J}=\\sigma\\vec{E}');
    expect(strip.parts[0].answer).toContain('J_0');
    expect(strip.parts[0].answer).not.toContain('\\vec');
  });
  test('worked integrals retain antiderivatives, endpoint subtraction and intermediate algebra',()=>{
    const calculations=(id:string)=>problemEntries.flatMap(({problem})=>problem.parts)
      .find(part=>part.id===id)?.steps.map(step=>step.math).join('\n');
    const milestones:Record<string,string[]>={
      'e2-s26-q1-a':['[J_0y]_0^W','[z]_{-0.5h}^{-0.4h}','(-0.4h+0.5h)','[z]_{0.4h}^{0.5h}','I_{\\mathrm{middle}}'],
      'e2-f25-q1-b':['(-\\cos\\pi)-(-\\cos0)','\\frac{R^3}{3}-\\frac{0^3}{3}'],
      'e2-f25-q1-d':['(-\\cos\\pi)-(-\\cos0)','\\frac{a^3}{3}-\\frac{0^3}{3}'],
      'e2-f25-q2-b':['[x]_0^L','[y]_0^W','[z]_{H/2}^H','[z]_0^{H/2}'],
      'e2-f25-q3-a':['\\int0\\,dr','[\\ln(s/a)]_a^r','V(a)=A\\ln1+B=0','V(b)=A\\ln(b/a)=-V_0'],
      'e2-f25-q3-b':['\\frac1{r/a}\\frac d{dr}(r/a)','\\frac ar\\frac1a'],
      'e2-s26-q3-a':['[r^\\prime]_a^R=R-a','[\\phi]_0^{2\\pi}','[z]_0^\\ell'],
      'e2-s26-q3-b':['[\\ln(s/a)]_r^b','\\ln(b/a)-\\ln(r/a)','[s]_r^b=b-r'],
      'e1-s26-q4-c':['g-gbt+gbt+gt^2','129600-59800=69800','0.274760-j0.725907'],
    };
    for(const[id,required]of Object.entries(milestones)){
      const math=calculations(id);
      if(!math)continue; // Unplugged papers are deliberately absent from the active catalog.
      for(const expression of required)expect(math,`${id}: ${expression}`).toContain(expression);
    }
  });
});

type C={re:number;im:number};
const add=(a:C,b:C):C=>({re:a.re+b.re,im:a.im+b.im});
const mul=(a:C,b:C):C=>({re:a.re*b.re-a.im*b.im,im:a.re*b.im+a.im*b.re});
const div=(a:C,b:C):C=>{const d=b.re*b.re+b.im*b.im;return{re:(a.re*b.re+a.im*b.im)/d,im:(a.im*b.re-a.re*b.im)/d};};
const scale=(a:C,n:number):C=>({re:a.re*n,im:a.im*n});
function input(z:C,d:number):C {const t=Math.tan(2*Math.PI*d);return div(add(z,{re:0,im:t}),add({re:1,im:0},mul({re:0,im:t},z)));}
describe('Independent physical and numerical consistency checks',()=>{
  test('numerical quadrature agrees with the expanded current, Gaussian charge and potential integrals',()=>{
    function integrate(f:(x:number)=>number,a:number,b:number){
      const n=400,h=(b-a)/n;
      let sum=f(a)+f(b);
      for(let i=1;i<n;i++)sum+=(i%2?4:2)*f(a+i*h);
      return sum*h/3;
    }
    const J0=3.7,W=1.3,h=.8;
    const inner=(z:number)=>integrate(()=>Math.abs(z)>.4*h?J0:0,0,W);
    // One-sided interval endpoints do not change the integral; evaluate inside each layer.
    const current=integrate(()=>inner(-.45*h),-.5*h,-.4*h)
      +integrate(()=>inner(0),-.4*h,.4*h)
      +integrate(()=>inner(.45*h),.4*h,.5*h);
    expect(current).toBeCloseTo(.2*J0*W*h,10);
    const rho=2.1,R=1.7;
    const angular=integrate(()=>1,0,2*Math.PI)*integrate(Math.sin,0,Math.PI);
    expect(angular).toBeCloseTo(4*Math.PI,8);
    expect(rho*angular*integrate(r=>r*r,0,R)).toBeCloseTo(4*Math.PI*rho*R**3/3,8);
    const a=1.2,b=4,eps=2.3,rho0=.7,sa=3,r=2;
    const enclosed=2*Math.PI*a*sa+2*Math.PI*integrate(s=>rho0*a/s*s,a,r);
    expect(enclosed).toBeCloseTo(2*Math.PI*a*(sa+rho0*(r-a)),10);
    const field=(s:number)=>a/(eps*s)*(sa+rho0*(s-a));
    const potential=-integrate(field,b,r);
    expect(potential).toBeCloseTo(a/eps*((sa-a*rho0)*Math.log(b/r)+rho0*(b-r)),9);
  });
  test('both exact single-stub branches match each stated load',()=>{
    for(const [z,branches] of [[{re:2,im:1},[[.19879180882521663,.375],[.375,.125]]],[{re:.5,im:1.8},[[.27528271387830444,.30758870570883495],[.3784108474800829,.19241129429116505]]]] as [C,number[][]][]){
      for(const [d,l] of branches){const y=div({re:1,im:0},input(z,d));expect(y.re).toBeCloseTo(1,10);expect(y.im+Math.tan(2*Math.PI*l)).toBeCloseTo(0,10);}
    }
  });
  test('F26 quarter-wave network reaches two real impedances and matches to 50 Ω',()=>{
    const z={re:3,im:-1};for(const [d,resistance] of [[.23259887818173403,14.837129522559273],[.482598878181734,168.49620381077406]]){const zin=scale(input(z,d),50);expect(zin.im).toBeCloseTo(0,9);expect(zin.re).toBeCloseTo(resistance,9);const zt=Math.sqrt(50*resistance);expect(zt*zt/resistance).toBeCloseTo(50,10);}
  });
  test('the official F26 interface choices retain local reflections while net input reflection cancels',()=>{
    const part=problemEntries.find(({problem})=>problem.id==='e1-f26-q4')?.problem.parts.at(-1);
    if(part){expect(part.answer).toBe('\\text{Interfaces (a), (b) and (c)}');expect(part.answerText?.en).toContain('Select a, b and c');}
    const load={re:150,im:-50},gammaLoad=div(add(load,{re:-50,im:0}),add(load,{re:50,im:0}));
    expect(Math.hypot(gammaLoad.re,gammaLoad.im)).toBeGreaterThan(0);
    for(const resistance of [14.837129522559273,168.49620381077406]){
      const transformer=Math.sqrt(50*resistance);
      const localA=(transformer-50)/(transformer+50),localB=(50-transformer)/(50+transformer);
      expect(Math.abs(localA)).toBeGreaterThan(.1);
      expect(localA+localB).toBeCloseTo(0,12);
      const networkInput=transformer**2/resistance;
      expect((networkInput-50)/(networkInput+50)).toBeCloseTo(0,12);
    }
  });
  test('F25 phasor satisfies both the 10 V source and 125 Ω load boundary',()=>{
    const vp=5,vm=-15/7,z0=50;const v0=vp+vm,i0=(vp-vm)/z0;expect(v0+50*i0).toBeCloseTo(10,12);
    const vL={re:0,im:-vp+vm},iL={re:0,im:(-vp-vm)/z0};expect(div(vL,iL).re).toBeCloseTo(125,12);
  });
  test('DC bounce amplitudes and the infinite geometric sum agree',()=>{const initial=10*50/80,gL=.5,gg=-.25;expect(initial*(1+gL)).toBe(9.375);expect(initial*(1+gL)*(1+gL*gg)).toBe(8.203125);expect(initial*(1+gL)/(1-gL*gg)).toBeCloseTo(10*150/180,12);});
  test('loss and impedance power relations conserve net power',()=>{expect((5*5-3*3)/(2*50)).toBe(.16);expect(.5*Math.exp(-30/150)).toBeCloseTo(.4093653765,9);expect(-Math.log(.904)/100).toBeCloseTo(.00100923,7);});
  test('spherical Gauss field is continuous at a and the outer net charge is zero',()=>{const rho=2,a=3,eps=5;const inner=rho*a/(3*eps),outside=rho*a**3/(3*eps*a*a);expect(inner).toBe(outside);expect(4*Math.PI*eps*a*a*inner).toBeCloseTo(4*Math.PI*rho*a**3/3,10);});
  test('space-charge potential differentiates to the Gauss field and has the right capacitance',()=>{
    const a=1.2,b=4,eps=2.3,rho0=.7,sa=3;const V=(r:number)=>a/eps*((sa-a*rho0)*Math.log(b/r)+rho0*(b-r));expect(V(b)).toBe(0);
    for(const r of [1.3,2,3.5]){const h=1e-5,field=-(V(r+h)-V(r-h))/(2*h);expect(field).toBeCloseTo(a/(eps*r)*(sa+rho0*(r-a)),8);}
    const density=(v:number)=>eps*v/(a*Math.log(b/a))+a*rho0-rho0*(b-a)/Math.log(b/a);const h=1e-5;const dQ=2*Math.PI*a*(density(2+h)-density(2-h))/(2*h);expect(dQ).toBeCloseTo(2*Math.PI*eps/Math.log(b/a),8);
  });
  test('image-charge superposition cancels tangential field and preserves surface-charge signs',()=>{
    const x0=1.3,z0=.8,q=2;const charges=[[x0,z0,q],[-x0,z0,-q],[x0,-z0,-q],[-x0,-z0,q]];
    for(const x of [-2,-.3,0,.3,2]){let Ex=0,Ez=0;for(const [xc,zc,Q] of charges){const r3=((x-xc)**2+zc**2)**1.5;Ex+=Q*(x-xc)/r3;Ez+=Q*(-zc)/r3;}const expected=2*q*z0*(1/((x+x0)**2+z0*z0)**1.5-1/((x-x0)**2+z0*z0)**1.5);expect(Ex).toBeCloseTo(0,12);expect(Ez).toBeCloseTo(expected,12);if(x>0)expect(Ez).toBeLessThan(0);}
  });
  test('dielectric and current-density results use the appropriate components and area',()=>{const e2n=2/5*(-100);expect(e2n).toBe(-40);expect(-e2n*.01).toBe(.4);const J=3,W=2,h=.5,sigma=4,I=.2*J*W*h,R=(J/sigma)/I;expect(R).toBeCloseTo(5/(sigma*W*h),12);});
});
