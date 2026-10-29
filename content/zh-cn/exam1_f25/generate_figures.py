"""Question and solution drawings owned by exam1_f25."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import matplotlib.pyplot as plt
import numpy as np
import plotting as p
import question_primitives as q

SVG_LABELS = {'Source': '源端', 'Load': '负载', 'Admittance Smith chart': '导纳 Smith 圆图'}


def render_figures(save, dark):
    p.setup(dark)
    q.setup((p.INK, p.PAPER, p.MUTED, p.TEAL, p.ORANGE), dark)
    def single(name, draw, size=(8.6, 3.5)):
        fig, ax = plt.subplots(figsize=size)
        draw(ax)
        save(fig, name, dark)

    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    p.bounce(ax, [1, 0.6, 0.2, 0.12], 10, 'ns', [(0, 0, '$V_{\\rm in}=1.00\\,\\mathrm{V}$'), (1, 1, '$V_L=1.60\\,\\mathrm{V}$'), (0, 2, '$V_{\\rm in}=0.80\\,\\mathrm{V}$'), (1, 3, '$V_L=0.32\\,\\mathrm{V}$')], ('$\\Gamma_g=1/3$', '$\\Gamma_L=0.6$'))
    save(fig, 'bounce-f25', dark)
    for name, z, admittance in [('e1-f25-q4', 2 + 1j, True)]:
        fig, ax = plt.subplots(figsize=(5.5, 5.5))
        p.smith(ax, z, admittance)
        save(fig, 'smith-' + name, dark)

    for name,rg,load,detail,voltage,pulse in [
        ('e1-f25-q1','75','75',r'$Z_0=75$','1 V\n\n250 MHz',False),
        ('e1-f25-q2','100','200',r'$T_d=10\mathrm{n}$','3 V',True),
        ('e1-f25-q3','50','125',r'$Z_0=50$','10 V',False),
    ]:
        symbol=r'$R_1$' if name=='e1-f25-q3' else r'$R_L$'
        single(name,lambda ax,rg=rg,load=load,detail=detail,voltage=voltage,pulse=pulse,symbol=symbol:q.t1_circuit(ax,rg,load,detail,voltage,pulse,symbol))
    single('e1-f25-q4',lambda ax:q.stub_network(ax), (8.8,4.0))


if __name__ == '__main__':
    from generate_figures import generate_paper
    generate_paper(Path(__file__).resolve().parent)
