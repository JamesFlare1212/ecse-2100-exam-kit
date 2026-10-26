export type Locale = 'zh' | 'en';
export type Localized = Record<Locale, string>;
export type Region = [number, number, number, number];
export interface SourceRef { doc: string; page: number; label: Localized; region?: Region }
export interface Formula {
  id: string;
  title: Localized;
  math: string;
  source: SourceRef;
  note?: Localized;
}
export interface Step { text: Localized; math?: string; refs: string[] }
export interface OriginalFigure { doc:string; page:number; region:Region }
export interface ProblemGuide {
  concept: Localized;
  known: Localized;
  goal: Localized;
  approach: Localized;
}
export interface Part {
  id: string;
  label: string;
  points: number;
  prompt: Localized;
  steps: Step[];
  answer: string;
  answerText?: Localized;
  note?: Localized;
  figure?: string;
  figureCaption?: Localized;
  spatialFigure?: string;
  questionFigure?: { name:string; source:OriginalFigure; caption:Localized };
  sourcePage: number;
  solutionPage: number;
}
export interface Problem {
  wording: 'original';
  id: string;
  number: number;
  title: Localized;
  topic: Localized;
  statement: Localized;
  givens: string[];
  points: number;
  figure: string;
  figureAtParts?: boolean;
  figureCaption: Localized;
  originalFigure: OriginalFigure;
  lectures: SourceRef[];
  guide: ProblemGuide;
  parts: Part[];
  note?: Localized;
}
export interface Exam {
  id: string;
  number: number;
  term: Localized;
  year: number;
  points: number;
  doc: string;
  solutionDoc: string;
  questionsOnly: boolean;
  problems: Problem[];
}
export type ExamInfo = Omit<Exam, 'problems'>;
/** Search/navigation data deliberately excludes guides, worked steps and answers. */
export type ProblemIndex = Pick<Problem, 'id' | 'number' | 'title' | 'topic' | 'statement'> & {
  parts: Pick<Part, 'id' | 'prompt'>[];
};
export type ExamIndex = ExamInfo & { problems: ProblemIndex[] };
export interface SourceDocument {
  id: string; title: string; kind: string; pages: number; pdf: string;
  pageBase: string; sizes: number[][]; original: string; sha256: string;
}
