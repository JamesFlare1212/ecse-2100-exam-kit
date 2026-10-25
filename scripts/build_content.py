"""Compile the authored bilingual question bank to a framework-independent JSON file."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
def L(zh,en): return {'zh':zh,'en':en}
def S(zh,en,math='',refs=()):
    return {'text':L(zh,en),'math':math,'refs':list(refs)}
def P(label,points,zh,en,steps,answer,page,sol=None,**extra):
    return {'label':label,'points':points,'prompt':L(zh,en),'steps':steps,'answer':answer,'sourcePage':page,'solutionPage':sol or page,**extra}
def R(n,page,zh,en):
    return {'doc':f'lecture-{n:02d}','page':page,'label':L(zh,en)}
def Q(exam,num,zh,en,topic,statement,givens,points,page,region,lectures,parts,caption=None,**extra):
    id=f'{exam}-q{num}'
    for p in parts: p['id']=f'{id}-{p["label"].replace("(","").replace(")","")}'
    return {'id':id,'number':num,'title':L(zh,en),'topic':L(*topic),'statement':L(*statement),'givens':givens,'points':points,'figure':id,'figureCaption':L(*(caption or ('几何示意图；尺寸以题设符号为准。','Schematic geometry; dimensions follow the symbols in the question.'))),'originalFigure':{'doc':exam,'page':page,'region':region},'lectures':lectures,'parts':parts,**extra}
def E(id,num,season,year,points,problems,questionsOnly=True):
    return {'id':id,'number':num,'term':L(season[0],season[1]),'year':year,'points':points,'doc':id,'solutionDoc':id+'-sol' if questionsOnly else id,'questionsOnly':questionsOnly,'problems':problems}

# These imports contain only authored data and math, never scrape-generated solutions.
from exam2 import create as exam2
from exam1 import create as exam1
from original_questions import apply_original_questions
from source_figures import apply_source_figures
from question_translations import apply_translations
from problem_guides import apply_guides
exams=exam1(L,S,P,R,Q,E)+exam2(L,S,P,R,Q,E)
apply_original_questions(exams)
apply_translations(exams)
apply_source_figures(exams)
apply_guides(exams)
dest=ROOT/'src/lib/data/exams.json'
dest.write_text(json.dumps(exams,ensure_ascii=False,indent=2)+'\n')
print(f'{len(exams)} exams / {sum(len(e["problems"]) for e in exams)} problems / {sum(len(q["parts"]) for e in exams for q in e["problems"])} parts')
