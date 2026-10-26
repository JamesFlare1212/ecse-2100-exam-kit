import formulaData from '../../content/formulas.json';
import type { ExamIndex, Formula, Problem, SourceDocument, Localized } from './types';
import { DEFAULT_PROBLEM_ID } from './problem-navigation';

export const formulas = formulaData as Formula[];
export const formulaById = Object.fromEntries(formulas.map(f => [f.id, f]));
export function createCatalog(exams: ExamIndex[], documents: Record<string, SourceDocument>) {
  const problemEntries = exams.flatMap(exam => exam.problems.map(problem => ({ exam, problem })));
  const partIds = new Set(problemEntries.flatMap(({problem}) => problem.parts.map(p => p.id)));
  const problemIds = new Set(problemEntries.map(({problem}) => problem.id));
  const findProblem = (id: string) => problemEntries.find(p => p.problem.id === id)
    ?? problemEntries.find(p => p.problem.id === DEFAULT_PROBLEM_ID) ?? problemEntries[0];
  return { exams, documents, problemEntries, partIds, problemIds, totalParts: partIds.size, findProblem };
}
export type Catalog = ReturnType<typeof createCatalog>;
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
