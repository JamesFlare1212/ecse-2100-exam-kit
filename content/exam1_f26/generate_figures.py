"""Question and solution drawings owned by exam1_f26."""
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
    p.bounce(ax, [6, -3, 0, 0], 250, 'ns', [(0, 0, '$V_{\\rm in}=6\\,\\mathrm{V}$'), (1, 1, '$V_L=3\\,\\mathrm{V}$'), (0, 2, '$V_{\\rm in}=3\\,\\mathrm{V}$')], ('$\\Gamma_g=0$', '$\\Gamma_L=-0.5$'))
    p.label(ax, 0.5, 2.85, '$V_2^+=V_2^-=0$', ha='center', fontsize=11, color=p.MUTED)
    save(fig, 'bounce-f26', dark)
    fig, ax = plt.subplots(figsize=(7, 2.7))
    x = np.linspace(-1, 0, 500)
    ax.plot(x, np.abs(5 * np.exp(-2j * np.pi * x) + 3 * np.exp(2j * np.pi * x)), color=p.ORANGE, lw=2)
    ax.set_xlabel('$z$ (m)')
    ax.set_ylabel('Voltage envelope (V)')
    ax.set_yticks([2, 5, 8])
    p.tidy(ax)
    fig.tight_layout()
    save(fig, 'standing-damage', dark)
    for name, z, admittance in [('e1-f26-q4', 3 - 1j, False)]:
        fig, ax = plt.subplots(figsize=(5.5, 5.5))
        p.smith(ax, z, admittance)
        save(fig, 'smith-' + name, dark)

    single('e1-f26-q1',q.distributed,(8.5,2.8))
    single('e1-f26-q1-b',lambda ax:q.tl_circuit(ax,r'$R_g=75$',r'$R_L=25$',length='',dc=True,switch=True,voltage='12'))
    fig,axs=plt.subplots(2,1,figsize=(8.6,6.1))
    for ax,damage,caption in [(axs[0],True,'Circuit A'),(axs[1],False,'Circuit B')]:
        q.tl_circuit(ax,r'$R_g=50$',r'$R_L=50$' if damage else r'$Z_{eff}$',r'$Z_0=50$',length='',voltage='10 V\n150 MHz',damage=damage,zeff=not damage)
        q.text(ax,.1,2.99,caption,fontsize=12)
    fig.tight_layout(h_pad=1)
    save(fig,'e1-f26-q2',dark)
    single('e1-f26-q4',q.transformer,(8.9,3.4))
    cases = {'e1-f26-q3-a': lambda ax: q.tl_circuit(ax, '$R_g=50$', '$R_L=50$', '$Z_0=50$', '$L=\\lambda/6$', input_arrow=True), 'e1-f26-q3-b': lambda ax: q.tl_circuit(ax, '$R_g=25$', '$R_L=25$', '$Z_0=50$', '$L=\\lambda/2$', input_arrow=True), 'e1-f26-q3-c': lambda ax: q.tl_circuit(ax, '$R_g=25$', '$R_L=100$', '$Z_0=50$', '$L=\\lambda/4$', input_arrow=True), 'e1-f26-q3-d': lambda ax: q.stub_network(ax, source_circuit=True)}
    for name,draw in cases.items():single(name,draw,(9.0,4.2 if name.endswith(('-c','-d')) else 3.5))
    fig,axs=plt.subplots(2,2,figsize=(14,9))
    for ax,name,label in zip(axs.flat,cases,['a', 'b', 'c', 'd']):
        cases[name](ax);ax.set_title(label,loc='left',fontsize=12)
    fig.tight_layout()
    save(fig,'e1-f26-q3',dark)


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
