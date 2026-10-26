import { examIndex, documents } from '#lib/catalog.server';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = () => ({ examIndex, documents });
