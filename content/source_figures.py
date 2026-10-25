"""Exact original image bounds (relative to the PDF page, top-left origin).

Bounds come from PDF image objects, rather than broad crops containing prose.
Each question recreation is checked against these source figures. Multiple
circuits belong beside their own subparts, never in an invented overview.
"""

SOURCE_FIGURES = {
    'e1-f25-q1': (2, [.2525, .2682, .4939, .1612]),
    'e1-f25-q2': (4, [.2153, .2895, .5694, .1751]),
    'e1-f25-q3': (6, [.2262, .1874, .5475, .1685]),
    'e1-f25-q4': (8, [.2721, .1970, .4549, .1848]),
    'e1-s26-q1': (2, [.2558, .1816, .4882, .1481]),
    'e1-s26-q2': (4, [.2608, .1986, .4783, .1225]),
    'e1-s26-q3': (6, [.1176, .3151, .4826, .1318]),
    'e1-s26-q4': (8, [.2665, .1989, .4669, .1758]),
    'e1-f26-q1': (2, [.2803, .1946, .4395, .1211]),
    'e1-f26-q2': (4, [.2030, .1500, .5200, .2800]),
    'e1-f26-q3': (6, [.1471, .2675, .4430, .1659]),
    'e1-f26-q4': (8, [.1626, .1950, .6748, .2125]),
    'e2-f25-q1': (2, [.3818, .2838, .2363, .1653]),
    'e2-f25-q2': (4, [.2537, .2948, .4919, .2022]),
    'e2-f25-q3': (6, [.3635, .1785, .2730, .1690]),
    'e2-f25-q4': (8, [.2882, .1857, .4236, .1777]),
    'e2-s26-q1': (2, [.4631, .1650, .4313, .2034]),
    'e2-s26-q2': (4, [.2716, .2067, .4567, .1883]),
    'e2-s26-q3': (6, [.4977, .1160, .3734, .1911]),
    'e2-s26-q4': (8, [.3316, .1823, .4838, .1780]),
    'e1-s26-q2-template': (4, [.1471, .6781, .2139, .2252]),
    'e1-s26-q3-ai': (6, [.1176, .3151, .4826, .1318]),
    'e1-s26-q3-aii': (6, [.1176, .6345, .5089, .1355]),
    'e1-s26-q3-b': (7, [.1176, .1096, .4713, .1361]),
    'e1-s26-q3-c': (7, [.1176, .4714, .5016, .1735]),
    'e1-f26-q1-b': (3, [.2034, .1280, .5926, .1674]),
    'e1-f26-q3-a': (6, [.1471, .2675, .4430, .1659]),
    'e1-f26-q3-b': (6, [.1471, .6154, .4284, .1674]),
    'e1-f26-q3-c': (7, [.1471, .1284, .4430, .1666]),
    'e1-f26-q3-d': (7, [.1765, .5196, .4686, .1685]),
}

# Separate image crops prevent the paragraph between Circuit A and Circuit B
# from being accidentally included in the original-figure toggle.
SOURCE_PANELS = {
    'e1-f26-q2': [[.2030,.1500,.5200,.1330],[.2030,.3140,.5200,.1170]]
}


def figure_source(name):
    doc = name[:6]
    page, region = SOURCE_FIGURES[name]
    # A small margin preserves strokes exactly on the image object's boundary.
    x, y, w, h = region
    return dict(doc=doc, page=page, region=[max(0,x-.002), max(0,y-.002), w+.004, h+.004])


def apply_source_figures(exams):
    problems = {q['id']: q for e in exams for q in e['problems']}
    caption = dict(zh='复刻原卷插图，保留原图的视角、结构与标注。',
                   en='Recreated from the exam figure, preserving its perspective, geometry and labels.')
    for q in problems.values():
        q['originalFigure'] = figure_source(q['id'])
        q['figureCaption'] = caption.copy()

    def part_figure(qid, index, name):
        problems[qid]['parts'][index]['questionFigure'] = dict(
            name=name, source=figure_source(name), caption=caption.copy())

    for qid, names in {
        'e1-s26-q3': ['ai','aii','b','c'],
        'e1-f26-q3': ['a','b','c','d'],
    }.items():
        problems[qid]['figureAtParts'] = True
        for index, name in enumerate(names):
            part_figure(qid, index, f'{qid}-{name}')
    part_figure('e1-f26-q1', 3, 'e1-f26-q1-b')
    part_figure('e1-s26-q2', 1, 'e1-s26-q2-template')

    # Annotated Smith charts are solutions, not part of the supplied question.
    for qid in ['e1-f25-q4','e1-s26-q4','e1-f26-q4']:
        problems[qid]['parts'][2]['figure'] = f'smith-{qid}'
