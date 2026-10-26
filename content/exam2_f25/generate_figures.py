"""Question and solution drawings owned by exam2_f25."""
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

    for selected, name in enumerate(['sphere-inner', 'sphere-middle', 'sphere-outer']):
        fig, ax = plt.subplots(figsize=(7.2, 5.5))
        p.sphere(ax, selected)
        save(fig, name, dark)

    single('e2-f25-q1',q.sphere_question,(5.8,4.7))
    single('e2-f25-q2',q.plates,(8.3,4.0))
    # Same world geometry as a cylinder; the source omits the far end cap.
    coax = dict(view=(.28,.86,-.43), radii=(.34,1.65), length=5.0, radius_angles=(.30,.75))
    single('e2-f25-q3',lambda ax:q.coax_perspective(ax,leaky=False,**coax),(7.5,4.6))
    single('e2-f25-q4',q.charged_spheres,(8.1,4.1))


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
