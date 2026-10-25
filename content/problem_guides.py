"""Authored study introductions, separate from the verbatim exam questions.

Each introduction identifies the concepts, actual givens, requested quantities
and a starting route. Lecture links come from the problem's checked PDF refs.
Do not use computed answers as givens or turn these into replacement questions.
"""


def apply_guides(exams):
    def guide(concept_zh, concept_en, known_zh, known_en,
              goal_zh, goal_en, approach_zh, approach_en):
        return {
            name: {'zh': zh, 'en': en}
            for name, zh, en in [
                ('concept', concept_zh, concept_en),
                ('known', known_zh, known_en),
                ('goal', goal_zh, goal_en),
                ('approach', approach_zh, approach_en),
            ]
        }

    guides = {
        'e1-f25-q1': guide(
            "本题把传输线匹配、传播速度和低损耗衰减放在同一条有线电视连接中考查。",
            "This problem connects impedance matching, propagation speed and low-loss attenuation in a cable-TV link.",
            r"电缆长 $30\,\mathrm m$，速度因子为 $0.85$，频率为 $250\,\mathrm{MHz}$；初始情况下源、线和负载均为 $75\,\Omega$。衰减小问另给出单位长度电阻。",
            r"The cable is $30\,\mathrm m$ long, with velocity factor $0.85$ and frequency $250\,\mathrm{MHz}$. Initially the source, line and load are all $75\,\Omega$; the attenuation part also supplies the resistance per unit length.",
            "判断反射，求延迟、波长和到达负载的入射电压，再研究换用另一种电缆后的最短匹配长度。",
            "Check reflection, find delay, wavelength and the incident voltage at the load, then find the shortest matching length for a different cable.",
            "先比较负载与特性阻抗，再把速度因子换成波速。求电压幅值时分别考虑源端分压和沿线衰减；最后利用输入阻抗随电长度重复的性质。",
            "Start by comparing load and line impedances, then convert velocity factor to speed. Separate the launch voltage divider from propagation loss, and use the periodicity of input impedance for the final part."),
        'e1-f25-q2': guide(
            "本题考查有限宽度脉冲在失配传输线上的发射、反射与反弹图。",
            "This problem follows the launch and repeated reflections of a finite-duration pulse on a mismatched line.",
            r"$l=400\,\mathrm{nH/m}$、$c=160\,\mathrm{pF/m}$、$T_d=10\,\mathrm{ns}$；源脉冲为 $3\,\mathrm V$、持续 $1\,\mathrm{ns}$，$R_g=100\,\Omega$、$R_L=200\,\Omega$。",
            r"The line has $l=400\,\mathrm{nH/m}$, $c=160\,\mathrm{pF/m}$ and $T_d=10\,\mathrm{ns}$. A $3\,\mathrm V$, $1\,\mathrm{ns}$ source pulse drives $R_g=100\,\Omega$ and $R_L=200\,\Omega$.",
            "求特性阻抗和初始入射脉冲，标清各次反射与端点测得的电压，并判断长时间后的状态。",
            "Find the characteristic impedance and initial pulse, label reflected waves and measured endpoint voltages, and determine the long-time behavior.",
            "先由分布参数求特性阻抗，再求源端分压与两端反射系数。反弹图中要区分行波幅值和端点总电压，并记住源脉冲会结束。",
            "Find line impedance from its distributed parameters, then the launch divider and both reflection coefficients. Distinguish traveling-wave amplitudes from total endpoint voltage, and remember that the source pulse ends."),
        'e1-f25-q3': guide(
            "本题考查四分之一波长阻抗变换，以及相量、时域波形与功率匹配之间的联系。",
            "This problem links quarter-wave impedance transformation, phasors, time-domain waves and power matching.",
            r"原电路中 $Z_0=50\,\Omega$、$L=\lambda/4$、$R_g=50\,\Omega$、$R_L=125\,\Omega$；源幅值为 $10\,\mathrm V$，并给出了波长与频率。",
            r"The original circuit has $Z_0=50\,\Omega$, $L=\lambda/4$, $R_g=50\,\Omega$ and $R_L=125\,\Omega$. The source amplitude is $10\,\mathrm V$, and wavelength and frequency are supplied.",
            "求输入阻抗、总电压的相量和时域表达式，选择匹配用电缆，并解释匹配时为何仍可存在局部反射。",
            "Find input impedance and total voltage in phasor and time-domain form, choose a matching line, and explain why local reflections can remain.",
            "先用四分之一波长的特殊性质看清输入端负载，再由源端边界条件确定行波。将端口是否匹配与负载处是否反射分开讨论。",
            "Use the quarter-wave property to identify the impedance seen by the source, then determine the waves from the source boundary condition. Treat port matching and reflection at the load as separate questions."),
        'e1-f25-q4': guide(
            "本题考查 Smith 图上的阻抗与导纳转换，以及并联开路支节匹配。",
            "This problem uses Smith-chart impedance/admittance conversion and a parallel open-circuit matching stub.",
            r"负载为 $Z_L=(150+j75)\,\Omega$，馈线与支节的特性阻抗为 $75\,\Omega$，支节终端开路。",
            r"The load is $Z_L=(150+j75)\,\Omega$, the lines have characteristic impedance $75\,\Omega$, and the stub is open-circuited.",
            "依次找出归一化负载阻抗、导纳、支节接入距离和支节长度，并在图上说明过程。",
            "Locate the normalized load impedance and admittance, then find the stub position and length with the construction shown on the chart.",
            "并联结构用导纳相加最直接。先把负载转为导纳，沿等反射系数圆转到实部匹配的位置，再让开路支节补偿剩余的虚部。",
            "Admittances add directly in a parallel network. Convert the load to admittance, rotate along its constant-reflection circle until the real part matches, then cancel the remaining imaginary part with the open stub."),
        'e1-s26-q1': guide(
            "本题是从实验读数反推传输线参数：传播、匹配和衰减需要依次联系起来。",
            "This problem works backward from measurements to the propagation, matching and loss parameters of a transmission line.",
            r"电缆长 $100\,\mathrm m$，测得延迟 $392\,\mathrm{ns}$；图中 $R_g=25\,\Omega$、$R_L=50\,\Omega$，输入电压幅值不随频率变化。后续给出频率及输入、输出幅值。",
            r"The cable is $100\,\mathrm m$ long with measured delay $392\,\mathrm{ns}$. The circuit has $R_g=25\,\Omega$ and $R_L=50\,\Omega$, and the input-voltage magnitude is independent of frequency. Later parts supply frequency and endpoint amplitudes.",
            r"求速度因子、$Z_0$、波长、单位长度电感与电容，再由幅值衰减求 $\alpha$ 和单位长度电阻。",
            r"Find velocity factor, $Z_0$, wavelength and distributed inductance and capacitance; then infer $\alpha$ and resistance per unit length from attenuation.",
            "先由长度和延迟确定波速，再利用频率无关的输入测量判断匹配。最后处理损耗，注意电压幅值的衰减指数与功率的衰减指数不同。",
            "Find speed from length and delay, then interpret the frequency-independent input measurement to identify matching. Handle loss afterward, keeping voltage-amplitude attenuation distinct from power attenuation."),
        'e1-s26-q2': guide(
            "本题考查持续直流阶跃在失配传输线上的反弹过程，以及暂态与稳态的区别。",
            "This problem distinguishes the transient reflections of a sustained DC step from the eventual steady state.",
            r"$V_g=10\,\mathrm V$、$R_g=30\,\Omega$、$Z_0=50\,\Omega$、$R_L=150\,\Omega$，单程延迟 $T_d=50\,\mathrm{ps}$；开关闭合后电源持续接通。",
            r"The sustained source has $V_g=10\,\mathrm V$, $R_g=30\,\Omega$, $Z_0=50\,\Omega$ and $R_L=150\,\Omega$, with one-way delay $T_d=50\,\mathrm{ps}$.",
            "求两端反射系数和前几次行波，画出指定时间内的负载电压，再求稳态电压。",
            "Find both reflection coefficients and the first traveling waves, plot the specified load-voltage history, and find the steady-state voltage.",
            "先求初始发射波，再按到达端点的时刻逐次反射。负载电压是入射波与反射波的和；长时间结果还应与直流等效电路相符。",
            "Start with the launched wave and reflect it at each arrival time. Load voltage combines incident and reflected waves; the long-time limit should agree with the DC equivalent circuit."),
        'e1-s26-q3': guide(
            "本题通过不同电路考查传输线的阻抗变换、匹配和开路支节的滤波作用。",
            "These circuits test impedance transformation, matching and the filtering action of an open-circuit stub.",
            r"所有电路均有 $f=200\,\mathrm{MHz}$、速度因子 $0.65$；第 a) 问可选 $25\,\Omega$、$50\,\Omega$、$75\,\Omega$ 电缆，各电路的连接与终端见原图。",
            r"All circuits operate at $200\,\mathrm{MHz}$ with velocity factor $0.65$. Part a offers $25\,\Omega$, $50\,\Omega$ and $75\,\Omega$ cables; each diagram supplies its connections and terminations.",
            "选出匹配所需的电缆类型和实际长度，计算指定输入阻抗，并确定使主线发生全反射的支节长度。",
            "Select cable type and physical length for matching, calculate the specified input impedance, and choose a stub length that produces total reflection.",
            "先把电长度与米数联系起来，再识别半波、四分之一波等特殊长度。遇到并联支节时改用导纳，先判断接点实际呈现开路还是短路。",
            "Relate electrical length to physical length, then recognize half-wave and quarter-wave properties. For a parallel stub, use admittance and identify whether the junction effectively sees an open or a short."),
        'e1-s26-q4': guide(
            "本题考查用 Smith 图完成单支节匹配，重点是并联时应使用导纳。",
            "This problem constructs a single-stub match on the Smith chart, using admittance for the parallel connection.",
            r"负载为 $Z_L=(25+j90)\,\Omega$，所有线段均有 $Z_0=50\,\Omega$，匹配支节开路。",
            r"The load is $Z_L=(25+j90)\,\Omega$, all line sections have $Z_0=50\,\Omega$, and the matching stub is open-circuited.",
            "求归一化阻抗、导纳，以及直通线距离和开路支节长度，并标出 Smith 图上的读数过程。",
            "Find normalized impedance and admittance, then the through-line distance and open-stub length, showing the Smith-chart readings.",
            "归一化后先作阻抗到导纳的中心对称转换，再向发生器方向旋转到电导匹配处。此时支节只需补偿电纳，注意两条可行分支与读数方向。",
            "Normalize, reflect through the chart center to convert impedance to admittance, then rotate toward the generator to match conductance. The stub cancels susceptance; keep track of both branches and the direction of the wavelength scale."),
        'e1-f26-q1': guide(
            "本题从分布参数模型出发，把无损线的传播性质与直流反弹图连接起来。",
            "This problem connects a distributed line model to lossless propagation and a DC bounce diagram.",
            r"模型给出 $l=0.3125\,\mathrm{\mu H/m}$、$c=55.6\,\mathrm{pF/m}$，电缆长度为 $60\,\mathrm m$；后半题的源与负载参数见电路图。",
            r"The model supplies $l=0.3125\,\mathrm{\mu H/m}$ and $c=55.6\,\mathrm{pF/m}$ for a $60\,\mathrm m$ cable. The later circuit supplies its source and load parameters.",
            "判断线是否有损，求速度因子、特性阻抗与延迟，再计算开关闭合后的反射和指定端点电压。",
            "Identify loss, find velocity factor, characteristic impedance and delay, then calculate reflections and the requested endpoint voltages after switching.",
            "先确认模型包含哪些储能或耗能元件，再求线参数。反弹分析使用这些参数作为输入，并把单个行波幅值与端点叠加电压区分开。",
            "First identify the storage and loss elements in the model, then calculate the line parameters. Use them in the bounce diagram, distinguishing individual wave amplitudes from summed endpoint voltages."),
        'e1-f26-q2': guide(
            "本题从已测得的正、反向电压相量分析受损线上的驻波、功率和等效终端。",
            "This problem uses measured forward and backward voltage phasors to analyze standing waves, power and an effective termination.",
            r"两行波为 $\widetilde V^+=5e^{-j2\pi z}\,\mathrm V$ 与 $\widetilde V^-=3e^{j2\pi z}\,\mathrm V$，并给出 $Z_0=50\,\Omega$ 和工作频率。",
            r"The waves are $\widetilde V^+=5e^{-j2\pi z}\,\mathrm V$ and $\widetilde V^-=3e^{j2\pi z}\,\mathrm V$, with $Z_0=50\,\Omega$ and the operating frequency supplied.",
            "求时域电压、反射系数、驻波比、最大电压、净平均功率与等效阻抗，并与未损坏时比较。",
            "Find time-domain voltage, reflection coefficient, standing-wave ratio, maximum voltage, net average power and effective impedance, then compare with the undamaged line.",
            "先保留传播方向和相位约定，再从两行波的比值与叠加出发。功率要扣除反向波携带的功率，不能只把总电压幅值代入电阻功率式。",
            "Keep propagation direction and phase conventions explicit. Use the ratio and superposition of the waves, and subtract backward-wave power rather than treating total voltage magnitude as a resistor voltage."),
        'e1-f26-q3': guide(
            "本题考查能否识别传输线的特殊性质，而不是直接套用通用输入阻抗公式。",
            "This problem tests recognition of line properties rather than substitution into the general input-impedance formula.",
            r"各电路给出终端、发生器电阻与线长，包括 $\lambda/6$、$\lambda/2$、$\lambda/4$ 及并联开路支节；线的特性阻抗为 $50\,\Omega$。",
            r"The diagrams supply terminations, source resistances and lengths including $\lambda/6$, $\lambda/2$, $\lambda/4$ and a parallel open stub. The characteristic impedance is $50\,\Omega$.",
            "分别求发生器看到的输入阻抗，并据此判断源端是否匹配。",
            "Find the impedance seen by the generator in each circuit and decide whether the source is matched.",
            "先检查终端是否已匹配，再识别半波重复与四分之一波变换。并联支节应先合成导纳，最后才将总输入阻抗与发生器电阻比较。",
            "Check for a matched termination, then recognize half-wave repetition and quarter-wave transformation. Combine a parallel stub in admittance before comparing the resulting input impedance with the source resistance."),
        'e1-f26-q4': guide(
            "本题考查先用主线消去复负载的虚部，再用四分之一波长变换器完成匹配。",
            "This problem first transforms a complex load to a real impedance, then completes the match with a quarter-wave transformer.",
            r"$Z_L=(150-j50)\,\Omega$、$Z_0=50\,\Omega$，长度为 $d$ 的线速度因子为 $0.85$，工作频率为 $100\,\mathrm{MHz}$。",
            r"The load is $Z_L=(150-j50)\,\Omega$ and the feedline is $50\,\Omega$. The section of length $d$ has velocity factor $0.85$ at $100\,\mathrm{MHz}$.",
            "在 Smith 图上找出两种纯实输入阻抗，选一支求实际线长与变换器阻抗，并判断系统内部哪些界面仍有反射。",
            "Find the two real input impedances on the Smith chart, choose a branch for physical length and transformer impedance, and identify interfaces where reflections remain.",
            "先沿负载的等反射系数圆找到实轴交点，再把图上的波长读数换成米。四分之一波变换器负责第二次阻抗变换；馈线匹配并不等于内部每个界面都匹配。",
            "Find the real-axis crossings on the load's constant-reflection circle and convert wavelength readings to meters. The quarter-wave section performs the second transformation; a matched feedline does not imply that every internal interface is matched."),
        'e2-f25-q1': guide(
            "本题考查球对称高斯定律，以及改变介质后电场与电势差的变化。",
            "This problem uses spherical symmetry in Gauss's law and examines how dielectric material changes field and potential difference.",
            r"半径 $a$ 的球有均匀体电荷密度 $\rho_0$；半径 $b$ 的导体壳带等量异号总电荷，初始夹层介电常数为 $\varepsilon_0$。",
            r"A sphere of radius $a$ has uniform charge density $\rho_0$. The conducting shell at radius $b$ carries the opposite total charge; the gap initially has permittivity $\varepsilon_0$.",
            "为三个径向区域分别选取高斯面并求电场，再解释填入更高介电常数材料后电势差如何变化。",
            "Choose Gaussian surfaces and find the field in three radial regions, then explain the change in potential difference for a higher-permittivity dielectric.",
            "先按观察半径列出实际包围的电荷，再利用球面对称性简化通量。导体壳与球的总电荷相消，只能直接用于同时包围二者的高斯面。",
            "Determine the enclosed charge separately for each observation radius, then use spherical symmetry to simplify flux. Cancellation of the two total charges applies directly only to a surface enclosing both."),
        'e2-f25-q2': guide(
            "本题考查介质边界条件和电场能量法，并用电路中的并联电容作核对。",
            "This problem combines dielectric boundary conditions with field-energy capacitance and a parallel-capacitor check.",
            r"两极板间距为 $L$，电势分别为 $V_0$、$V_1$；两种介质沿高度各占一半，介电常数为 $\varepsilon_1$、$\varepsilon_2$，共同承受两板间电压。",
            r"The plates are separated by $L$ at potentials $V_0$ and $V_1$. Two dielectrics of permittivities $\varepsilon_1$ and $\varepsilon_2$ each occupy half the height and share the plate voltage.",
            "求第二种介质中的电场与电位移、总储能和电容，再判断是否符合并联电容规则。",
            "Find the field and displacement in the second dielectric, total stored energy and capacitance, then compare with the parallel-capacitor rule.",
            "先看清电场相对介质界面的方向，选择切向边界条件。分别对两块介质积分能量后相加；电场方向的符号还要与极板电势核对。",
            "Identify the field direction relative to the dielectric interface and use the tangential boundary condition. Integrate energy over each dielectric and add the results, checking the field's sign against the plate potentials."),
        'e2-f25-q3': guide(
            "本题考查柱对称 Laplace 方程，从电势边界条件一路求到表面电荷与电容。",
            "This problem solves a cylindrically symmetric Laplace equation, then obtains surface charge and capacitance from the potential.",
            r"同轴内、外导体半径为 $a$、$b$，有 $V(a)=0$、$V(b)=-V_0$；介质介电常数为 $\varepsilon$，间隙内没有自由体电荷。",
            r"The coaxial conductors have radii $a$ and $b$, with $V(a)=0$ and $V(b)=-V_0$. The gap has permittivity $\varepsilon$ and no free volume charge.",
            "求间隙内电势、电位移、两导体的表面电荷密度和单位长度电容。",
            "Find potential, electric displacement, both conductor surface-charge densities and capacitance per unit length.",
            "先用对称性把电势写成半径的函数，再用两个电势条件确定积分常数。由电势求场后，分别检查内、外导体表面法向的符号。",
            "Use symmetry to make potential a function of radius, then determine integration constants from both boundary potentials. Differentiate to obtain the field and check the outward normal separately at each conductor."),
        'e2-f25-q4': guide(
            "本题考查电场的矢量叠加、受力以及静电势差的路径无关性。",
            "This problem combines vector field superposition, electric force and path independence of electrostatic potential.",
            r"两个半径为 $a$ 的导体球位于 $x=\pm d$，分别带 $+Q$、$-Q$；观察点为 $P=(0,0,z)$，另有关于原点至 $P$ 的电势差问题。",
            r"Two conducting spheres of radius $a$ are centered at $x=\pm d$ with charges $+Q$ and $-Q$. The observation point is $P=(0,0,z)$; the potential-difference question runs from the origin to $P$.",
            "从单球外部电场出发求两球的合场、试探电荷受力，并列出电势差积分，说明积分路径是否影响结果。",
            "Start with the exterior field of one sphere, find the combined field and force on a test charge, and set up the potential integral with an explanation of path independence.",
            "按试卷采用的球外场模型，先写出每个源指向观察点的位移矢量，再相加分量。电场是矢量，不能仅将两项大小相加；模型适用性见后面的核对说明。",
            "Under the exterior-sphere field model used by the exam, write each source-to-observer displacement vector before adding components. Add vectors rather than magnitudes; the later source note discusses the model's scope."),
        'e2-s26-q1': guide(
            "本题考查电流密度的通量积分、微观欧姆定律，以及趋肤效应为什么会增大电阻。",
            "This problem connects current-density flux, microscopic Ohm's law and the resistance increase caused by skin effect.",
            r"微带线宽为 $W$、厚为 $h$、电导率为 $\sigma$，电流沿 $x$ 方向。题设分段给出 $\vec J(z)$：上下表层有电流，中间区域为零。",
            r"The strip has width $W$, thickness $h$ and conductivity $\sigma$, with current along $x$. The given piecewise $\vec J(z)$ is nonzero in the top and bottom surface layers and zero in the middle.",
            r"依次求总电流 $I$、单位长度电势降 $V^\prime$ 和单位长度电阻 $R^\prime$，再解释电导率与电流分布的影响。",
            r"Find total current $I$, voltage drop per unit length $V^\prime$ and resistance per unit length $R^\prime$, then explain the effects of conductivity and current distribution.",
            r"先认清哪些区域真正载流，再选垂直于电流的横截面积分。得到总电流后，用 $\mathbf J=\sigma\mathbf E$ 联系电场与电势降，最后回到电阻定义。",
            r"Identify the current-carrying regions before integrating over a cross-section perpendicular to the current. Then use $\mathbf J=\sigma\mathbf E$ to connect field and voltage drop, and apply the definition of resistance."),
        'e2-s26-q2': guide(
            "本题考查分层介质中切向电场与法向电位移的边界条件，以及介质极化的解释。",
            "This problem applies tangential-field and normal-displacement boundary conditions to layered dielectrics and interprets them through polarization.",
            r"三层介电常数依次为 $2\varepsilon_0$、$5\varepsilon_0$、$2\varepsilon_0$，中间层厚 $0.01\,\mathrm m$；已给出第一层的 $\vec E_1=100\hat x-100\hat y$。",
            r"The layers have permittivities $2\varepsilon_0$, $5\varepsilon_0$ and $2\varepsilon_0$, with a $0.01\,\mathrm m$ middle layer. The first-layer field is $\vec E_1=100\hat x-100\hat y$.",
            "求第二、第三层电场和中间层两端的电势差，并用极化解释电场大小的差异。",
            "Find the fields in layers two and three and the voltage across the middle layer, then explain the field-magnitude differences through polarization.",
            "先按界面方向把电场分为切向与法向。在无自由面电荷的介质界面，分别使用切向电场连续和法向电位移连续，再沿法向路径计算电势差。",
            "Split the field into tangential and normal components. At a dielectric interface without free surface charge, preserve tangential electric field and normal displacement, then integrate along the normal to obtain the voltage."),
        'e2-s26-q3': guide(
            "本题考查有体电荷时的柱对称高斯定律、电势积分和微分电容，不能直接套用无体电荷的同轴公式。",
            "This problem combines cylindrical Gauss's law, potential integration and differential capacitance in the presence of volume charge.",
            r"内、外导体半径为 $a$、$b$，内表面电荷密度为 $\rho_{sa}$，外导体接地；间隙介电常数为 $\varepsilon$，体电荷密度为 $\rho(r)=\rho_0a/r$。",
            r"The conductors have radii $a$ and $b$, inner surface-charge density $\rho_{sa}$ and a grounded outer conductor. The gap has permittivity $\varepsilon$ and volume-charge density $\rho(r)=\rho_0a/r$.",
            r"求电场、电势和导体间电压，再将 $\rho_{sa}$ 写成电压的函数，最后用 $dQ/dV_0$ 求单位长度电容。",
            r"Find field, potential and conductor voltage, express $\rho_{sa}$ as a function of voltage, then obtain capacitance per unit length using $dQ/dV_0$.",
            "同轴高斯面包围的电荷包括内导体表面电荷和一部分体电荷。先分别计入二者，再积分得到电势；求微分电容时保持给定体电荷分布不变。",
            "A coaxial Gaussian surface encloses both inner-conductor charge and part of the volume charge. Account for both before integrating the field to potential; hold the given volume-charge distribution fixed when differentiating for capacitance."),
        'e2-s26-q4': guide(
            "本题考查镜像法、库仑场叠加和理想导体表面的电荷边界条件。",
            "This problem combines image charges, Coulomb-field superposition and the surface-charge boundary condition at a perfect conductor.",
            r"真实电荷 $-q$、$+q$ 位于 $(-x_0,0,z_0)$、$(x_0,0,z_0)$；理想导体占据 $z<0$，上方介质的介电常数为 $\varepsilon_0$，观察点在表面上方。",
            r"The real charges $-q$ and $+q$ are at $(-x_0,0,z_0)$ and $(x_0,0,z_0)$. A perfect conductor occupies $z<0$, the upper region has permittivity $\varepsilon_0$, and the field is evaluated just above its surface.",
            "构造镜像几何与电场线，求单个真实电荷和完整系统的表面电场，再求感应面电荷密度。",
            "Construct the image geometry and field lines, find the surface field of one real charge and of the complete system, then obtain induced surface-charge density.",
            "先为每个真实电荷确定镜像的位置和符号，再逐项写出位移矢量。叠加后检查导体表面的切向场是否抵消；镜像下半空间用于辅助计算，不是导体内部的真实电场。",
            "Assign each real charge its mirrored position and opposite sign, then write the displacement vectors. Check cancellation of tangential field at the conductor; the image region is a mathematical construction, not the physical field inside the conductor."),
    }
    problems = {p['id']: p for exam in exams for p in exam['problems']}
    if guides.keys() != problems.keys():
        raise ValueError("Every original problem must have exactly one authored guide")
    for problem_id, introduction in guides.items():
        problems[problem_id]['guide'] = introduction
