"""Question and solution drawings owned by exam2_s26."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import matplotlib.pyplot as plt
import numpy as np
import plotting as p
import question_primitives as q

SVG_LABELS = {'Real charges': '真实电荷', 'Image system only': '仅用于构造镜像'}


def render_figures(save, dark):
    p.setup(dark)
    q.setup((p.INK, p.PAPER, p.MUTED, p.TEAL, p.ORANGE), dark)
    def single(name, draw, size=(8.6, 3.5)):
        fig, ax = plt.subplots(figsize=size)
        draw(ax)
        save(fig, name, dark)

    for name, stream in [('images-geometry', False), ('images-fieldlines', True)]:
        fig, ax = plt.subplots(figsize=(6.7, 4.3))
        p.images(ax, stream)
        save(fig, name, dark)

    strip = dict(view=(.72,.48,.50), width=2.6, length=3.7, height=.72)
    coax = dict(view=(.35,.80,-.49), radii=(.52,1.65), length=5.0, radius_angles=(-.24,.75))
    single('e2-s26-q1',lambda ax:q.microstrip(ax,**strip),(8.0,5.0))
    single('e2-s26-q2',q.boundaries,(8.0,4.4))
    single('e2-s26-q3',lambda ax:q.coax_perspective(ax,**coax),(8.0,5.0))
    single('e2-s26-q4',q.conducting_plane,(8.3,4.5))
    single('leaky-gauss',lambda ax:q.coax_perspective(ax,gaussian=True,**coax),(8.0,5.0))


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
