"""Authored formula index; rectangles are normalized PDF coordinates (x,y,w,h)."""
import json
from pathlib import Path
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def L(zh, en): return {'zh': zh, 'en': en}
items = []
def F(id, zh, en, math, page, region, note=None, doc='crib'):
    items.append({'id': id, 'title': L(zh,en), 'math': math, 'source': {'doc':doc, 'page':page, 'region':region, 'label': L(f'原始公式表 · 第 {page} 页' if doc=='crib' else f'Lecture 04 · 第 {page} 页', f'Original crib · p. {page}' if doc=='crib' else f'Lecture 04 · p. {page}')}, **({'note':note} if note else {})})

F('wave','波长与相位常数','Wavelength & phase constant',r'\beta=\frac{\omega}{u},\qquad \lambda=\frac{2\pi}{\beta}=\frac{u}{f}',1,[.12,.185,.76,.075])
F('velocity','波速','Wave velocity',r'u=\frac{1}{\sqrt{lc}}=\mathrm{vf}\,u_c',1,[.50,.539,.38,.072])
F('impedance','无损线特性阻抗','Characteristic impedance',r'Z_0=\frac{V_0^+}{I_0^+}=-\frac{V_0^-}{I_0^-}=\sqrt{\frac{l}{c}}',1,[.12,.456,.38,.080])
F('reflection','反射系数','Reflection coefficient',r'\Gamma_L=\frac{V_0^-}{V_0^+}=\frac{Z_L-Z_0}{Z_L+Z_0}',1,[.50,.456,.38,.080],L('在负载参考面使用 ΓL；其他参考面需包含传播相位。','Use ΓL at the load reference plane; include propagation phase at other planes.'))
F('phasor','电压行波相量','Traveling-wave voltage',r'\widetilde V(z)=V^+e^{-j\beta z}+V^-e^{j\beta z}',1,[.50,.353,.38,.101])
F('swr','电压驻波比','Voltage standing-wave ratio',r'\mathrm{SWR}=\frac{|V_0^+|+|V_0^-|}{|V_0^+|-|V_0^-|}=\frac{1+|\Gamma|}{1-|\Gamma|}',1,[.12,.539,.38,.072])
F('zin','传输线输入阻抗','Line input impedance',r'Z_{\mathrm{in}}=Z_0\frac{Z_L+jZ_0\tan(\beta L)}{Z_0+jZ_L\tan(\beta L)}',1,[.12,.613,.38,.073])
F('power','时间平均功率','Time-average power',r'P_{\mathrm{av}}=\frac{|V_0^+|^2}{2Z_0}(1-|\Gamma|^2)',1,[.50,.613,.38,.073])
F('open','开路传输线','Open-circuited line',r'Z_{\mathrm{in}}=-jZ_0\cot(\beta L)',1,[.12,.687,.38,.049])
F('half','半波线重复负载','Half-wave impedance repeat',r'L=\frac{\lambda}{2}\;\Longrightarrow\;Z_{\mathrm{in}}=Z_L',1,[.12,.737,.38,.075])
F('quarter','四分之一波长变换','Quarter-wave transformation',r'L=\frac{\lambda}{4}\;\Longrightarrow\;Z_{\mathrm{in}}=\frac{Z_0^2}{Z_L}',1,[.50,.737,.38,.075])
F('attenuation','低损耗衰减','Low-loss attenuation',r'\alpha=\frac{r}{2Z_0}',2,[.50,.300,.38,.070],L('原表的简化式采用可忽略的并联漏电导 g；一般低损耗式还含 gZ₀/2。','The crib simplification assumes negligible shunt conductance g; the general low-loss expression also includes gZ₀/2.'))
F('lossy-wave','有损线行波','Lossy traveling wave',r'\widetilde V(z)=V^+e^{-\gamma z}+V^-e^{\gamma z},\qquad\gamma=\alpha+j\beta',2,[.12,.115,.76,.090])
F('bounce','初始入射波与时延','Launched wave & transit time',r'V_1^+=V_g\frac{Z_0}{Z_g+Z_0},\qquad T=\frac{d}{u}',31,[.10,.63,.73,.36],L('公式表第 2 页给出反弹图；初始分压公式直接引用 Lecture 04 的原式。','Crib p. 2 contains the bounce diagram; this launch equation is quoted directly from Lecture 04.'),doc='lecture-04')
F('geometry','柱、球坐标体积元','Cylindrical & spherical volume elements',r'd\mathcal V=r\,dr\,d\phi\,dz\quad\text{or}\quad r^2\sin\theta\,dr\,d\theta\,d\phi',3,[.045,.532,.93,.054])
F('gauss','高斯定律','Gauss’s law',r'\oiint\mathbf D\cdot d\mathbf S=\iiint\rho\,d\mathcal V=Q_{\mathrm{enc}}',4,[.12,.509,.76,.033])
F('constitutive','电位移与电场','Electric displacement',r'\mathbf D=\epsilon\mathbf E',4,[.12,.568,.76,.027])
F('conservative','静电场无旋','Conservative electrostatic field',r'\oint\mathbf E\cdot d\mathbf l=0,\qquad\nabla\times\mathbf E=0',4,[.12,.540,.76,.029])
F('coulomb','点电荷电场与力','Coulomb’s law',r'\mathbf E=\frac{q}{4\pi\epsilon r^2}\,\hat{\mathbf r},\qquad\mathbf F_{12}=\frac{q_1q_2}{4\pi\epsilon r^2}\,\hat{\mathbf r}',4,[.12,.624,.76,.075])
F('potential','电势差','Potential difference',r'V(b)-V(a)=-\int_a^b\mathbf E\cdot d\mathbf l',4,[.50,.724,.38,.057])
F('gradient','由电势求电场','Electric field from potential',r'\mathbf E=-\nabla V',4,[.12,.724,.38,.057])
F('boundary','静电边界条件','Electrostatic boundary conditions',r'D_{1n}-D_{2n}=\rho_s,\qquad E_{1t}=E_{2t}',5,[.12,.090,.76,.142],L('沿用原表法向 n₂₁，从材料 2 指向材料 1。无自由面电荷时 D₁ₙ=D₂ₙ。','The original normal n₂₁ points from material 2 to material 1. With no free surface charge, D₁ₙ=D₂ₙ.'))
F('capacitance','电容定义','Capacitance',r'C=\frac{Q}{V}',5,[.12,.280,.38,.065],L('固定空间电荷存在时采用小信号定义 dQ/dV，见 S26 Exam 2 第 3(d) 小问。','With fixed space charge, use differential capacitance dQ/dV; see S26 Exam 2, 3(d).'))
F('energy','电场能量','Electric field energy',r'W_e=\frac12\iiint\epsilon|\mathbf E|^2\,d\mathcal V=\frac12 CV^2',5,[.12,.346,.76,.066])
F('laplace','拉普拉斯方程','Laplace’s equation',r'\nabla^2 V=0',5,[.12,.459,.38,.058])
F('poisson','泊松方程','Poisson’s equation',r'\nabla^2 V=-\frac{\rho}{\epsilon}',5,[.50,.459,.38,.058])
F('ohm','微观欧姆定律','Microscopic Ohm’s law',r'\mathbf J=\sigma\mathbf E',5,[.12,.630,.38,.067])
F('resistance','电阻定义','Resistance',r'R=\frac{V}{I}',5,[.50,.630,.38,.067])
F('current','电流密度的通量','Current-density flux',r'I_c=\iint\mathbf J_c\cdot d\mathbf S=\iint\sigma\mathbf E\cdot d\mathbf S',7,[.12,.712,.38,.075])

out=ROOT/'static/excerpts'; out.mkdir(exist_ok=True, parents=True)
for item in items:
    s=item['source']; doc=pymupdf.open(ROOT/f'static/sources/{s["doc"]}.pdf'); page=doc[s['page']-1]
    x,y,w,h=s['region']; r=page.rect; crop=pymupdf.Rect(x*r.width,y*r.height,(x+w)*r.width,(y+h)*r.height)
    pix=page.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=crop,alpha=False)
    Image.frombytes('RGB',(pix.width,pix.height),pix.samples).save(out/f'{item["id"]}.webp','WEBP',quality=92)
(ROOT/'src/lib/data/formulas.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print(f'{len(items)} formulas and source excerpts indexed.')
