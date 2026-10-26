"""Question and solution drawings owned by exam1_s26."""
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

    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    p.bounce(ax, [6.25, 3.125, -0.78125, -0.390625], 50, 'ps', [(0, 0, '$V_{\\rm in}=6.25\\,\\mathrm{V}$'), (1, 1, '$V_L=9.375\\,\\mathrm{V}$'), (0, 2, '$V_{\\rm in}=8.59375\\,\\mathrm{V}$'), (1, 3, '$V_L=8.203125\\,\\mathrm{V}$')], ('$\\Gamma_g=-0.25$', '$\\Gamma_L=0.5$'))
    save(fig, 'bounce-s26', dark)
    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    p.loadsteps(ax, [0, 50, 150, 200], [0, 9.375, 8.203125, 8.203125], '$t$ (ps)')
    save(fig, 'load-step-s26', dark)
    for name, z, admittance in [('e1-s26-q4', 0.5 + 1.8j, True)]:
        fig, ax = plt.subplots(figsize=(5.5, 5.5))
        p.smith(ax, z, admittance)
        save(fig, 'smith-' + name, dark)

    single('e1-s26-q1',lambda ax:q.tl_circuit(ax,r'$R_g=25\Omega$',r'$Z_L=50\Omega$',vin=True))
    single('e1-s26-q2',lambda ax:q.tl_circuit(ax,r'$R_g=30\Omega$',r'$Z_L=150\Omega$',r'$Z_0=50\Omega$',dc=True,switch=True,voltage='10 V'))
    single('e1-s26-q4',lambda ax:q.stub_network(ax,spring=True),(8.8,4.0))
    single('e1-s26-q2-template',q.bounce_template,(3.7,4.7))
    cases = {'e1-s26-q3-ai': lambda ax: q.tl_circuit(ax, '$R_g=100\\Omega$', '$Z_L=100\\Omega$'), 'e1-s26-q3-aii': lambda ax: q.tl_circuit(ax, '$R_g=50\\Omega$', '$Z_L=12.5\\Omega$'), 'e1-s26-q3-b': lambda ax: q.tl_circuit(ax, '$R_g=50\\Omega$', '$R_L=50\\Omega$', '$Z_0=50\\Omega$', '$L=\\lambda/4$', capacitor=True, input_arrow=True), 'e1-s26-q3-c': lambda ax: q.stub_network(ax, source_circuit=True, spring_c=True)}
    for name,draw in cases.items():single(name,draw,(9.0,4.2 if name.endswith(('-c','-d')) else 3.5))
    fig,axs=plt.subplots(2,2,figsize=(14,9))
    for ax,name,label in zip(axs.flat,cases,['a(i)', 'a(ii)', 'b', 'c']):
        cases[name](ax);ax.set_title(label,loc='left',fontsize=12)
    fig.tight_layout()
    save(fig,'e1-s26-q3',dark)


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
