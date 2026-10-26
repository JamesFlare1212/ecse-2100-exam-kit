"""Question and solution drawings owned by exam2_s26."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import matplotlib.pyplot as plt
import numpy as np
import plotting as p
import question_primitives as q


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

    single('e2-s26-q1',q.microstrip,(8.0,5.0))
    single('e2-s26-q2',q.boundaries,(8.0,4.4))
    single('e2-s26-q3',q.coax_perspective,(8.0,5.0))
    single('e2-s26-q4',q.conducting_plane,(8.3,4.5))
    single('leaky-gauss',lambda ax:q.coax_perspective(ax,gaussian=True),(8.0,5.0))


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
