"""Exam 1: Fall 2025 and Spring 2026; Fall 2026 is in exam1_f26.py."""
def create(L,S,P,R,Q,E):
    f='e1-f25'; s='e1-s26'
    linelect=[R(2,39,'特性阻抗与波速','Characteristic impedance and speed'),R(5,32,'低损耗衰减','Low-loss attenuation')]
    cable=Q(f,1,'有线电视的传输线连接','A cable television connection',('传输线基础 · 衰减','Transmission lines · attenuation'),
      ('用一根长 30 m、特性阻抗 75 Ω、速度因子 0.85 的同轴线连接信号源与电视。信号源幅度 1 V，源电阻与电视负载均为 75 Ω，频率为 250 MHz。',
       'Connect a source to a television using a 30 m coaxial cable with characteristic impedance 75 Ω and velocity factor 0.85. The source amplitude is 1 V, source and load resistances are both 75 Ω, and frequency is 250 MHz.'),
      [r'L=30\,\mathrm m',r'Z_0=R_g=R_L=75\,\Omega',r'\mathrm{vf}=0.85',r'f=250\,\mathrm{MHz}'],10,2,[.20,.27,.60,.22],linelect,[
        P('a',2,'负载处是否存在反射？解释原因。','Will the load reflect the wave? Explain.',[
          S('先写原表的负载反射系数，比较的是负载阻抗和线的特性阻抗。', 'Begin with the crib load reflection coefficient, comparing load impedance with line characteristic impedance.', '\\Gamma_L=\\frac{Z_L-Z_0}{Z_L+Z_0}', ['reflection']),
          S('本题电视负载与电缆均为 75 Ω，逐项代入分子和分母。', 'Both the television load and cable are 75 Ω. Substitute them into numerator and denominator.', '\\Gamma_L=\\frac{75\\,\\Omega-75\\,\\Omega}{75\\,\\Omega+75\\,\\Omega}=\\frac0{150\\,\\Omega}=0', []),
          S('反射电压幅度等于入射幅度乘 ΓL，因此不存在由负载产生的反向波。', 'The reflected voltage amplitude is the incident amplitude times ΓL, so the load produces no backward wave.', 'V_0^-=\\Gamma_LV_0^+=0', []),
          S('结论是负载匹配、无反射；源阻抗相同也避免源端失配。', 'The load is matched with no reflection; the equal source impedance also avoids source mismatch.', '\\Gamma_L=0', [])],r'\Gamma_L=0',2,answerText=L('无反射。','There is no reflection.')),
        P('b',2,'求同轴线的单程时延。','Find the one-way transit time.',[
          S('先写波速和传播时间的关系，速度因子是相对真空光速的比值。', 'Begin with the wave-speed and propagation-time relations; velocity factor is relative to vacuum light speed.', 'u=\\mathrm{vf}\\,u_c,\\qquad T_d=\\frac Lu', ['velocity', 'bounce']),
          S('将 0.85 和 3×10⁸ m/s 代入，先得到电缆内的实际传播速度。', 'Substitute 0.85 and 3×10⁸ m/s to obtain the cable propagation speed first.', 'u=0.85(3.00\\times10^8\\,\\mathrm{m/s})=2.55\\times10^8\\,\\mathrm{m/s}', []),
          S('长度除以波速，米约去后结果为秒。', 'Divide length by speed; meters cancel, leaving seconds.', 'T_d=\\frac{30\\,\\mathrm m}{2.55\\times10^8\\,\\mathrm{m/s}}=1.17647\\times10^{-7}\\,\\mathrm s', []),
          S('利用 1 ns=10⁻⁹ s 转换单位；这是单程时间，不再乘 2。', 'Convert using 1 ns=10⁻⁹ s. This is one-way time, so do not multiply by two.', 'T_d=117.65\\,\\mathrm{ns}', [])],r'T_d=117.65\,\mathrm{ns}',2),
        P('c',2,'求电缆内信号波长。','Find the wavelength on the cable.',[
          S('先写原表的波长关系，使用电缆内部波速。', 'Begin with the crib wavelength relation, using the cable wave speed.', '\\lambda=\\frac uf,\\qquad u=\\mathrm{vf}\\,u_c', ['wave', 'velocity']),
          S('把频率由 MHz 换成 Hz，并写出上问得到的波速。', 'Convert MHz to Hz and state the previously determined speed.', 'f=250\\times10^6\\,\\mathrm{Hz},\\qquad u=2.55\\times10^8\\,\\mathrm{m/s}', []),
          S('将数值及单位代入波长公式。', 'Substitute numerical values and units into the wavelength equation.', '\\lambda=\\frac{2.55\\times10^8\\,\\mathrm{m/s}}{250\\times10^6\\,\\mathrm{s^{-1}}}=\\frac{2.55}{2.50}\\,\\mathrm m', []),
          S('化简得到电缆内波长，而非真空中的 1.20 m。', 'Simplify to the cable wavelength, rather than the vacuum wavelength of 1.20 m.', '\\lambda=1.02\\,\\mathrm m', [])],r'\lambda=1.02\,\mathrm m',3,2),
        P('d',3,r'若低损耗电缆串联电阻 $r=1\,\Omega/\mathrm m$，求负载处的入射电压幅度。',r'For low-loss series resistance $r=1\,\Omega/\mathrm m$, find the incident voltage amplitude at the load.',[
          S('先写原表的低损耗衰减式与行波包络；本题使用可忽略并联漏电导的模型。', 'Begin with the crib low-loss attenuation and traveling-wave envelope, using the model with negligible shunt conductance.', '\\alpha=\\frac r{2Z_0},\\qquad |V^+(z)|=|V_0^+|e^{-\\alpha z}', ['attenuation', 'lossy-wave']),
          S('代入每单位长度电阻和特性阻抗，求出 α。', 'Substitute resistance per length and characteristic impedance to calculate α.', '\\alpha=\\frac{1\\,\\Omega/\\mathrm m}{2(75\\,\\Omega)}=\\frac1{150}\\,\\mathrm{m^{-1}}=6.66667\\times10^{-3}\\,\\mathrm{Np/m}', []),
          S('负载入射波的起始幅度不是源电压 1 V，必须先做源端分压。', 'The launched amplitude is not the 1 V source voltage; apply the source divider first.', 'V_0^+=V_g\\frac{Z_0}{R_g+Z_0}=(1\\,\\mathrm V)\\frac{75\\,\\Omega}{75\\,\\Omega+75\\,\\Omega}=0.500\\,\\mathrm V', ['bounce']),
          S('传播到 30 m，衰减指数 αL 是无量纲的 0.2。', 'At 30 m, the attenuation exponent αL is dimensionless and equals 0.2.', '\\alpha L=\\frac1{150\\,\\mathrm m}(30\\,\\mathrm m)=0.2,\\qquad |V^+(L)|=(0.500\\,\\mathrm V)e^{-0.2}', []),
          S('求指数值得到负载处的入射电压幅度；ΓL=0，所以没有额外反射项。', 'Evaluate the exponential to obtain the incident load amplitude. Since ΓL=0, there is no additional reflected term.', '|V^+(30\\,\\mathrm m)|=0.5e^{-0.2}=0.4094\\,\\mathrm V', [])],r'|V^+(30\,\mathrm m)|=0.5e^{-0.2}=0.4094\,\mathrm V',3,2),
        P('e',1,'若改用 50 Ω 电缆，满足最大功率传输的最短非零长度是多少？','With 50 Ω cable, what is the shortest nonzero length for maximum power transfer?',[
          S('最大功率传输要求源看到的输入阻抗与 75 Ω 源电阻匹配；按原题采用无损匹配近似。', 'Maximum power transfer requires the input seen by the source to match its 75 Ω resistance. Use the source’s lossless matching approximation.', 'Z_{\\mathrm{in}}=R_g=75\\,\\Omega', []),
          S('原表的半波线性质会将负载原样重复到输入端，不论中间电缆是否为 50 Ω。', 'The crib half-wave property repeats the load at the input even with a 50 Ω cable in between.', 'L=n\\frac{\\lambda}{2}\\quad\\Longrightarrow\\quad Z_{\\mathrm{in}}=Z_L=75\\,\\Omega', ['half']),
          S('核对最短正长度：代入通用输入阻抗并令 Zin=ZL，因 Z₀≠ZL，只能使 tan(βL)=0。', 'Check the shortest positive length: setting Zin=ZL in the general equation with Z₀≠ZL requires tan(βL)=0.', 'j(Z_0^2-Z_L^2)\\tan(\\beta L)=0\\quad\\Longrightarrow\\quad\\beta L=n\\pi', ['zin']),
          S('沿用同一速度因子与频率，波长仍为 1.02 m，n 取最小正整数 1。', 'The unchanged velocity factor and frequency give λ=1.02 m. Choose the smallest positive integer n=1.', 'L_{\\min}=\\frac{\\lambda}{2}=\\frac{1.02\\,\\mathrm m}{2}', []),
          S('这是重复阻抗的半波长度，不是把 75 Ω 变换成另一电阻的四分之一波长。', 'This is the half-wave impedance-repeat length.', 'L_{\\min}=0.510\\,\\mathrm m', [])],r'L_{\min}=0.510\,\mathrm m',3)
      ])
    qubit=Q(f,2,'短脉冲与超导量子比特','Short pulses & superconducting qubits',('反弹图 · 有限脉冲','Bounce diagrams · finite pulses'),
      (r'传输线 $l=400\,\mathrm{nH/m}$、$c=160\,\mathrm{pF/m}$、单程时延 10 ns。源在 t=0 发出幅度 3 V、持续 1 ns 的单个矩形脉冲。损坏后源电阻 100 Ω，负载 200 Ω。',
       r'A line has $l=400\,\mathrm{nH/m}$, $c=160\,\mathrm{pF/m}$ and one-way delay 10 ns. At t=0 the source emits a single 3 V rectangular pulse lasting 1 ns. After damage, source and load resistances are 100 Ω and 200 Ω.'),
      [r'l=400\,\mathrm{nH/m}',r'c=160\,\mathrm{pF/m}',r'T_d=10\,\mathrm{ns}',r'\tau_p=1\,\mathrm{ns}'],10,4,[.20,.29,.60,.22],
      [R(4,31,'反弹图参数','Bounce-diagram parameters'),R(4,40,'短脉冲的反射','Short-pulse reflections')],[
        P('a',1,'求特性阻抗。','Find the characteristic impedance.',[
          S('先写无损传输线特性阻抗原式。l、c 都是每单位长度参数。', 'Begin with the lossless characteristic-impedance equation; l and c are both per-length parameters.', 'Z_0=\\sqrt{\\frac lc}', ['impedance']),
          S('先把 nH 与 pF 换成 H 与 F，两个前缀不能直接相消。', 'Convert nH and pF to H and F before forming their ratio.', 'l=400\\times10^{-9}\\,\\mathrm{H/m},\\qquad c=160\\times10^{-12}\\,\\mathrm{F/m}', []),
          S('计算根号内的比值，单位为 Ω²。', 'Evaluate the ratio under the square root, in Ω².', '\\frac lc=\\frac{400\\times10^{-9}}{160\\times10^{-12}}=2.5\\times10^3=2500\\,\\Omega^2', []),
          S('取正平方根，因为这里特性阻抗为正实数。', 'Take the positive square root for this positive real characteristic impedance.', 'Z_0=50\\,\\Omega', [])],r'Z_0=50\,\Omega',4),
        P('b',2,'求最初进入传输线的脉冲幅度 $V_1^+$。','Find the initial launched pulse amplitude $V_1^+$.',[
          S('原始分压公式给出尚未收到负载反射时进入线路的第一行波。', 'The launch-divider equation gives the first traveling wave before any load reflection returns.', 'V_1^+=V_g\\frac{Z_0}{R_g+Z_0}', ['bounce']),
          S('本题源脉冲为 3 V，损坏后的源电阻为 100 Ω，线路仍为 50 Ω。', 'The source pulse is 3 V, the damaged source resistance is 100 Ω and the line remains 50 Ω.', 'V_1^+=(3\\,\\mathrm V)\\frac{50\\,\\Omega}{100\\,\\Omega+50\\,\\Omega}', []),
          S('先求分压比 50/150=1/3，再乘源幅度；脉冲宽度仍是 1 ns。', 'Evaluate 50/150=1/3 and multiply by source amplitude; pulse width remains 1 ns.', 'V_1^+=(3\\,\\mathrm V)\\frac13', []),
          S('因此最初入射到线路的电压是 1 V，而非整个源脉冲的 3 V。', 'The initially launched voltage is therefore 1 V.', 'V_1^+=1.00\\,\\mathrm V', [])],r'V_1^+=1.00\,\mathrm V',4),
        P('c',6,r'绘制 $0\le t<4T_d$ 的反弹图，标出行波及源、负载处测得的幅度。',r'Draw the bounce diagram for $0\le t<4T_d$, labeling traveling and measured source/load amplitudes.',[
          S('先写端点反射公式以及到达波与反射波相加得到测量电压的关系。', 'Begin with endpoint reflection and the relation between measured voltage, arriving wave and its immediate reflection.', '\\Gamma=\\frac{R-Z_0}{R+Z_0},\\qquad V_{\\mathrm{ref}}=\\Gamma V_{\\mathrm{arr}},\\qquad V_{\\mathrm{end}}=(1+\\Gamma)V_{\\mathrm{arr}}', ['reflection']),
          S('分别把负载和源阻抗代入，得到两个正的反射系数。', 'Substitute the load and source resistances separately to obtain both positive reflection coefficients.', '\\Gamma_L=\\frac{200-50}{200+50}=\\frac35,\\qquad \\Gamma_g=\\frac{100-50}{100+50}=\\frac13', []),
          S('初始脉冲在 0 时刻从源出发，于 Tᵈ=10 ns 到达负载；负载产生第一反向波。', 'The initial pulse leaves the source at zero and reaches the load at Tᵈ=10 ns, producing the first backward wave.', 'V_1^+=1.00\\,\\mathrm V,\\qquad V_1^-=\\Gamma_LV_1^+', []),
          S('逐项计算第一次负载反射及负载实际电压；此处反射系数乘的是入射的 V₁⁺。', 'Calculate the first load reflection and actual load voltage. The reflection coefficient multiplies incident V₁⁺.', 'V_1^-=\\frac35(1)=0.60\\,\\mathrm V,\\qquad V_L(T_d)=(1+0.6)(1)=1.60\\,\\mathrm V', []),
          S('20 ns 时反向波回到源，源反射生成 V₂⁺；源端测到的是 V₁⁻+V₂⁺。', 'At 20 ns the return reaches the source and generates V₂⁺; measured source voltage is V₁⁻+V₂⁺.', 'V_2^+=\\Gamma_gV_1^-=\\frac13(0.6)=0.20\\,\\mathrm V,\\qquad V_{\\mathrm{in}}(2T_d)=0.6+0.2=0.80\\,\\mathrm V', []),
          S('30 ns 时第二次正向脉冲到达负载，继续乘 ΓL，负载电压仍是到达波与反射波之和。', 'At 30 ns the second forward pulse reaches the load. Multiply by ΓL again and add arrival plus reflection.', 'V_2^-=\\Gamma_LV_2^+=0.6(0.2)=0.12\\,\\mathrm V,\\qquad V_L(3T_d)=0.2+0.12=0.32\\,\\mathrm V', []),
          S('在反弹图上按 0、10、20、30、40 ns 标时刻。所有波宽均为 1 ns，彼此不重叠，不能像永久阶跃那样累加旧脉冲。', 'Label the diagram at 0, 10, 20, 30 and 40 ns. All pulses last 1 ns and do not overlap, so do not accumulate old pulses as for a permanent step.', '\\begin{gathered}V_1^-=0.60\\,\\mathrm V,\\quad V_2^+=0.20\\,\\mathrm V,\\quad V_2^-=0.12\\,\\mathrm V\\\\V_L(10\\,\\mathrm{ns})=1.60\\,\\mathrm V,\\quad V_{\\mathrm{in}}(20\\,\\mathrm{ns})=0.80\\,\\mathrm V,\\quad V_L(30\\,\\mathrm{ns})=0.32\\,\\mathrm V\\end{gathered}', [])],r'\begin{gathered}V_1^-=0.60\,\mathrm V,\quad V_2^+=0.20\,\mathrm V,\quad V_2^-=0.12\,\mathrm V\\V_L(10\,\mathrm{ns})=1.60\,\mathrm V,\quad V_{\mathrm{in}}(20\,\mathrm{ns})=0.80\,\mathrm V,\quad V_L(30\,\mathrm{ns})=0.32\,\mathrm V\end{gathered}',5,figure='bounce-f25',figureCaption=L('1 ns 有限脉冲的反弹图：标出各行波及源、负载处的测量电压。', 'Bounce diagram for a finite 1 ns pulse, labeling traveling waves and measured source/load voltages.')),
        P('d',1,'无限多次反射后，线上的电压为多少？','What is the line voltage after infinitely many reflections?',[
          S('先写每一轮反弹的递推式；相继正向波相差一整次负载反射和源反射。', 'Begin with the bounce recurrence: successive forward waves differ by one load and one source reflection.', 'V_{n+1}^+=\\Gamma_g\\Gamma_LV_n^+', ['reflection', 'bounce']),
          S('将上一问两系数相乘，得到小于 1 的往返倍率。', 'Multiply the preceding coefficients to obtain the round-trip factor, smaller than one.', '\\Gamma_g\\Gamma_L=\\frac13(0.6)=0.2,\\qquad V_n^+=(1\\,\\mathrm V)(0.2)^{n-1}', []),
          S('题目只发出一个 1 ns 脉冲，源随后回到零；后续有限宽脉冲的幅度逐轮趋于零。', 'Only one 1 ns pulse is emitted, after which the source returns to zero; subsequent finite-width pulse amplitudes decay to zero.', 'V_g(t>1\\,\\mathrm{ns})=0,\\qquad \\lim_{n\\to\\infty}(0.2)^{n-1}=0', []),
          S('因此稳态没有持续激励。端点电阻吸收脉冲能量，不能套用持续 DC 源的分压值。', 'There is no sustained excitation. The termination resistors absorb the pulse energy, so a permanent-DC divider value does not apply.', '\\lim_{t\\to\\infty}V(z,t)=0\\,\\mathrm V', [])],r'\lim_{t\to\infty}V(z,t)=0\,\mathrm V',5)
      ],caption=('线路示意与反弹轨迹；每次到达显示行波幅度，端点测量另加反射波。','Circuit and bounce trajectories show traveling-wave amplitudes; endpoint measurements add the immediate reflection.'))
    quarter=Q(f,3,'四分之一波长传输线','Quarter-wave transmission lines',('输入阻抗 · 电压相量','Input impedance · voltage phasors'),
      (r'信号源幅度 10 V、源电阻 50 Ω。无损传输线特性阻抗 50 Ω，长度 $L=\lambda/4$；负载 125 Ω。给定 $\lambda=20\,\mathrm m$、$f=100\,\mathrm{kHz}$。网页统一取输入端 z=0、负载端 z=L、源相位为零。',
       r'A 10 V source with resistance 50 Ω drives a lossless 50 Ω line of length $L=\lambda/4$, terminated in 125 Ω. Given $\lambda=20\,\mathrm m$ and $f=100\,\mathrm{kHz}$. Here z=0 is the input, z=L the load, and source phase is zero.'),
      [r'R_g=50\,\Omega',r'R_L=125\,\Omega',r'L=5\,\mathrm m',r'\beta=\pi/10\,\mathrm{rad/m}'],10,6,[.20,.19,.60,.18],
      [R(3,39,'输入阻抗的四分之一波长性质','Quarter-wave input impedance'),R(6,14,'四分之一波长匹配','Quarter-wave matching')],[
        P('a',1,'求输入阻抗。','Find input impedance.',[
          S('先写原表的四分之一波长阻抗变换性质。', 'Begin with the crib quarter-wave impedance transformation.', 'L=\\frac{\\lambda}{4}\\quad\\Longrightarrow\\quad Z_{\\mathrm{in}}=\\frac{Z_0^2}{Z_L}', ['quarter']),
          S('将本题 Z₀=50 Ω、负载 125 Ω 代入，平方的阻抗单位要保留。', 'Substitute Z₀=50 Ω and load 125 Ω, retaining units in the squared impedance.', 'Z_{\\mathrm{in}}=\\frac{(50\\,\\Omega)^2}{125\\,\\Omega}=\\frac{2500}{125}\\,\\Omega', []),
          S('由 λ/4 的变换性质，输入为实数；与 50 Ω 源并不匹配。', 'The quarter-wave property gives a real input, which does not match the 50 Ω source.', 'Z_{\\mathrm{in}}=20\\,\\Omega', [])],r'Z_{\mathrm{in}}=20\,\Omega',6),
        P('b',4,r'写出总电压相量 $\widetilde V(z)$。',r'Write the total voltage phasor $\widetilde V(z)$.',[
          S('先写总行波相量原式。明确本页取输入端 z=0、负载端 z=L，源相位为零。', 'Begin with the total traveling-wave phasor. Set z=0 at the input, z=L at the load and zero source phase.', '\\widetilde V(z)=V^+e^{-j\\beta z}+V^-e^{j\\beta z}', ['phasor']),
          S('由波长求 β 与线长，再求往返传播相位。', 'Use the wavelength to compute β and length, then the round-trip phase.', '\\beta=\\frac{2\\pi}{\\lambda}=\\frac{\\pi}{10}\\,\\mathrm{rad/m},\\quad L=\\frac{20}{4}=5\\,\\mathrm m,\\quad 2\\beta L=\\pi', ['wave']),
          S('先计算负载参考面的反射系数。', 'First calculate the reflection coefficient at the load reference plane.', '\\Gamma_L=\\frac{125-50}{125+50}=\\frac{75}{175}=\\frac37', ['reflection']),
          S('移至输入参考面必须乘往返相位；因此输入面的反向系数是负的。', 'Moving to the input plane requires the round-trip phase, making the backward coefficient negative there.', '\\Gamma_{\\mathrm{in}}=\\frac{V^-}{V^+}=\\Gamma_Le^{-2j\\beta L}=\\frac37e^{-j\\pi}=-\\frac37', []),
          S('写源端电压边界。Rg=Z₀ 时反向项抵消，只剩 2V⁺，由此确定正向幅度。', 'Write the source voltage boundary. Since Rg=Z₀, the backward terms cancel, leaving 2V⁺ and fixing the forward amplitude.', '\\begin{aligned}V_g&=\\widetilde V(0)+R_g\\widetilde I(0)\\\\&=(V^++V^-)+\\frac{R_g}{Z_0}(V^+-V^-)\\\\&=2V^+\\end{aligned}', []),
          S('代入 Vg=10 V，并乘输入反射系数求反向幅度。', 'Substitute Vg=10 V and multiply by the input reflection coefficient for the backward amplitude.', 'V^+=\\frac{10}{2}=5\\,\\mathrm V,\\qquad V^-=-\\frac37(5)=-\\frac{15}{7}\\,\\mathrm V', []),
          S('核对输入端分压：相量之和应为 10×20/(50+20)。这也检验反向项的符号。', 'Check input voltage division: the coefficient sum must equal 10×20/(50+20), verifying the backward sign.', '\\widetilde V(0)=5-\\frac{15}{7}=\\frac{20}{7}\\,\\mathrm V=10\\frac{20}{50+20}\\,\\mathrm V', []),
          S('将 β、正向与反向系数代回总行波相量。', 'Substitute β and both amplitudes into the traveling-wave phasor.', '\\widetilde V(z)=5e^{-j\\pi z/10}-\\frac{15}{7}e^{j\\pi z/10}\\quad[\\mathrm V]', [])],r'\widetilde V(z)=5e^{-j\pi z/10}-\frac{15}{7}e^{j\pi z/10}\quad[\mathrm V]',6,
          note=L('官方解写成 5e⁻ʲᵝᶻ+2.145eʲᵝᶻ，却未声明原点。对本页明确的“输入端 z=0、源相位 0”约定，反向项必须为负，否则不满足输入分压。若以负载为原点，两项还需统一的 −j 相位。','The official solution prints 5e⁻ʲᵝᶻ+2.145eʲᵝᶻ without fixing its origin. For the input-origin, zero-source-phase convention here, the backward term must be negative to satisfy the source divider. With a load origin both coefficients also carry a common −j phase.')),
        P('c',2,'把相量变换到时域。','Convert the phasor to the time domain.',[
          S('先写相量到瞬时值的定义，采用与前问相同的 eʲωt 约定。', 'Begin with the phasor-to-time definition using the same eʲωt convention as above.', 'v(z,t)=\\Re\\{\\widetilde V(z)e^{j\\omega t}\\}', ['phasor']),
          S('将 100 kHz 转为 Hz，再计算角频率。', 'Convert 100 kHz to Hz and calculate angular frequency.', 'f=100\\times10^3\\,\\mathrm{Hz}=10^5\\,\\mathrm{Hz},\\qquad\\omega=2\\pi f=2\\pi\\times10^5\\,\\mathrm{rad/s}', ['wave']),
          S('把上一问两个行波全部代入，并把时间因子分别乘进去。', 'Substitute both preceding waves and distribute the time factor.', 'v(z,t)=\\Re\\left\\{5e^{j(2\\pi10^5t-\\pi z/10)}-\\frac{15}{7}e^{j(2\\pi10^5t+\\pi z/10)}\\right\\}', []),
          S('逐项使用 Re(eʲθ)=cosθ；第二项的负实幅度必须保留。', 'Apply Re(eʲθ)=cosθ term by term, retaining the negative real amplitude of the second wave.', 'v(z,t)=5\\cos(2\\pi10^5t-\\pi z/10)-\\frac{15}{7}\\cos(2\\pi10^5t+\\pi z/10)\\quad[\\mathrm V]', [])],r'v(z,t)=5\cos(2\pi10^5t-\pi z/10)-\frac{15}{7}\cos(2\pi10^5t+\pi z/10)\quad[\mathrm V]',7,6),
        P('d',2,'保持 L=λ/4，要实现最大功率传输应改用多大 Z₀？','Keeping L=λ/4, which Z₀ gives maximum power transfer?',[
          S('先写最大功率传输的实阻抗匹配条件，以及原表四分之一波长变换式。', 'Begin with the resistive maximum-power matching condition and the crib quarter-wave relation.', 'Z_{\\mathrm{in}}=R_g,\\qquad Z_{\\mathrm{in}}=\\frac{Z_{0T}^2}{R_L}', ['quarter']),
          S('保持线长 λ/4，待选的是变换线的特性阻抗 Z₀T。把源和负载代入。', 'Keep the length λ/4 and solve for transformer characteristic impedance Z₀T. Substitute source and load values.', '50\\,\\Omega=\\frac{Z_{0T}^2}{125\\,\\Omega}', []),
          S('两边乘 125 Ω，再取正平方根。', 'Multiply by 125 Ω and take the positive square root.', 'Z_{0T}^2=(50\\,\\Omega)(125\\,\\Omega)=6250\\,\\Omega^2,\\qquad Z_{0T}=\\sqrt{6250}\\,\\Omega', []),
          S('所得特性阻抗使源看到 50 Ω 的实输入阻抗。', 'The resulting characteristic impedance presents a real 50 Ω input to the source.', 'Z_{0T}=79.06\\,\\Omega', [])],r'Z_{0T}=79.06\,\Omega',7,6),
        P('e',1,'为什么负载仍有反射，却可以最大功率传输？','How can maximum power transfer occur while the load still reflects?',[
          S('先写负载局部反射系数，再写整个网络向源呈现的输入阻抗；两者的参考位置不同。', 'Begin with the local load reflection coefficient and the input impedance of the whole network; they describe different reference planes.', '\\Gamma_L=\\frac{R_L-Z_{0T}}{R_L+Z_{0T}},\\qquad Z_{\\mathrm{in}}=\\frac{Z_{0T}^2}{R_L}', ['reflection', 'quarter']),
          S('将上一问选出的 Z₀T 代入输入阻抗，明确验证源端匹配。', 'Substitute the chosen Z₀T and explicitly verify the source input match.', 'Z_{\\mathrm{in}}=\\frac{(\\sqrt{50\\cdot125})^2}{125}=50\\,\\Omega=R_g', []),
          S('同一个变换线在负载处仍与 125 Ω 不相等，所以局部反射系数非零。', 'At the load the transformer impedance still differs from 125 Ω, so the local reflection coefficient remains nonzero.', '\\Gamma_L=\\frac{125-\\sqrt{50\\cdot125}}{125+\\sqrt{50\\cdot125}}\\approx0.2251\\ne0', []),
          S('无损线上的正反波共同构成匹配的输入电压电流比。接受的净功率沿线守恒，内部反向波并不等于没有功率送入负载。', 'Forward and backward waves jointly produce the matched input V/I ratio. Net accepted power is conserved along the lossless line despite the internal backward wave.', 'P_{\\mathrm{av}}=\\frac{|V^+|^2-|V^-|^2}{2Z_{0T}}>0', ['power']),
          S('因此最大功率传输与负载存在反射可以同时成立。', 'Maximum power transfer can therefore coexist with load reflections.', 'Z_{\\mathrm{in}}=R_g\\quad\\text{with}\\quad\\Gamma_L\\ne0', [])],r'Z_{\mathrm{in}}=R_g\quad\text{with}\quad\Gamma_L\ne0',7,answerText=L('输入端整体匹配与内部反射可以同时存在。','Overall input matching can coexist with internal reflections.'))
      ])

    def stub(exam,is_spring):
        load=r'(25+j90)\,\Omega' if is_spring else r'(150+j75)\,\Omega'
        z=r'0.5+j1.8' if is_spring else r'2+j'
        y=r'0.143266-j0.515759' if is_spring else r'0.4-j0.2'
        d=r'0.275283\lambda' if is_spring else r'0.198792\lambda'
        b=r'2.641969' if is_spring else '1'
        ell=r'0.307589\lambda' if is_spring else r'0.375000\lambda'
        pts=[2,1,3,2] if is_spring else [2,2,3,3]
        z0=50 if is_spring else 75
        note=L('核对：官方图给出 d≈0.271λ、ℓ≈0.305λ、b≈2.82，另一分支写 d≈0.318λ。直接代入给定 zL=0.5+j1.8 后，精确结果为本页数值；另一分支 d=0.378411λ、ℓ=0.192411λ。已用输入导纳方程独立校验。','Check: the official chart gives d≈0.271λ, ℓ≈0.305λ, b≈2.82 and an alternative d≈0.318λ. Direct substitution of zL=0.5+j1.8 gives the values here; the other exact branch is d=0.378411λ, ℓ=0.192411λ. Both are independently checked with the input-admittance equation.') if is_spring else None
        return Q(exam,4,'Smith 图上的单支节匹配','Single-stub matching on a Smith chart',('Smith 图 · 开路支节','Smith chart · open stub'),
          (rf'用开路并联支节，把负载 $Z_L={load}$ 匹配到 ${z0}\,\Omega$ 馈线。所有传输线特性阻抗均为 ${z0}\,\Omega$。求归一化阻抗、导纳、主线距离 d 和开路支节长度 ℓ。',
           rf'Match $Z_L={load}$ to a ${z0}\,\Omega$ feedline with an open-circuit shunt stub. Every line has characteristic impedance ${z0}\,\Omega$. Find normalized impedance/admittance, through-line distance d and stub length ℓ.'),
          [r'Z_L='+load,rf'Z_0={z0}\,\Omega',r'y_d+y_s=1'],8 if is_spring else 10,8,([.20,.16,.65,.19] if is_spring else [.25,.197,.53,.183]),
          [R(6,25,'阻抗归一化与 Smith 图','Normalization and the Smith chart'),R(7,19,'阻抗与导纳转换','Impedance-to-admittance conversion'),R(7,29,'单支节匹配步骤','Single-stub matching procedure')],[
            P('a',pts[0],'求归一化负载阻抗，并在 Smith 图上定位。','Normalize the load impedance and locate it on the Smith chart.',((((([
          S('先写归一化定义。这里 z 为无量纲负载阻抗，参考阻抗取该题馈线的 Z₀。', 'Begin with normalization. The load impedance z is dimensionless and referenced to the feedline Z₀.', 'z_L=\\frac{Z_L}{Z_0}', ['zin']),
          S('把复负载的实部和虚部分别除以 Z₀，保留电抗的正号。', 'Divide the real and imaginary parts by Z₀ separately, preserving the positive reactance.', 'z_L=\\frac{(25+j90)\\,\\Omega}{50\\,\\Omega}=0.5+j1.8', []),
          S('在 Smith 阻抗图中找 r=Re(zL) 圆与 x=Im(zL)>0 弧的交点；也可用反射系数验证坐标。', 'On the impedance chart intersect the r=Re(zL) circle with the positive-x reactance arc; verify the plotted coordinate with the reflection coefficient.', '\\Gamma_z=\\frac{z_L-1}{z_L+1}', ['reflection']),
          S('将已归一化的复数代入，得到该点的 Γ 平面坐标；它位于上半平面。', 'Substitute the normalized complex impedance to obtain its Γ-plane coordinate, in the upper half-plane.', '\\Gamma_z=\\frac{-0.5+j1.8}{1.5+j1.8}\\approx0.453552+j0.655738', [])] if is_spring else [
          S('先写归一化定义。这里 z 为无量纲负载阻抗，参考阻抗取该题馈线的 Z₀。', 'Begin with normalization. The load impedance z is dimensionless and referenced to the feedline Z₀.', 'z_L=\\frac{Z_L}{Z_0}', ['zin']),
          S('把复负载的实部和虚部分别除以 Z₀，保留电抗的正号。', 'Divide the real and imaginary parts by Z₀ separately, preserving the positive reactance.', 'z_L=\\frac{(150+j75)\\,\\Omega}{75\\,\\Omega}=2+j', []),
          S('在 Smith 阻抗图中找 r=Re(zL) 圆与 x=Im(zL)>0 弧的交点；也可用反射系数验证坐标。', 'On the impedance chart intersect the r=Re(zL) circle with the positive-x reactance arc; verify the plotted coordinate with the reflection coefficient.', '\\Gamma_z=\\frac{z_L-1}{z_L+1}', ['reflection']),
          S('将已归一化的复数代入，得到该点的 Γ 平面坐标；它位于上半平面。', 'Substitute the normalized complex impedance to obtain its Γ-plane coordinate, in the upper half-plane.', '\\Gamma_z=\\frac{(2+j)-1}{(2+j)+1}=\\frac{1+j}{3+j}=0.4+j0.2', [])]))))),r'z_L='+z,8),
            P('b',pts[1],'求归一化负载导纳，并说明如何在图上找到。','Find normalized load admittance and explain its chart construction.',((((([
          S('先写归一化导纳定义，再代入 Y=1/Z，说明为什么结果是 1/zL。', 'Begin with normalized admittance and substitute Y=1/Z to show why it equals 1/zL.', 'y_L=\\frac{Y_L}{Y_0}=\\frac{1/Z_L}{1/Z_0}=\\frac{Z_0}{Z_L}=\\frac1{z_L}', []),
          S('复数取倒数要乘共轭数；分母变成实部平方加虚部平方。', 'Take the complex reciprocal by multiplying by the conjugate; the denominator becomes the sum of squared components.', 'y_L=\\frac1{0.5+j1.8}=\\frac{0.5-j1.8}{0.5^2+1.8^2}=\\frac{50-j180}{349}\\approx0.143266-j0.515759', []),
          S('在同一阻抗网格上读取导纳时，表示坐标应关于图心反转，即旋转 180°。这不是让实际负载的反射改变符号。', 'Reading admittance on the same impedance grid requires reversing the displayed point through the center, a 180° rotation; the actual load reflection does not change sign.', '\\Gamma_y=\\frac{y_L-1}{y_L+1}=\\frac{1-z_L}{1+z_L}=-\\Gamma_z', ['reflection']),
          S('因此沿同一个等模圆转到对径点，再读出电导与电纳；代数倒数与图上结果一致。', 'Move to the diametrically opposite point on the same magnitude circle and read conductance and susceptance; the algebraic reciprocal verifies the chart.', 'y_L=\\frac1{0.5+j1.8}=\\frac{0.5-j1.8}{0.5^2+1.8^2}=\\frac{50-j180}{349}\\approx0.143266-j0.515759', [])] if is_spring else [
          S('先写归一化导纳定义，再代入 Y=1/Z，说明为什么结果是 1/zL。', 'Begin with normalized admittance and substitute Y=1/Z to show why it equals 1/zL.', 'y_L=\\frac{Y_L}{Y_0}=\\frac{1/Z_L}{1/Z_0}=\\frac{Z_0}{Z_L}=\\frac1{z_L}', []),
          S('复数取倒数要乘共轭数；分母变成实部平方加虚部平方。', 'Take the complex reciprocal by multiplying by the conjugate; the denominator becomes the sum of squared components.', 'y_L=\\frac1{2+j}=\\frac{2-j}{(2+j)(2-j)}=\\frac{2-j}{5}=0.4-j0.2', []),
          S('在同一阻抗网格上读取导纳时，表示坐标应关于图心反转，即旋转 180°。这不是让实际负载的反射改变符号。', 'Reading admittance on the same impedance grid requires reversing the displayed point through the center, a 180° rotation; the actual load reflection does not change sign.', '\\Gamma_y=\\frac{y_L-1}{y_L+1}=\\frac{1-z_L}{1+z_L}=-\\Gamma_z', ['reflection']),
          S('因此沿同一个等模圆转到对径点，再读出电导与电纳；代数倒数与图上结果一致。', 'Move to the diametrically opposite point on the same magnitude circle and read conductance and susceptance; the algebraic reciprocal verifies the chart.', 'y_L=\\frac1{2+j}=\\frac{2-j}{(2+j)(2-j)}=\\frac{2-j}{5}=0.4-j0.2', [])]))))),r'y_L='+y,8),
            P('c',pts[2],'求使 $y_d=1+jb$ 的主线距离 d。','Find through-line distance d for $y_d=1+jb$.',((((([
          S('先从原表输入阻抗式取倒数并归一化，得到向源移动距离 d 后的输入导纳。', 'Begin by taking the reciprocal of the crib input-impedance equation and normalizing to obtain admittance a distance d toward the source.', 'y_d=\\frac{y_L+jt}{1+jy_Lt},\\qquad t=\\tan(\\beta d),\\quad\\beta=\\frac{2\\pi}{\\lambda}', ['zin', 'wave']),
          S('把负载导纳分成 g+jb，将分母写成实部 1−bt 与虚部 gt。', 'Write load admittance as g+jb and express the denominator with real part 1−bt and imaginary part gt.', 'g=\\frac{50}{349},\\quad b=-\\frac{180}{349},\\quad |y_L|^2=\\frac{100}{349}', []),
          S('乘分母共轭数，单独取实部。匹配实部要求实际输入电导等于 Y₀，即归一化实部等于 1。', 'Multiply by the denominator conjugate and take the real part. Matching conductance to Y₀ requires normalized real part one.', '\\Re(y_d)=\\frac{g(1+t^2)}{(1-bt)^2+(gt)^2}=1', []),
          S('展开分母并把右边移到左边，得到可逐项代入的二次方程。', 'Expand the denominator and collect terms to obtain the quadratic for substitution.', '(g^2+b^2-g)t^2-2bt+(1-g)=0', []),
          S('把本题的 g、b 代入并求根；两个根对应 Smith 图与 g=1 圆的两个交点。', 'Substitute this load’s g and b and solve. The two roots correspond to the intersections with the g=1 circle on the Smith chart.', '50t^2+360t+299=0\\quad\\Longrightarrow\\quad t=\\frac{-360\\pm\\sqrt{69800}}{100}', []),
          S('列出两个 t 值，再由 t=tan(2πd/λ) 选 0≤d<λ/2 的分支。', 'List both t values, then choose branches satisfying 0≤d<λ/2 using t=tan(2πd/λ).', 't_1=-6.241969,\\quad t_2=-0.958031', []),
          S('反正切的负值要加 π 后再除以 2π；距离按 λ/2 周期重复。图上对应从负载向源顺时针旋转。', 'For a negative arctangent add π before dividing by 2π. Distances repeat modulo λ/2; on the chart rotate clockwise toward the source.', '\\frac{d_1}{\\lambda}=\\frac{\\pi+\\arctan(-6.241969)}{2\\pi}=0.275283,\\quad\\frac{d_2}{\\lambda}=0.378411', []),
          S('把两个距离对应的 t 代回输入导纳式，验证实部确为 1，并保留待抵消的虚部。', 'Substitute each t back into the admittance formula to verify real part one and retain the susceptance to be cancelled.', 'y_{d,1}=\\frac{y_L+j(-6.241969)}{1+jy_L(-6.241969)}\\approx1+j2.641969,\\quad y_{d,2}\\approx1-j2.641969', []),
          S('选第一组非负距离作为本页主答案；另一分支仍是有效匹配方案。', 'Choose the first nonnegative distance as the primary solution; the other branch is also valid.', 'd=0.275283\\lambda,\\qquad y_d=1+j2.641969', [])] if is_spring else [
          S('先从原表输入阻抗式取倒数并归一化，得到向源移动距离 d 后的输入导纳。', 'Begin by taking the reciprocal of the crib input-impedance equation and normalizing to obtain admittance a distance d toward the source.', 'y_d=\\frac{y_L+jt}{1+jy_Lt},\\qquad t=\\tan(\\beta d),\\quad\\beta=\\frac{2\\pi}{\\lambda}', ['zin', 'wave']),
          S('把负载导纳分成 g+jb，将分母写成实部 1−bt 与虚部 gt。', 'Write load admittance as g+jb and express the denominator with real part 1−bt and imaginary part gt.', 'g=0.4,\\quad b=-0.2,\\quad |y_L|^2=0.20', []),
          S('乘分母共轭数，单独取实部。匹配实部要求实际输入电导等于 Y₀，即归一化实部等于 1。', 'Multiply by the denominator conjugate and take the real part. Matching conductance to Y₀ requires normalized real part one.', '\\Re(y_d)=\\frac{g(1+t^2)}{(1-bt)^2+(gt)^2}=1', []),
          S('展开分母并把右边移到左边，得到可逐项代入的二次方程。', 'Expand the denominator and collect terms to obtain the quadratic for substitution.', '(g^2+b^2-g)t^2-2bt+(1-g)=0', []),
          S('把本题的 g、b 代入并求根；两个根对应 Smith 图与 g=1 圆的两个交点。', 'Substitute this load’s g and b and solve. The two roots correspond to the intersections with the g=1 circle on the Smith chart.', '-0.2t^2+0.4t+0.6=0\\quad\\Longrightarrow\\quad t^2-2t-3=(t-3)(t+1)=0', []),
          S('列出两个 t 值，再由 t=tan(2πd/λ) 选 0≤d<λ/2 的分支。', 'List both t values, then choose branches satisfying 0≤d<λ/2 using t=tan(2πd/λ).', 't_1=3,\\quad t_2=-1', []),
          S('反正切的负值要加 π 后再除以 2π；距离按 λ/2 周期重复。图上对应从负载向源顺时针旋转。', 'For a negative arctangent add π before dividing by 2π. Distances repeat modulo λ/2; on the chart rotate clockwise toward the source.', '\\frac{d_1}{\\lambda}=\\frac{\\arctan3}{2\\pi}=0.198792,\\quad \\frac{d_2}{\\lambda}=\\frac{\\pi-\\pi/4}{2\\pi}=0.375000', []),
          S('把两个距离对应的 t 代回输入导纳式，验证实部确为 1，并保留待抵消的虚部。', 'Substitute each t back into the admittance formula to verify real part one and retain the susceptance to be cancelled.', 'y_{d,1}=\\frac{0.4-j0.2+j3}{1+j(0.4-j0.2)3}=1+j,\\quad y_{d,2}=1-j', []),
          S('选第一组非负距离作为本页主答案；另一分支仍是有效匹配方案。', 'Choose the first nonnegative distance as the primary solution; the other branch is also valid.', 'd=0.198792\\lambda,\\qquad y_d=1+j1', [])]))))),r'd='+d+r',\qquad y_d=1+j'+b,8,note=note if note else L('另一有效分支为 d=0.375λ、yd=1−j。所有距离按 λ/2 周期重复。','The other branch is d=0.375λ with yd=1−j. Distances repeat modulo λ/2.'),figureCaption=(L('按给定负载精确计算的导纳 Smith 图；两组匹配结果在推导中分别核验。', 'Admittance Smith chart computed from the stated load; both matching branches are checked in the derivation.') if is_spring else L('阻抗与导纳在同一 Smith 网格上的对径点、g=1 的两个交点及第一组匹配旋转。', 'Diametrically opposite impedance/admittance chart points, both g=1 intersections, and the first matching rotation.'))),
            P('d',pts[3],'求完成匹配的开路支节长度 ℓ。','Find the open-stub length ℓ that completes the match.',((((([
          S('先写原表开路传输线阻抗，再取倒数并用 Y₀=1/Z₀ 归一化。', 'Begin with the crib open-line impedance, then invert and normalize with Y₀=1/Z₀.', 'Z_s=-jZ_0\\cot(\\beta\\ell),\\qquad y_s=\\frac{1/Z_s}{1/Z_0}=j\\tan(\\beta\\ell)', ['open']),
          S('支节并联时导纳相加，目标是总归一化导纳为 1。若主线为 1+jB，支节必须为 −jB。', 'Parallel admittances add and the target total is one. If the main line is 1+jB, the stub must supply −jB.', 'y_{\\mathrm{in}}=y_d+y_s=1,\\qquad y_s=1-(1+jB)=-jB', []),
          S('代入 c) 选中分支的电纳，列出需要满足的正切方程。', 'Insert the susceptance of the selected branch from c) and write the tangent equation.', 'y_s=-j2.641969,\\qquad \\tan(2\\pi\\ell/\\lambda)=-2.641969', []),
          S('选最小非负的开路支节长度；正切为负时使用第二象限的电长度。', 'Choose the smallest nonnegative open-stub length; a negative tangent requires a second-quadrant electrical length.', '\\beta\\ell=\\pi-\\arctan(2.641969),\\qquad \\frac{\\ell}{\\lambda}=\\frac{\\pi-\\arctan(2.641969)}{2\\pi}=0.307589', []),
          S('核对虚部恰好抵消；若改用另一主线交点，必须同时改用配套的支节长度。', 'Check exact susceptance cancellation. Choosing the other main-line intersection also requires its corresponding stub length.', 'd_2=0.378411\\lambda,\\quad y_{s,2}=+j2.641969,\\quad \\ell_2=0.192411\\lambda', []),
          S('本页所选分支的开路支节参数如下。', 'The open-stub parameters for the selected branch are:', '\\ell=0.307589\\lambda,\\qquad y_s=-j2.641969', [])] if is_spring else [
          S('先写原表开路传输线阻抗，再取倒数并用 Y₀=1/Z₀ 归一化。', 'Begin with the crib open-line impedance, then invert and normalize with Y₀=1/Z₀.', 'Z_s=-jZ_0\\cot(\\beta\\ell),\\qquad y_s=\\frac{1/Z_s}{1/Z_0}=j\\tan(\\beta\\ell)', ['open']),
          S('支节并联时导纳相加，目标是总归一化导纳为 1。若主线为 1+jB，支节必须为 −jB。', 'Parallel admittances add and the target total is one. If the main line is 1+jB, the stub must supply −jB.', 'y_{\\mathrm{in}}=y_d+y_s=1,\\qquad y_s=1-(1+jB)=-jB', []),
          S('代入 c) 选中分支的电纳，列出需要满足的正切方程。', 'Insert the susceptance of the selected branch from c) and write the tangent equation.', 'y_s=-j,\\qquad \\tan(2\\pi\\ell/\\lambda)=-1', []),
          S('选最小非负的开路支节长度；正切为负时使用第二象限的电长度。', 'Choose the smallest nonnegative open-stub length; a negative tangent requires a second-quadrant electrical length.', '\\beta\\ell=-\\pi/4+\\pi=3\\pi/4,\\qquad \\frac{\\ell}{\\lambda}=\\frac{3\\pi/4}{2\\pi}=0.375', []),
          S('核对虚部恰好抵消；若改用另一主线交点，必须同时改用配套的支节长度。', 'Check exact susceptance cancellation. Choosing the other main-line intersection also requires its corresponding stub length.', 'd_2=0.375\\lambda,\\quad y_{d,2}=1-j,\\quad y_{s,2}=+j,\\quad\\ell_2=0.125\\lambda', []),
          S('本页所选分支的开路支节参数如下。', 'The open-stub parameters for the selected branch are:', '\\ell=0.375000\\lambda,\\qquad y_s=-j1', [])]))))),r'\ell='+ell+r',\qquad y_s=-j'+b,8)
          ],caption=('左侧复刻并联开路支节结构；右侧为 Matplotlib 绘制的 Smith 图，点标记给出两组匹配交点。','Left: recreated shunt open-stub topology. Right: a Matplotlib Smith chart marking both matching intersections.'))

    lowloss=Q(s,1,'从测量反推低损耗模型','Recovering a low-loss line model',('参数测量 · 低损耗线','Measurements · low-loss line'),
      ('一卷 100 m 的低损耗同轴线连接 25 Ω 信号源和 50 Ω 负载。测得单程时延 392 ns；扫频时输入幅度恒为 1 V。100 MHz 时，输入与负载电压幅度分别为 1 V、0.904 V。忽略并联漏电导。',
       'A 100 m low-loss cable connects a 25 Ω source to a 50 Ω load. Measured one-way delay is 392 ns, and input amplitude stays at 1 V during a frequency sweep. At 100 MHz, input and load amplitudes are 1 V and 0.904 V. Neglect shunt conductance.'),
      [r'L=100\,\mathrm m',r'T_d=392\,\mathrm{ns}',r'R_g=25\,\Omega',r'R_L=50\,\Omega'],8,2,[.22,.18,.58,.16],linelect,[
        P('a',1,'求速度因子。','Find the velocity factor.',[
          S('先写传播距离、单程时间与波速的关系，再用速度因子的定义。', 'Begin with the distance, one-way time and speed relation, then the velocity-factor definition.', 'u=\\frac L{T_d},\\qquad \\mathrm{vf}=\\frac u{u_c}', ['bounce', 'velocity']),
          S('将长度和测得时延统一为米与秒。', 'Express length and measured delay in meters and seconds.', 'L=100\\,\\mathrm m,\\qquad T_d=392\\,\\mathrm{ns}=392\\times10^{-9}\\,\\mathrm s', []),
          S('代入距离除以时间，先求实际传播速度。', 'Substitute distance divided by time to compute the propagation speed first.', 'u=\\frac{100}{392\\times10^{-9}}\\,\\mathrm{m/s}=2.5510204\\times10^8\\,\\mathrm{m/s}', []),
          S('再除以真空光速，速度因子没有单位。', 'Divide by vacuum light speed to obtain a dimensionless factor.', '\\mathrm{vf}=\\frac{2.5510204\\times10^8}{3.00\\times10^8}=0.85034\\approx0.85', [])],r'\mathrm{vf}=0.85034\approx0.85',2),
        P('b',1,'由扫频时的输入幅度不变，推断特性阻抗。','Infer characteristic impedance from frequency-independent input amplitude.',[
          S('先写反射系数与输入阻抗原式，识别随频率变化的驻波来源。', 'Begin with the reflection and input-impedance equations to identify frequency-dependent standing-wave behavior.', '\\Gamma_L=\\frac{Z_L-Z_0}{Z_L+Z_0},\\qquad Z_{\\mathrm{in}}=Z_0\\frac{Z_L+jZ_0\\tan(\\beta L)}{Z_0+jZ_L\\tan(\\beta L)}', ['reflection', 'zin']),
          S('扫频改变 βL；若有明显负载失配，输入阻抗通常随频率改变，源端分压也会改变。', 'Sweeping frequency changes βL. With load mismatch, input impedance and hence the source divider generally vary with frequency.', 'V_{\\mathrm{in}}=V_g\\frac{Z_{\\mathrm{in}}}{R_g+Z_{\\mathrm{in}}},\\qquad \\beta=\\frac{2\\pi f}{u}', []),
          S('按题设固定源和低损耗近似，输入幅度不随扫频变化，采用官方的匹配推断 ΓL≈0。', 'For the stated fixed-source, low-loss model, follow the official inference that constant input amplitude indicates ΓL≈0.', '\\Gamma_L\\approx0\\quad\\Longrightarrow\\quad Z_L-Z_0\\approx0', []),
          S('负载是 50 Ω，所以推断出的特性阻抗也是约 50 Ω。', 'The 50 Ω load therefore implies approximately the same characteristic impedance.', 'Z_0\\approx50\\,\\Omega', [])],r'Z_0\approx50\,\Omega',2),
        P('c',1,'在 100 MHz 时求波长。','Find wavelength at 100 MHz.',[
          S('先写公式表的波长与波速关系。', 'Begin with the crib wavelength–speed relation.', '\\lambda=\\frac uf', ['wave']),
          S('使用 a) 从时延测出的未舍入波速，并把频率换成 Hz。', 'Use the unrounded speed measured in a) and convert frequency to Hz.', 'u=2.5510204\\times10^8\\,\\mathrm{m/s},\\qquad f=100\\,\\mathrm{MHz}=100\\times10^6\\,\\mathrm{Hz}', []),
          S('代入数值，s⁻¹ 与 m/s 中的时间单位约去。', 'Substitute the values and cancel the time units.', '\\lambda=\\frac{2.5510204\\times10^8\\,\\mathrm{m/s}}{100\\times10^6\\,\\mathrm{s^{-1}}}', []),
          S('按题目要求保留至少两位有效数字。', 'Retain at least the two significant digits requested.', '\\lambda=2.5510\\,\\mathrm m\\approx2.55\\,\\mathrm m', [])],r'\lambda=2.5510\,\mathrm m\approx2.55\,\mathrm m',2),
        P('d',2,'求每单位长度电感 l 和电容 c。','Find per-unit-length inductance l and capacitance c.',[
          S('先写需要联立的两条原表公式；低损耗近似下使用无损线的 Z₀ 与波速关系。', 'Begin with both crib equations, using the lossless relations for Z₀ and speed in the low-loss approximation.', 'Z_0=\\sqrt{\\frac lc},\\qquad u=\\frac1{\\sqrt{lc}}', ['impedance', 'velocity']),
          S('将 Z₀ 除以 u，根号相乘后只剩 l；将 Z₀ 乘 u 得到 1/c。', 'Divide Z₀ by u to isolate l; multiply Z₀ by u to obtain 1/c.', '\\frac{Z_0}{u}=\\sqrt{\\frac lc}\\sqrt{lc}=l,\\qquad Z_0u=\\frac{\\sqrt{l/c}}{\\sqrt{lc}}=\\frac1c', []),
          S('先代入求每单位长度电感，保留 H/m 单位。', 'Substitute to obtain inductance per unit length, retaining H/m.', 'l=\\frac{Z_0}{u}=\\frac{50}{2.5510204\\times10^8}=1.9600\\times10^{-7}\\,\\mathrm{H/m}', []),
          S('再独立代入求电容，不要把分母中的 Z₀ 漏掉。', 'Substitute separately for capacitance, retaining Z₀ in the denominator.', 'c=\\frac1{Z_0u}=\\frac1{50(2.5510204\\times10^8)}=7.8400\\times10^{-11}\\,\\mathrm{F/m}', []),
          S('把 H、F 分别换为 nH、pF；此处沿用未舍入时延，原解的微小差别来自中间舍入。', 'Convert H and F to nH and pF. The small difference from the official inductance comes from its intermediate rounding.', 'l=196.0\\,\\mathrm{nH/m},\\qquad c=78.40\\,\\mathrm{pF/m}', [])],r'l=196.0\,\mathrm{nH/m},\qquad c=78.40\,\mathrm{pF/m}',3,note=L('使用未舍入的 392 ns 得 l=196.0 nH/m；官方先取 vf=0.85 得 196.1 nH/m，属于舍入差异。','Using the unrounded 392 ns gives l=196.0 nH/m. The official 196.1 nH/m uses vf rounded to 0.85.')),
        P('e',2,'由幅度比求衰减常数 α。','Find attenuation constant α from the amplitude ratio.',[
          S('先写有损行波包络。负载匹配时幅度之比直接给出单程指数衰减。', 'Begin with the lossy-wave envelope; with a matched load, the amplitude ratio gives one-way exponential attenuation.', '|V(L)|=|V(0)|e^{-\\alpha L}', ['lossy-wave']),
          S('把两个测得幅度及线长代入，先形成无量纲比值。', 'Substitute the measured amplitudes and length, forming a dimensionless ratio first.', '\\frac{0.904\\,\\mathrm V}{1.000\\,\\mathrm V}=e^{-\\alpha(100\\,\\mathrm m)}', []),
          S('两边取自然对数；指数的负号不能省去。', 'Take natural logarithms on both sides, keeping the minus sign.', '\\ln(0.904)=-\\alpha(100\\,\\mathrm m)', []),
          S('再除以负的长度系数，得到正衰减常数。', 'Divide by the negative length coefficient to obtain a positive attenuation constant.', '\\alpha=-\\frac{\\ln(0.904)}{100\\,\\mathrm m}=\\frac{0.1009259186}{100\\,\\mathrm m}', []),
          S('幅度的指数衰减用 Np/m 表示，不是功率衰减或 dB/m。', 'This amplitude attenuation is in Np/m, rather than a power coefficient or dB/m.', '\\alpha=1.00926\\times10^{-3}\\,\\mathrm{Np/m}', [])],r'\alpha=1.00926\times10^{-3}\,\mathrm{Np/m}',3),
        P('rf',1,'求每单位长度串联电阻 r。','Find series resistance per unit length r.',[
          S('先写原表低损耗衰减公式。按该题模型忽略并联漏电导 g。', 'Begin with the crib low-loss attenuation equation, neglecting shunt conductance g in this model.', '\\alpha=\\frac r{2Z_0}', ['attenuation']),
          S('两边乘 2Z₀，先解出未知串联电阻密度。', 'Multiply both sides by 2Z₀ to isolate series resistance per length.', 'r=2Z_0\\alpha', []),
          S('代入未舍入的衰减系数和 b) 的 50 Ω 特性阻抗。', 'Insert the unrounded attenuation and the 50 Ω characteristic impedance from b).', 'r=2(50\\,\\Omega)(1.0092592\\times10^{-3}\\,\\mathrm{m^{-1}})', []),
          S('化简并检查单位是 Ω/m。', 'Simplify and check the units are Ω/m.', 'r=0.10093\\,\\Omega/\\mathrm m\\approx0.10\\,\\Omega/\\mathrm m', [])],r'r=0.10093\,\Omega/\mathrm m\approx0.10\,\Omega/\mathrm m',3)
      ])
    transient=Q(s,2,'直流阶跃的多次反射','Multiple reflections of a DC step',('瞬态 · 反弹图','Transients · bounce diagrams'),
      ('t=0 时开关闭合，10 V 恒定直流源通过 30 Ω 源电阻驱动 50 Ω 传输线。负载为 150 Ω，单程时延 50 ps。与短脉冲不同，源电压将持续保持。',
       'At t=0 a switch connects a sustained 10 V DC source through 30 Ω to a 50 Ω line. The load is 150 Ω and one-way delay is 50 ps. Unlike a short pulse, the source remains on.'),
      [r'V_g=10\,\mathrm V',r'R_g=30\,\Omega',r'Z_0=50\,\Omega',r'R_L=150\,\Omega',r'T_d=50\,\mathrm{ps}'],8,4,[.21,.16,.59,.18],
      [R(4,31,'行波反弹参数','Traveling-wave bounce parameters'),R(4,41,'持续直流阶跃','Sustained DC step')],[
        P('a',2,'求负载与源端反射系数。','Find the load and source reflection coefficients.',[
          S('先写原表的端点电压反射系数；负载端和源端都以同一个线路 Z₀ 为参考。', 'Begin with the crib endpoint voltage reflection coefficient, referencing both ends to the same line Z₀.', '\\Gamma=\\frac{Z-Z_0}{Z+Z_0}', ['reflection']),
          S('负载端代入 150 Ω 和 50 Ω，先算差再算和。', 'At the load insert 150 Ω and 50 Ω, evaluating the difference and sum separately.', '\\Gamma_L=\\frac{150-50}{150+50}=\\frac{100}{200}=+0.50', []),
          S('源端返回波看到 30 Ω 源电阻，因此对应系数为负。', 'A wave returning to the source sees its 30 Ω resistance, giving a negative coefficient.', '\\Gamma_g=\\frac{30-50}{30+50}=\\frac{-20}{80}=-0.25', []),
          S('两系数均为电压比，无量纲；负号表示源端反射电压反相。', 'Both coefficients are dimensionless voltage ratios; the negative sign indicates voltage inversion at the source.', '\\Gamma_L=0.50,\\qquad\\Gamma_g=-0.25', [])],r'\Gamma_L=0.50,\qquad\Gamma_g=-0.25',4),
        P('b',2,'求 $V_1^+,V_1^-,V_2^+,V_2^-$。','Find $V_1^+,V_1^-,V_2^+,V_2^-$.',[
          S('先写初始分压和反射递推式，再按传播顺序逐个计算。', 'Begin with the launch divider and reflection recurrence, then evaluate in propagation order.', 'V_1^+=V_g\\frac{Z_0}{R_g+Z_0},\\qquad V_n^-=\\Gamma_LV_n^+,\\qquad V_{n+1}^+=\\Gamma_gV_n^-', ['bounce', 'reflection']),
          S('t=0 时把 10 V、30 Ω、50 Ω 代入，得到第一正向阶跃。', 'At t=0 substitute 10 V, 30 Ω and 50 Ω to obtain the first forward step.', 'V_1^+=(10\\,\\mathrm V)\\frac{50}{30+50}=10\\frac58=6.25\\,\\mathrm V', []),
          S('50 ps 时到达负载，第一反向波乘负载反射系数 +0.5。', 'At 50 ps the wave reaches the load; multiply by +0.5 for the first backward wave.', 'V_1^-=\\Gamma_LV_1^+=0.5(6.25)=3.125\\,\\mathrm V', []),
          S('100 ps 时反向波到源，再乘 −0.25，得到第二正向阶跃。', 'At 100 ps the return reaches the source; multiply by −0.25 for the second forward step.', 'V_2^+=\\Gamma_gV_1^-=-0.25(3.125)=-0.78125\\,\\mathrm V', []),
          S('150 ps 时第二正向阶跃到负载，再乘 +0.5；两次反射的负号不能丢失。', 'At 150 ps the second forward step reaches the load; multiply by +0.5, retaining its negative sign.', 'V_2^-=\\Gamma_LV_2^+=0.5(-0.78125)=-0.390625\\,\\mathrm V', []),
          S('把四个行波幅度标在反弹图对应的四条轨迹上。', 'Label these four traveling-wave amplitudes on their four bounce trajectories.', '\\begin{gathered}V_1^+=6.25\\,\\mathrm V,\\quad V_1^-=3.125\\,\\mathrm V\\\\V_2^+=-0.78125\\,\\mathrm V,\\quad V_2^-=-0.390625\\,\\mathrm V\\end{gathered}', [])],r'\begin{gathered}V_1^+=6.25\,\mathrm V,\quad V_1^-=3.125\,\mathrm V\\V_2^+=-0.78125\,\mathrm V,\quad V_2^-=-0.390625\,\mathrm V\end{gathered}',4,figure='bounce-s26',figureCaption=L('持续 DC 阶跃的反弹图：各行波按 50 ps 单程时延传播，端点电压需累加历史阶跃。', 'Bounce diagram of a sustained DC step with 50 ps transit time; endpoint voltages include previous steps.')),
        P('c',3,r'画 $0\le t\le150\,\mathrm{ps}$ 的负载电压，标出临界时刻。',r'Plot load voltage for $0\le t\le150\,\mathrm{ps}$, labeling critical times.',[
          S('先写每次到达负载所增加的电压：入射阶跃与即时反射阶跃相加。', 'Begin with each load voltage increment: add the arriving step and its immediate reflected step.', '\\Delta V_{L,n}=V_n^++V_n^-=(1+\\Gamma_L)V_n^+', ['bounce', 'reflection']),
          S('第一行波传播时间为 50 ps，未到达前，负载处仍没有电压变化。', 'The first transit takes 50 ps, so the load voltage remains unchanged before that arrival.', 'V_L(t)=0\\quad(0\\le t<50\\,\\mathrm{ps})', []),
          S('50 ps 到达时代入 V₁⁺ 与 ΓL，求第一次阶跃后的平台值。', 'At 50 ps substitute V₁⁺ and ΓL to obtain the first plateau.', 'V_L(50^+\\,\\mathrm{ps})=0+(1+0.5)(6.25)=9.375\\,\\mathrm V', []),
          S('100 ps 的反射发生在源端；还需再传播 50 ps 才影响负载，所以中间平台保持不变。', 'The 100 ps reflection occurs at the source and needs another 50 ps to affect the load, so the intermediate plateau stays unchanged.', 'V_L(t)=9.375\\,\\mathrm V\\quad(50\\le t<150\\,\\mathrm{ps})', []),
          S('150 ps 第二次入射带来负的增量。源持续接通，所以新平台要在旧平台上累加。', 'The second arrival at 150 ps gives a negative increment. With the source still on, add it to the existing plateau.', '\\Delta V_{L,2}=(1+0.5)(-0.78125)=-1.171875\\,\\mathrm V', []),
          S('将增量加到 9.375 V，按右连续理想阶跃标记端点。', 'Add the increment to 9.375 V and mark right-continuous ideal-step values.', 'V_L(150^+\\,\\mathrm{ps})=9.375-1.171875=8.203125\\,\\mathrm V', [])],r'V_L(t)=\begin{cases}0&0\le t<50\,\mathrm{ps}\\9.375\,\mathrm V&50\le t<150\,\mathrm{ps}\\8.203125\,\mathrm V&t=150^+\,\mathrm{ps}\end{cases}',5,figure='load-step-s26',figureCaption=L('负载电压在 50 ps 上升至 9.375 V，在 150 ps 降至 8.203125 V。', 'Load voltage rises to 9.375 V at 50 ps and falls to 8.203125 V at 150 ps.')),
        P('d',1,'求稳态电压。','Find the steady-state voltage.',[
          S('持续 DC 的最终稳态中，无损传输线等效为理想连接；用串联回路的电压定律开始推导。', 'At final sustained-DC steady state the lossless line is an ideal connection. Begin with the series-loop voltage law.', 'V_g=I_\\infty R_g+I_\\infty R_L=I_\\infty(R_g+R_L)', []),
          S('先求最终电流，再乘负载电阻。', 'Solve for final current, then multiply by the load resistance.', 'I_\\infty=\\frac{V_g}{R_g+R_L},\\qquad V_\\infty=I_\\infty R_L=V_g\\frac{R_L}{R_g+R_L}', []),
          S('代入 10 V、30 Ω 和 150 Ω。', 'Substitute 10 V, 30 Ω and 150 Ω.', 'V_\\infty=(10\\,\\mathrm V)\\frac{150}{30+150}=\\frac{1500}{180}\\,\\mathrm V', []),
          S('也可对反弹图求和：第一负载增量为 9.375 V，每次往返乘 ΓgΓL=−1/8。', 'Alternatively sum the bounce increments: the first is 9.375 V and each round trip multiplies it by ΓgΓL=−1/8.', 'V_\\infty=9.375\\sum_{n=0}^\\infty(-1/8)^n=\\frac{9.375}{1-(-1/8)}', ['bounce']),
          S('级数求和与 DC 电路分压完全一致。', 'The geometric sum agrees with the DC circuit divider.', 'V_\\infty=\\frac{25}{3}\\,\\mathrm V\\approx8.333\\,\\mathrm V', [])],r'V_\infty=\frac{25}{3}\,\mathrm V\approx8.333\,\mathrm V',5)
      ],caption=('左图为各次行波；右图为负载电压阶跃，在 50 ps 与 150 ps 发生变化。','Traveling-wave bounces and load-voltage steps. Load changes occur at 50 ps and 150 ps.'))

    inputq=Q(s,3,'输入阻抗与支节阻断','Input impedance & a blocking stub',('半波线 · 四分之一波线','Half-wave · quarter-wave lines'),
      ('各电路频率均为 200 MHz，电缆速度因子 0.65，可选电缆特性阻抗为 25、50、75 Ω。分别利用半波重复、四分之一波变换及开路支节性质作答。',
       'Every circuit operates at 200 MHz with velocity factor 0.65. Available cables have characteristic impedances 25, 50 and 75 Ω. Use half-wave repetition, quarter-wave transformation and open-stub properties.'),
      [r'f=200\,\mathrm{MHz}',r'\mathrm{vf}=0.65',r'\lambda=0.975\,\mathrm m'],8,6,[.13,.28,.66,.52],
      [R(6,14,'四分之一波长匹配','Quarter-wave matching'),R(7,42,'支节作为陷波器','Stubs as blocking filters')],[
        P('a(i)',2,'电路 1：Rg=RL=100 Ω。选择电缆类型与匹配长度。','Circuit 1: Rg=RL=100 Ω. Choose cable type and matching length.',[
          S('此问两端都是 100 Ω，优先使用原表的半波阻抗重复性质。', 'Both terminations are 100 Ω, so start with the crib half-wave impedance-repeat property.', 'L=\\frac{\\lambda}{2}\\quad\\Longrightarrow\\quad Z_{\\mathrm{in}}=Z_L', ['half']),
          S('无论选 25、50 还是 75 Ω 电缆，半波线都将 100 Ω 负载重复为 100 Ω 输入，等于源电阻。', 'A half-wave line of 25, 50 or 75 Ω repeats the 100 Ω load as a 100 Ω input, matching the source.', 'Z_{\\mathrm{in}}=100\\,\\Omega=R_g,\\qquad Z_0\\in\\{25,50,75\\}\\,\\Omega', []),
          S('先由速度因子和频率计算电缆内波长。', 'First calculate the cable wavelength from velocity factor and frequency.', '\\lambda=\\frac{\\mathrm{vf}\\,u_c}{f}=\\frac{0.65(3\\times10^8\\,\\mathrm{m/s})}{200\\times10^6\\,\\mathrm{Hz}}=0.975\\,\\mathrm m', ['wave', 'velocity']),
          S('取一个半波的正长度即可完成所需匹配。', 'One positive half-wavelength length gives the required match.', 'L=\\frac{0.975\\,\\mathrm m}{2}=0.4875\\,\\mathrm m', []),
          S('因此三种给定电缆都可使用，长度相同。', 'All three available cables therefore work with the same length.', 'Z_0\\in\\{25,50,75\\}\\,\\Omega,\\qquad L=0.4875\\,\\mathrm m', [])],r'Z_0\in\{25,50,75\}\,\Omega,\qquad L=0.4875\,\mathrm m',6),
        P('a(ii)',2,'电路 2：Rg=50 Ω、RL=12.5 Ω。选择电缆类型与长度。','Circuit 2: Rg=50 Ω, RL=12.5 Ω. Choose cable type and length.',[
          S('不同的纯电阻之间使用四分之一波长变换。先写原表阻抗反演式并设输入等于源电阻。', 'Use a quarter-wave transformer between unequal real resistances. Begin with impedance inversion and set the input equal to source resistance.', 'Z_{\\mathrm{in}}=\\frac{Z_0^2}{R_L}=R_g', ['quarter']),
          S('先解出待选电缆的特性阻抗，代入 50 Ω 与 12.5 Ω。', 'Solve for the cable characteristic impedance and substitute 50 Ω and 12.5 Ω.', 'Z_0=\\sqrt{R_gR_L}=\\sqrt{(50\\,\\Omega)(12.5\\,\\Omega)}=\\sqrt{625}\\,\\Omega=25\\,\\Omega', []),
          S('三种给定电缆中，25 Ω 对应类型 #1。再由统一的速度因子求波长。', 'Among the available cables, 25 Ω is type #1. Next calculate wavelength using the common velocity factor.', '\\lambda=\\frac{0.65(3\\times10^8)}{200\\times10^6}=0.975\\,\\mathrm m', ['wave']),
          S('取四分之一波长，并核对反演后确实为 50 Ω。', 'Choose a quarter wavelength and verify the transformed resistance is 50 Ω.', 'L=\\frac{0.975}{4}=0.24375\\,\\mathrm m,\\qquad \\frac{25^2}{12.5}=50\\,\\Omega', []),
          S('所需类型与长度如下。', 'The required cable and length are:', 'Z_0=25\\,\\Omega,\\qquad L=0.24375\\,\\mathrm m', [])],r'Z_0=25\,\Omega,\qquad L=0.24375\,\mathrm m',6),
        P('b',2,'50 Ω 四分之一波线，负载为 50 Ω 电阻串联 1 μF 电容。求输入阻抗。','Find input impedance of a 50 Ω quarter-wave line terminated in 50 Ω in series with 1 μF.',[
          S('先把串联电阻与电容合并为负载阻抗，再用四分之一波长性质变换。', 'First combine the series resistor and capacitor as the load, then use the quarter-wave property.', 'Z_C=\\frac1{j\\omega C},\\qquad Z_L=R+Z_C,\\qquad Z_{\\mathrm{in}}=\\frac{Z_0^2}{Z_L}', ['quarter']),
          S('由频率求角频率，并把 1 μF 写为 10⁻⁶ F。', 'Calculate angular frequency and express 1 μF as 10⁻⁶ F.', '\\omega=2\\pi(200\\times10^6)\\,\\mathrm{rad/s},\\qquad C=10^{-6}\\,\\mathrm F', ['wave']),
          S('利用 1/j=−j 求电容阻抗，并与 50 Ω 相加。', 'Use 1/j=−j for the capacitor impedance and add the 50 Ω resistor.', 'Z_C=-\\frac j{2\\pi(200\\times10^6)(10^{-6})}=-j7.95775\\times10^{-4}\\,\\Omega,\\qquad Z_L=50-j7.95775\\times10^{-4}\\,\\Omega', []),
          S('代入原表反演式，再乘分母共轭数，显示虚部符号为何反转。', 'Substitute into the crib inversion and multiply by the denominator conjugate to show the imaginary-sign reversal.', '\\begin{aligned}Z_{\\mathrm{in}}&=\\frac{2500}{50-jX_C}\\\\&=\\frac{2500(50+jX_C)}{50^2+X_C^2},\\quad X_C=7.95775\\times10^{-4}\\,\\Omega\\end{aligned}', []),
          S('Xc² 远小于 50²，因此实部约为 50 Ω，虚部为小的正电抗。', 'Since Xc² is negligible relative to 50², the real part is approximately 50 Ω with a small positive reactance.', 'Z_{\\mathrm{in}}\\approx(50+j7.95775\\times10^{-4})\\,\\Omega', [])],r'Z_{\mathrm{in}}\approx(50+j7.95775\times10^{-4})\,\Omega',7),
        P('c',2,'在 z=A 处并联一根开路支节，负载 100+j100 Ω。求使 A 处全反射的最短支节长度。','An open stub is in shunt at z=A with a 100+j100 Ω load. Find the shortest stub length producing total reflection at A.',[
          S('先写原表的开路支节输入阻抗。要使有电阻负载的并联节点全反射，可把支节输入变成短路。', 'Begin with the crib open-stub impedance. To obtain total reflection at a shunt node with a resistive load contribution, make the stub input a short.', 'Z_s=-jZ_0\\cot(\\beta\\ell)', ['open']),
          S('令支节输入阻抗为零，即 cot(βℓ)=0，选择最短正电长度 π/2。', 'Set the stub input to zero, requiring cot(βℓ)=0; choose the shortest positive electrical length π/2.', '\\beta\\ell=\\frac\\pi2,\\qquad\\ell=\\frac{\\pi/2}{2\\pi/\\lambda}=\\frac\\lambda4', ['wave']),
          S('短路支节并联任何有限负载都会把节点 A 的总阻抗压为零。', 'A shorted shunt branch makes the total impedance at A zero for any finite parallel load.', 'Z_A=\\frac{Z_sZ_L}{Z_s+Z_L}=\\frac{0\\cdot Z_L}{0+Z_L}=0', []),
          S('将节点阻抗代入反射系数原式；电压反相，模为 1。', 'Substitute the node impedance into the reflection equation; voltage reverses sign and the magnitude is one.', '\\Gamma_A=\\frac{Z_A-Z_0}{Z_A+Z_0}=\\frac{-Z_0}{Z_0}=-1', ['reflection']),
          S('由共同速度因子和频率求得 λ=0.975 m，再取四分之一波长。', 'The common velocity factor and frequency give λ=0.975 m; take one quarter of it.', '\\ell=\\frac\\lambda4=0.24375\\,\\mathrm m,\\qquad|\\Gamma_A|=1', [])],r'\ell=\frac\lambda4=0.24375\,\mathrm m,\qquad|\Gamma_A|=1',7)
      ])
    from exam1_f26 import create as f26
    return [E(f,1,('秋季','Fall'),2025,40,[cable,qubit,quarter,stub(f,False)]),E(s,1,('春季','Spring'),2026,32,[lowloss,transient,inputq,stub(s,True)]),f26(L,S,P,R,Q,E)]
