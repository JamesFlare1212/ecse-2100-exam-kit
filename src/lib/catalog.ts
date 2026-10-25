import examData from './data/exams.json';
import formulaData from './data/formulas.json';
import documentData from './data/documents.json';
import type { Exam, Formula, Problem, SourceDocument, Localized } from './types';

export const exams = examData as unknown as Exam[];
export const formulas = formulaData as unknown as Formula[];
export const documents = documentData as unknown as Record<string, SourceDocument>;
export const formulaById = Object.fromEntries(formulas.map(f => [f.id, f]));
export const problemEntries = exams.flatMap(exam => exam.problems.map(problem => ({ exam, problem })));
export const partIds = new Set(problemEntries.flatMap(({problem}) => problem.parts.map(p => p.id)));
export const problemIds = new Set(problemEntries.map(({problem}) => problem.id));
export const totalParts = partIds.size;
export function findProblem(id: string) {
  return problemEntries.find(p => p.problem.id === id) ?? problemEntries.find(p => p.problem.id === 'e2-s26-q3')!;
}
export function problemFormulas(problem: Problem) {
  const ids = [...new Set(problem.parts.flatMap(p => p.steps.flatMap(s => s.refs)))];
  return ids.map(id => formulaById[id]).filter(Boolean);
}
export const lectureTitles: Record<number, Localized> = {
  1: {zh:'电磁学导论',en:'Introduction to electromagnetics'},
  2: {zh:'传输线模型与波动方程',en:'Line models & wave equations'},
  3: {zh:'反射、驻波与输入阻抗',en:'Reflections, standing waves & impedance'},
  4: {zh:'瞬态分析与反弹图',en:'Transient analysis & bounce diagrams'},
  5: {zh:'功率与有损传输线',en:'Power & lossy transmission lines'},
  6: {zh:'阻抗匹配与 Smith 图',en:'Impedance matching & Smith charts'},
  7: {zh:'传输线支节匹配',en:'Matching with transmission-line stubs'},
  8: {zh:'场论数学 I：坐标与积分',en:'Field math I: coordinates & integrals'},
  9: {zh:'场论数学 II：矢量算符',en:'Field math II: vector operators'},
  10: {zh:'高斯定律',en:'Gauss’s law'},
  11: {zh:'电势与电介质',en:'Electric potential & materials'},
  12: {zh:'电边界条件与电容',en:'Electric boundary conditions & capacitance'},
  13: {zh:'Laplace、Poisson 与数值法',en:'Laplace, Poisson & numerical methods'},
  14: {zh:'电流与电阻',en:'Current & resistance'},
  15: {zh:'静磁场与安培定律',en:'Magnetostatics & Ampère’s law'}
};
