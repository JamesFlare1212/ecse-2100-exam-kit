import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const text = z.string().min(1);
const localized = z.object({ en: text, zh: text }).strict();
const positive = z.number().int().positive();
const points = z.number().int().nonnegative();
const region = z.tuple([z.number(), z.number(), z.number(), z.number()]);
const originalFigure = z.object({ doc: text, page: positive, region }).strict();
const source = z.object({ doc: text, page: positive, label: localized, region: region.optional() }).strict();

const questions = defineCollection({
  loader: glob({
    base: './content',
    pattern: 'exam*_[fs][0-9][0-9]/questions/*.md',
    generateId: ({ data }) => String(data.id),
    // The study renderer consumes the bilingual body as structured sections.
    // Avoid also compiling a second, unused copy of every solution to HTML.
    retainBody: true,
    deferRender: true,
  }),
  schema: z.object({
    id: text, number: positive, title: localized, topic: localized,
    wording: z.literal('original'), givens: z.array(text), points,
    figure: text, figureCaption: localized, originalFigure,
    figureAtParts: z.boolean().optional(), lectures: z.array(source).min(1),
    parts: z.array(z.object({
      id: text, label: text, points, sourcePage: positive, solutionPage: positive,
      figure: text.optional(), figureCaption: localized.optional(),
      questionFigure: z.object({ name: text, source: originalFigure, caption: localized }).strict().optional(),
    }).strict()).min(1),
  }).strict(),
});

export const collections = { questions };
