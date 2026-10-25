"""Original English question wording, transcribed from the bundled exam PDFs.

Only line wrapping, mathematical typesetting and list layout are normalized.
Problem/part labels and point values are rendered separately by the application.
Keep source typos and inconsistent givens here; explain corrections in solutions.
The Fall 2026 source contains solutions: those are deliberately excluded.
"""

def question(title, statement, *parts):
    return dict(title=title, statement=statement, parts=list(parts))


ORIGINAL_QUESTIONS = {
    'e1-f25-q1': question('Cable TV Connection',
        r'''You want to connect your television to a cable TV feed point located on the opposite side of your house. The only coaxial cable (T1) you have available for this purpose has the following properties:
• Length: $30\,\mathrm{m}$
• Characteristic impedance: $75\,\Omega$
• Velocity factor: $0.85$

The cable TV feed point consists of a voltage source $V_g$ with an amplitude of $1\,\mathrm{V}$, source impedance $R_g$ of $75\,\Omega$ and frequency $f$ of $250\,\mathrm{MHz}$. The television’s load impedance $R_L$ is also $75\,\Omega$. A circuit diagram illustrating this setup is shown below.''',
        'If you use the provided cable to connect the cable TV feed point to your television, will there be a reflection at the load? Explain why or why not.',
        'What is the time delay of the coaxial cable?',
        'What is the wavelength of the signal on the coaxial cable',
        r'Assuming that the cable can be considered low-loss and has a per-length resistance of $r=1\,\Omega/\mathrm{m}$, calculate the amplitude of the incident voltage wave at the load.',
        r'If the coaxial cable’s characteristic impedance were instead $50\Omega$, what is the minimum length of cable $(L>0)$ needed to be to ensure maximum power transfer from the source to the load?'),
    'e1-f25-q2': question('Transmission Lines and Superconducting Qubits',
        r'''In superconducting quantum computers, (microwave) voltage pulses are sent down transmission lines to perform operations on qubits. Consider one such transmission line with the following parameters:
• Per-length inductance: $l=400\,\mathrm{nH/m}$
• Per-length capacitance: $c=160\,\mathrm{pF/m}$
• Transit time (delay): $T_d=10\,\mathrm{ns}$
At time $t=0$, the voltage source sends a single DC pulse with amplitude $3\,\mathrm{V}$ and duration $1\,\mathrm{ns}$ down the transmission line toward the load. Due to damage to the circuit, the values of the source impedance and load impedance have increased from their originally designed values to $R_g=100\,\Omega$ and $R_L=200\,\Omega$, as shown in the circuit schematic below.''',
        'Calculate the characteristic impedance of the transmission line.',
        r'What is the initial amplitude of the voltage pulse $V_1^+$ that makes it into the transmission line?',
        r'Sketch a bounce diagram for the voltage amplitude of the pulse for time $0\le t<4T$. Be sure to label both traveling voltage amplitudes and the amplitudes that would be measured at the load and the source. You do not need to calculate the total voltage at the source for $t=4T_d$.',
        r'What will be the voltage on the transmission line after an infinite number of bounces $(t\to\infty)$?'),
    'e1-f25-q3': question('Quarter Wave Transmission Lines',
        r'''The transmission line in the circuit below has a characteristic impedance $Z_0=50\Omega$ and length $L=\frac{\lambda}{4}$. The amplitude of the sinusoidal source voltage is $V_g=10\,\mathrm{V}$, its wavelength is $\lambda=20\,\mathrm{m}$ and its frequency is $f=100\,\mathrm{kHz}$.''',
        r'Calculate $Z_{in}$ for the transmission line.',
        r'Write down the phasor for the total voltage wave $\widetilde V(z)$ on the transmission line.',
        r'Convert your expression for $\widetilde V(z)$ to the time domain $v(z,t)$.',
        r'In order to deliver maximum power to the load, you would need to find a transmission line with the same length $(L=\lambda/4)$, but with a different characteristic impedance. What would the characteristic impedance of this new transmission line need to be?',
        'Even though the transmission line you chose in part (d) delivers maximum power to the load in steady state, reflections will still occur on the transmission line at the load. How can there be maximum power transfer, but also reflections on the transmission line?'),
    'e1-f25-q4': question('Single Stub Matching',
        r'''You have been asked to match the load impedance $Z_L=150+j75\,\Omega$ to a feedline with characteristic impedance $Z_0=75\,\Omega$ by using an open-circuited transmission line stub. A diagram of the single-stub matching circuit is shown below. A Smith chart is attached to the back of your exam for recording your answers. A ruler will also be provided.''',
        'Calculate the normalized load impedance and plot it on the Smith chart.',
        'Plot the normalized load admittance on the Smith chart and show how you determined it from the plotted normalized load impedance. Write down the normalized load admittance you found from the Smith chart.',
        r'Calculate the distance $d_1$ (in terms of wavelength) from the load where the open-circuited stub should be placed, and give the input admittance $y_d$ of the transmission line at that point. Show all necessary work on the Smith chart for how you determined this value.',
        r'Calculate the length $l_1$ (in terms of wavelength) of the stub needed to match the source, and give the input admittance $y_s$ of the open-circuited stub of that length. Show all necessary work on the Smith chart for how you determined this value.'),
    'e1-s26-q1': question('Low-Loss Transmission Line Model',
        r'''You are given a spool of coaxial cable of length $L=100\mathrm{m}$ and are tasked with determining its properties through measurements. A diagram of your measurement setup is shown below. Assume the coaxial cable can be treated as a low-loss transmission line.''',
        r'You measure the time delay of your cable to be $T_d=392\mathrm{ns}$. What is the velocity factor of the coaxial cable?',
        r'You measure the amplitude of the voltage at the input to the coaxial cable $V_{in}$ to be $1\mathrm{V}$ for any frequency you set for $V_g$. What is the characteristic impedance $Z_0$ of the cable?',
        r'Calculate the wavelength $\lambda$ of the voltage wave on the coaxial cable if the frequency of the generator is $f=100\mathrm{MHz}=100\times10^6\,\mathrm{Hz}$.',
        r'Calculate the per-unit-inductance $l$ and per-unit-capacitance $c$ of the coaxial cable.',
        r'If you measure the amplitude of the voltage at the load to be $V(L=100\mathrm{m})=0.904\mathrm{V}$ and the amplitude of the voltage at the input to be $V(L=0\mathrm{m})=1\mathrm{V}$, determine the attenuation coefficient $\alpha$.',
        r'Calculate the per-unit-length resistance $r$ of the coaxial cable.'),
    'e1-s26-q2': question('Transient Analysis',
        r'''A transmission line of characteristic impedance $Z_0=50\Omega$ and time delay $T_d=50\mathrm{ps}$ is connected between a generator circuit with voltage $V_g=10\mathrm{V}$ and generator impedance $R_g=30\Omega$, and a load impedance $Z_L=150\Omega$, as shown below. The switch closes at time $t=0$ and provides a DC voltage to the transmission line.''',
        r'''Calculate the following quantities:
• The reflection coefficient at the load $\Gamma_L$
• The reflection coefficient at the generator $\Gamma_g$''',
        r'Calculate numerical values for $V_1^+$, $V_1^-$, $V_2^+$ and $V_2^-$ in the bounce diagram below.',
        r'Sketch a plot of the voltage at the load $V(z=L)$ vs. time for $0\le t\le150\mathrm{ps}$. Label voltage amplitudes and critical times, such as when the voltage wave undergoes relevant reflections.',
        r'Calculate the voltage on the transmission line after it has reached steady state $V_{ss}$.'),
    'e1-s26-q3': question('Input Impedance',
        r'''For all circuits in this problem, the frequency of the generator voltage is $f=200\mathrm{MHz}=200\times10^6\mathrm{Hz}$ and the velocity factor of all coaxial cables is $0.65$. In each part, provide a numerical answer with units.''',
        r'''For part a) only: you have access to spools of coaxial cable with characteristic impedances:
• Cable type #1: $Z_{01}=25\Omega$
• Cable type #2: $Z_{02}=50\Omega$
• Cable type #3: $Z_{03}=75\Omega$
In each of the circuits below, specify the type of cable (which characteristic impedance $Z_0$) and length $L$ that match the generator impedance to the load impedance.

Circuit #1''',
        'Circuit #2',
        r'Determine $Z_{in}$ for the circuit below.',
        r'In the circuit below, what length of open-circuited cable $\ell$ would lead to full reflection of the voltage wave at $z=A$?'),
    'e1-s26-q4': question('Single-Stub Matching with a Smith Chart',
        r'''Use the included Smith chart to match the feedline’s characteristic impedance $Z_0$ to the load impedance $Z_L$ via the single-stub matching method. As shown below, the matching circuit consists of a through-line of length $d$, which is connected to the load and an open-circuited stub of length $\ell$, connected in parallel with the through-line. $Z_0=50\Omega$ for all transmission lines in this problem.''',
        r'Calculate the normalized load impedance $z_L$ and plot it on the Smith chart.',
        r'Determine and plot the location of the normalized load admittance $y_L$ on the Smith chart, then read off its numerical value.',
        r'Determine the length of the through-line $d$ that yields an input admittance whose real part is matched to the characteristic admittance $Y_0=1/Z_0$ (i.e. $y_d=1+jA$). Show all work for how you determined this length on the Smith chart. You may leave your answer in terms of wavelengths.',
        r'Determine the length of the open-circuited stub $\ell$ that completes the impedance match. Show all work for how you determined this length on the Smith chart. You may leave your answer in terms of wavelengths.'),
    'e1-f26-q1': question('Transmission Line Fundamentals',
        r'''The transmission line model below consists of segments of length $\Delta z\ll\lambda$ and the following circuit element parameters:
• $l=0.3125\,\mathrm{\mu H/m}=3.125\times10^{-7}\,\mathrm{H/m}$
• $c=55.6\,\mathrm{pF/m}=5.56\times10^{-11}\,\mathrm{F/m}$''',
        'Is the transmission line that is represented by the model above a lossy transmission line or a lossless transmission line? Briefly explain.',
        'Calculate the velocity factor and characteristic impedance of the transmission line.',
        r'If the transmission line length is $L=60\mathrm{m}$, calculate the time delay $T_d$ of the transmission line.',
        r'''Now consider the DC circuit below, which contains a switch that closes at $t=0$, and a transmission line with the same properties as specified by the model in part a).

For the bounce diagram below, calculate the following parameters:
• All reflection coefficients
• All voltage amplitudes
• The voltage at the load $V_L$ at $t=T_d$
• The voltage at the input to the transmission line $V_{in}$ at $t=2T_d$'''),
    'e1-f26-q2': question('Damaged Transmission Line',
        r'''The transmission line in Circuit A below has been damaged, resulting in an abrupt change in its characteristic impedance at a point somewhere along the transmission line.

We can model Circuit A above by replacing the transmission line between the point of the damage and the load by an effective input impedance $Z_{\mathrm{eff}}$, as shown in Circuit B below.

Using a directional coupler, it has been determined that the steady-state forward-traveling voltage wave on the transmission line between its input and $Z_{\mathrm{eff}}$ in Circuit B is given by the phasor $\widetilde V^+(z)=5e^{-j2\pi z}\,\mathrm{V}$, and the backward-traveling voltage wave is given by the phasor $\widetilde V^-(z)=3e^{j2\pi z}\,\mathrm{V}$.''',
        r'Write the expression for the total voltage wave on the transmission line between its input and $Z_{\mathrm{eff}}$ in the time domain.',
        r'Calculate the reflection coefficient between the transmission line and $Z_{\mathrm{eff}}$.',
        'Calculate the standing wave ratio.',
        'Calculate the maximum voltage on the transmission line. How does this voltage compare with the maximum voltage on the transmission line when Circuit A is undamaged? Briefly explain.',
        r'Calculate the time-average power delivered to $Z_{\mathrm{eff}}$. How does this delivered power compare with the power delivered to the load when Circuit A is undamaged? Briefly explain.',
        r'Calculate the value of the impedance $Z_{\mathrm{eff}}$. Did the damage to the transmission line increase or decrease its characteristic impedance at that location?'),
    'e1-f26-q3': question('Impedance Matching',
        r'''In each of the cases below:
1. Calculate $Z_{in}$.
2. State whether or not the generator circuit sees a matched load.
Briefly justify your answer using a transmission line property or impedance matching method. Answers relying solely on the general mathematical equation for $Z_{in}$ will receive reduced credit.''',
        r'The generator circuit is connected to the load via a transmission line of length $L=\lambda/6$ and characteristic impedance $Z_0=50\Omega$.',
        r'The generator circuit is connected to the load via a transmission line of length $L=\lambda/2$ and characteristic impedance $Z_0=50\Omega$.',
        r'The generator circuit is connected to the load via a transmission line of length $L=\lambda/4$ and characteristic impedance $Z_0=50\Omega$.',
        r'''The generator circuit is connected to a feedline of characteristic impedance $Z_0=50\Omega$. The feedline is connected to the parallel combination of two other transmission lines:
• a line of length $d$, input admittance $Y_d$, and terminating impedance $Z_L$
• a line of length $l$, input admittance $Y_s$, and an open-circuit termination'''),
    'e1-f26-q4': question('Impedance Matching with a Smith Chart',
        r'''The load in the circuit below is to be matched to a $Z_0=50\Omega$ feedline using a quarter-wave transformer of characteristic impedance $Z_{0T}$ and a length of transmission line $d$ of characteristic impedance $Z_0$. The velocity factor of the transmission line of length $d$ is $0.85$ and the frequency of the signal on the line is $f=100\,\mathrm{MHz}=100\times10^6\,\mathrm{Hz}$.''',
        'Calculate the normalized load impedance. Plot it on the Smith chart.',
        r'What are the two values of purely real input impedance $Z_{in,d}$ that the transmission line of length $d$ could present? Show your work on the Smith chart. Give your impedances in unnormalized format.',
        r'Choose one of the two values of $Z_{in,d}$ from part b). How long $d$ (in meters) must the transmission line be to present your chosen input impedance $Z_{in,d}$? Show your work on the Smith chart.',
        r'For the case you chose in part c), find the characteristic impedance $Z_{0T}$ of the quarter-wave transformer that matches the load network to the $Z_0=50\Omega$ feedline.',
        r'''Once the transmission line and load are matched to the feedline, maximum power will be transferred from the generator to the load in steady state. Where do reflections still occur in the system?
Circle all that apply.

a. At the interface between the feedline and the input to the $L=\lambda/4$ line.
b. At the interface between the $L=\lambda/4$ line and the input to the line of length $d$.
c. At the interface between the line of length $d$ and the load $Z_L$.
d. No reflections occur anywhere in the system since the feedline is matched to the load.'''),
    'e2-f25-q1': question('Gauss’s Law with Spherical Symmetry',
        r'''In this problem, you will use Gauss’s law to solve for the electric field in each region.

The system below consists of:
• A sphere of constant volumetric charge density $\rho_0$ and radius $a$.
• A conducting shell of radius $b$ and surface charge density $\rho_{sb}$.

The total charge on the conducting shell is equal in magnitude to the total charge contained in the sphere, but opposite in sign. The region $a<r<b$ contains no free charge $\rho$ and the permittivity is $\varepsilon_0$.

Note: All diagrams must include the shape and position of the Gaussian surface used in your solution.''',
        r'Draw the diagram you will use for finding the electric field in the region $0<r<a$.',
        r'Find the electric field in the region $0<r<a$.',
        r'Draw the diagram you will use for finding the electric field in the region $a\le r\le b$.',
        r'Find the electric field in the region $a\le r\le b$.',
        r'Draw the diagram you will use for finding the electric field in the region $r>b$.',
        r'Find the electric field in the region $r>b$.',
        r'If you were to replace the material in the region $a<r<b$ by a dielectric with $\varepsilon>\varepsilon_0$, how would this affect the potential difference between $r=b$ and $r=a$? Explain this change in the context of electric materials and polarization.'),
    'e2-f25-q2': question('Parallel Plate Capacitor with Two Dielectrics',
        r'''In the system below, the space between two conducting plates located at $x=0$ and $x=L$ is filled with two different dielectrics:
• Region 1 occupies the space $\frac{H}{2}<z\le H$ and has permittivity $\varepsilon_1$.
• Region 2 occupies the space $0\le z<H/2$ and has permittivity $\varepsilon_2$.

The plate at $x=0$ is held at a constant potential $V_0$, while the plate at $x=L$ is held at a constant potential $V_1$. The plates have height $H$ in the z-dimension and depth $W$ in the y-direction.
The electric field in region 1 is given by $\vec E_1(x)=\frac{V_1-V_0}{L}\hat x$.''',
        r'Find the electric field, $\vec E_2(x)$, and displacement field, $\vec D_2(x)$, in region 2. Ignore fringing effects.',
        'Using your results from part a), find the total electric energy stored in the region between the conducting plates.',
        'Find the capacitance of the system using the total stored electric energy method.',
        'Bonus: Does your result in part c) agree with how parallel capacitances combine according to circuit theory? Explain.'),
    'e2-f25-q3': question('Coaxial Cable – Laplace’s Equation',
        r'''The coaxial cable below consists of a grounded, inner conductor of radius $a$ and an outer conducting shell of radius $b$, which is held at a constant potential $-V_0$. The space between the conductors $a<r<b$ has no free charge and is filled by a dielectric with permittivity $\varepsilon$.''',
        r'Use Laplace’s or Poisson’s equation to find $V(\vec r)$ in the region $a\le r\le b$.',
        r'Find the displacement field $\vec D(\vec r)$ in the region $a\le r\le b$.',
        'Find the charge density on the inner and outer conductors.',
        'Find the capacitance per unit length of the coaxial cable.'),
    'e2-f25-q4': question('Superposition of Electric Fields',
        r'''Two conducting spheres of radius $a$ are located on the x-axis: One sphere is located at $x=-d$ and has total surface charge $Q$, while the other sphere is located $x=d$ and has total surface charge $-Q$.
A diagram of this system is shown below.''',
        r'First, consider a conducting sphere of radius $a$ and total surface charge $Q$ located at the origin. Find the electric field due to this sphere for $r>a$ (outside the sphere).',
        r'Find the total electric field due to both of the conducting spheres in the figure above at the observation point $P=(0,0,z)$. You must express your answer in terms of cartesian coordinates.',
        r'A point charge with charge $-Q$ is now placed at observation point $P$. What is the force on the point charge due to the two conducting spheres?',
        r'Set up an integral for calculating the potential difference between the origin $O=(0,0,0)$ and the observation point $P=(0,0,z)$. You do not need to solve it!',
        'In electrostatics, does the path of integration matter when calculating potential differences? Which of Maxwell’s equations for electrostatics tells us this?'),
    'e2-s26-q1': question('Resistance of a Microstrip Line at High Frequencies',
        r'''As discussed in class, due to the skin effect, current prefers to flow closer to the surfaces of a conductor at higher frequencies. Consider the microstrip line below, which has the following properties:
• Width (in y-dimension): $W$
• Height (in z-dimension): $h$
• Length (in x-dimension): infinite
• Conductivity: $\sigma$

The current density distribution in the microstrip line is given by:
$$\vec J(z)=\begin{cases}J_0\hat x&\text{for }0.4h\le z<0.5h\\0&\text{for }-0.4h<z<0.4h\\J_0\hat x&\text{for }-0.5h<z\le-0.4h\end{cases}$$
Ignore any electric field fringing effects due to the finite width of the microstrip line.''',
        r'Calculate the total current $I$ flowing through the microstrip line.',
        r'Calculate the magnitude of the potential drop per unit length $V^{\prime}$ of the microstrip line.',
        r'Calculate the resistance per unit length $R^{\prime}$ of the microstrip line.',
        r'For the same current density as above, use physical reasoning to explain why increasing the conductivity $\sigma$ would lead to a decrease in the resistance of the microstrip line.',
        'For the same total current flowing through the microstrip line, how would the resistance of the microstrip line differ if the current density were distributed uniformly over the cross-section instead of being concentrated near the surfaces? Briefly explain using physical reasoning.'),
    'e2-s26-q2': question('Electrostatic Boundary Conditions',
        r'''Shown below is a stack of three dielectric materials:
• Dielectric 1: occupies the region $y>0.01\,\mathrm{m}$ and has permittivity $\varepsilon_1=2\varepsilon_0$
• Dielectric 2: occupies the region $0<y<0.01\,\mathrm{m}$ and has permittivity $\varepsilon_2=5\varepsilon_0$
• Dielectric 3: occupies the region $y<0$ and has permittivity $\varepsilon_3=2\varepsilon_0$

The electric field in dielectric 1 is given by:
$$\vec E_1=100\hat x-100\hat y$$''',
        r'Find the electric field in dielectric 2, $\vec E_2$.',
        r'Find the electric field in dielectric 3, $\vec E_3$.',
        r'Calculate the total potential difference across dielectric 2, $V_0$, (i.e. between $y=0.01\,\mathrm{m}$ and $y=0$).',
        'Using the concept of polarization in dielectric materials, briefly explain why the magnitude of the electric field in dielectric 2 is different from the magnitudes of the electric fields in dielectric 1 and dielectric 3. Be sure to comment on the relative magnitudes: why is one larger/smaller than the others?'),
    'e2-s26-q3': question('Leaky Coaxial Cable Dielectric',
        r'''The coaxial cable to the right has a poor dielectric, which has allowed some charge to leak between the inner conductor and outer conductor. The cable has an inner conductor of radius $a$ with surface charge density $\rho_{sa}$ and an outer conducting shell of radius $b$, held at a potential $V(b)=0$. The region $a<r<b$ is filled with a dielectric of permittivity $\varepsilon$ and volumetric charge density given by:
$$\rho(r)=\rho_0\frac{a}{r}$$''',
        r'Using Gauss’s law, find the electric field $\vec E(\vec r)$ in the region $a<r<b$. Include a diagram that shows the location of your Gaussian surface.',
        r'Find the potential $V(\vec r)$ in the region $a<r<b$.',
        r'Find the potential difference between the conductors, $V_0=V(a)-V(b)$. Then, express the surface charge density on the inner conductor, $\rho_{sa}$, as a function of $V_0$ and $\rho_0$.',
        r'When a volumetric charge density exists in the region between two conductors, the capacitance cannot be computed using the usual formulas. Instead, it must be defined by $C=\frac{dQ}{dV_0}$, where $Q$ is the total charge on one conductor and $V_0$ is the potential difference between the conductors. Using this definition and your results from earlier parts, determine the capacitance per unit length $C^{\prime}$ of the cable.'),
    'e2-s26-q4': question('Point Charges over a Conducting Plane',
        r'''Two immobile point charges are held at a height $z_0$ above a perfectly conducting plane that occupies the region $z<0$. A point charge $-q$ is located at $(-x_0,0,z_0)$ and a charge $+q$ is located at $(x_0,0,z_0)$. The region above the conductor $(z>0)$ has permittivity $\varepsilon_0$.''',
        r'Draw a diagram in the x-z plane showing the geometry you will use for applying the method of images. Include the real charges, their image charges, their coordinates, and clearly mark the position of the conducting surface.',
        r'In a new diagram, sketch the electric field lines between the charges you drew in part a), including those in the region $z<0$.',
        r'Determine the electric field $\vec E_{+q}$ at a point $P=(x,0,0)$ solely due to the point charge $+q$ located at $(x_0,0,z_0)$, ignoring the conducting plane.',
        r'Determine the total electric field $\vec E_{tot}$ at the point $P=(x,0,0)$ on the surface of the conductor, taking into account both real charges and the effect of the conducting plane.',
        r'Using your result from part d), calculate the surface charge density $\rho_s(\vec r)$ on the conductor at the point $P=(x,0,0)$.')
}


def apply_original_questions(exams):
    """Leave derivations intact; use the PDF's words for every question."""
    seen = set()
    for exam in exams:
        for problem in exam['problems']:
            original = ORIGINAL_QUESTIONS[problem['id']]
            assert len(problem['parts']) == len(original['parts']), problem['id']
            problem['title']['en'] = original['title']
            problem['statement']['en'] = original['statement']
            problem['wording'] = 'original'
            for part, prompt in zip(problem['parts'], original['parts']):
                part['prompt']['en'] = prompt
                if part['label'] == 'rf':
                    # Preserve its saved-progress ID while restoring the printed label.
                    part['label'] = 'f'
            seen.add(problem['id'])
    assert seen == ORIGINAL_QUESTIONS.keys()
