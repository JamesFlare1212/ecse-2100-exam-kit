/** Keep result emphasis in TeX; never add a second answer card around it. */
type Token = {start:number; end:number; kind:'space'|'relation'|'row'};

function topLevelTokens(tex:string):Token[] {
  const tokens:Token[]=[];
  let braces=0, environments=0;
  for(let i=0;i<tex.length;){
    if(tex[i]==='\\'){
      if(tex[i+1]==='{'||tex[i+1]==='}'){i+=2;continue;}
      const environment=/^\\(begin|end)\{[a-zA-Z*]+\}/.exec(tex.slice(i));
      if(environment){environments+=environment[1]==='begin'?1:-1;i+=environment[0].length;continue;}
      if(tex[i+1]==='\\'){
        if(!braces&&!environments)tokens.push({start:i,end:i+2,kind:'row'});
        i+=2;continue;
      }
      const command=/^\\([a-zA-Z]+)/.exec(tex.slice(i));
      if(command){
        if(!braces&&!environments){
          if(command[1]==='quad'||command[1]==='qquad')tokens.push({start:i,end:i+command[0].length,kind:'space'});
          if(command[1]==='approx')tokens.push({start:i,end:i+command[0].length,kind:'relation'});
        }
        i+=command[0].length;continue;
      }
      i+=2;continue;
    }
    if(tex[i]==='{')braces++;
    else if(tex[i]==='}')braces--;
    else if(tex[i]==='='&&!braces&&!environments)tokens.push({start:i,end:i+1,kind:'relation'});
    i++;
  }
  return tokens;
}

const box=(tex:string)=>'\\boxed{'+tex.trim()+'}';
const normalize=(tex:string)=>tex.replace(/\s+/g,'');

function splitAt(tex:string,tokens:Token[]){
  const pieces:{text:string;separator:string}[]=[];
  let offset=0;
  for(const token of tokens){
    let text=tex.slice(offset,token.start).trim();
    let separator=tex.slice(token.start,token.end)+' ';
    if(text.endsWith(',')){text=text.slice(0,-1).trimEnd();separator=','+separator;}
    pieces.push({text,separator});offset=token.end;
  }
  pieces.push({text:tex.slice(offset).trim(),separator:''});
  return pieces;
}

function emphasizeSegment(tex:string,hasOtherSegments:boolean):string {
  // Units, domain conditions and connecting prose are not separate results.
  if(hasOtherSegments&&(/^\[[\s\S]*\]$/.test(tex)||/^\([\s\S]*\)$/.test(tex)||/^\\text\{[\s\S]*\}$/.test(tex)))return tex;
  // An inequality or a geometry statement is meaningful as a complete result.
  if(/[<>]/.test(tex)||/\\(?:Longrightarrow|parallel)\b/.test(tex))return box(tex);
  const relation=topLevelTokens(tex).filter(t=>t.kind==='relation').at(-1);
  if(relation)return tex.slice(0,relation.end)+box(tex.slice(relation.end));
  return box(tex);
}

export function emphasizeAnswer(answer:string):string {
  const gathered=/^\\begin\{gathered\}([\s\S]*)\\end\{gathered\}$/.exec(answer);
  if(gathered){
    const body=gathered[1];
    return '\\begin{gathered}'+splitAt(body,topLevelTokens(body).filter(t=>t.kind==='row'))
      .map(({text,separator})=>emphasizeAnswer(text)+separator).join('')+'\\end{gathered}';
  }
  const pieces=splitAt(answer,topLevelTokens(answer).filter(t=>t.kind==='space'));
  return pieces.map(({text,separator})=>emphasizeSegment(text,pieces.length>1)+separator).join('');
}

export function conclusionMath(calculation:string|undefined,answer:string):{calculation?:string;result:string} {
  // Logical lead-ins express the derivation, rather than a second copy of its result.
  const lead=/^\s*(\\(?:therefore|because)\b(?:\s|\\quad|\\qquad|\\,|\\;)*)/.exec(calculation??'');
  if(lead){
    const conclusion=conclusionMath(calculation!.slice(lead[0].length),answer);
    return conclusion.calculation
      ? {calculation:lead[1]+conclusion.calculation,result:conclusion.result}
      : {result:lead[1]+conclusion.result};
  }
  const result=emphasizeAnswer(answer);
  if(!calculation)return {result};
  if(normalize(calculation)===normalize(answer))return {result};
  const pieces=splitAt(answer,topLevelTokens(answer).filter(t=>t.kind==='space'));
  const tailIsOnlyUnits=pieces.slice(1).every(p=>/^\[[\s\S]*\]$/.test(p.text));
  const answerRelations=topLevelTokens(pieces[0].text).filter(t=>t.kind==='relation');
  const calculationRelations=topLevelTokens(calculation).filter(t=>t.kind==='relation');
  // Join only uncomplicated equalities with an identical left-hand side.
  // Keep all other derivations intact rather than invent an equality.
  if(tailIsOnlyUnits&&answerRelations.length===1&&calculationRelations.length===1&&
     pieces[0].text[answerRelations[0].start]==='='&&calculation[calculationRelations[0].start]==='='&&
     !/[<>]|\\(?:approx|ne|neq|Longrightarrow|begin)\b/.test(calculation)&&
     !/[<>]|\\(?:approx|ne|neq|Longrightarrow|begin)\b/.test(pieces[0].text)&&
     normalize(calculation.slice(0,calculationRelations[0].start))===normalize(pieces[0].text.slice(0,answerRelations[0].start))){
    const emphasizedRelation=topLevelTokens(result).find(t=>t.kind==='relation')!;
    const relation=calculationRelations[0];
    return {result:'\\begin{aligned}'+calculation.slice(0,relation.start)+'&='+calculation.slice(relation.end)+
      '\\\\&='+result.slice(emphasizedRelation.end)+'\\end{aligned}'};
  }
  return {calculation,result};
}
