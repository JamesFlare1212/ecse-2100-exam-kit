"""Render and inspect the actual figure generators without changing static assets."""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from matplotlib.text import Text
import generate_figures as figures


def review(output):
    output.mkdir(parents=True, exist_ok=True)
    results = []

    def inspect(fig, name, dark):
        figures.prepare_figure(fig)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        collisions, strokes = [], []
        for ax in fig.axes:
            labels = [text for text in ax.texts if text.get_text() and text.get_visible()]
            # Use Text's box: Annotation's own box also includes its leader arrow.
            boxes = [(text, Text.get_window_extent(text, renderer).padded(1)) for text in labels]
            for (a, first), (b, second) in itertools.combinations(boxes, 2):
                if first.overlaps(second):
                    collisions.append([a.get_text(), b.get_text()])
            if name.startswith('sphere-'):
                patches = {patch.get_gid(): patch for patch in ax.patches if patch.get_gid()}
                for key in ['a', 'b', 'R']:
                    boundary = patches['sphere-boundary-' + key]
                    start, end = map(np.array, patches['sphere-radius-' + key]._posA_posB)
                    assert np.allclose(start, boundary.center), (name, key, 'different centers')
                    assert math.isclose(np.linalg.norm(end-start), boundary.radius, abs_tol=1e-12), (name, key, 'radius endpoint')
                start, end = map(np.array, patches['sphere-outward-normal']._posA_posB)
                assert math.isclose(np.linalg.norm(start), patches['sphere-boundary-R'].radius, abs_tol=1e-12), (name, 'normal must start on Gaussian surface')
                assert np.dot(start, end-start) > 0, (name, 'normal must point outward')
                assert abs(start[0]*end[1]-start[1]*end[0]) < 1e-12, (name, 'normal must be radial')
                for label, box in boxes:
                    for patch in ax.patches:
                        path = patch.get_path().transformed(patch.get_transform())
                        if box.overlaps(path.get_extents()) and path.intersects_bbox(box, filled=False):
                            strokes.append([label.get_text(), patch.get_gid()])
                    for line in ax.lines:
                        path = line.get_path().transformed(line.get_transform())
                        if box.overlaps(path.get_extents()) and path.intersects_bbox(box, filled=False):
                            strokes.append([label.get_text(), 'leader'])
        key = name + ('-dark' if dark else '')
        fig.savefig(output/(key+'.png'), bbox_inches='tight', pad_inches=.16, dpi=140)
        results.append({'name': key, 'textCollisions': collisions, 'strokeCollisions': strokes})
        figures.plt.close(fig)

    original_save = figures.save
    try:
        figures.save = inspect
        for dark in [False, True]:
            figures.setup(dark)
            figures.solution_figures(dark)
            colors = (figures.INK, figures.PAPER, figures.MUTED, figures.TEAL, figures.ORANGE)
            figures.render_question_figures(inspect, dark, colors)
    finally:
        figures.save = original_save
    (output/'report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    failures = [item for item in results if item['textCollisions'] or item['strokeCollisions']]
    for item in failures:
        print(json.dumps(item, ensure_ascii=False))
    assert not failures, f'{len(failures)} figure/theme pairs have overlapping annotations'
    print(f'Checked {len(results)} figure/theme pairs: no text overlaps; spherical radii, normals and label clearance verified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=figures.ROOT/'artifacts/figure-review')
    review(parser.parse_args().output)
