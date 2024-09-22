# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Consider a rocket that travels along a straight path. 
- Let \var{x_t}, \var{v_t}, and \var{a_t} be the position, velocity, and acceleration, respectively, of the rocket at time \var{t}.
- By discretizing time and by taking the time increment to be unity, we obtain an approximate discrete-time model of the form 
    
    \var{x_{t+1}} = \var{x_t} + \var{v_t}
    \var{v_{t+1}} = \var{v_t} + \var{a_t}

- We assume that the acceleration \var{a_t} is under our control, as it is determined by the rocket thrust.
- In a rough model, the magnitude |\var{a_t}| of the accelera­tion can be assumed to be proportional to the rate of fuel consumption at time \var{t}.
- Suppose that we have \var{x_0} and \var{v_0} as the initial position and velocity, respectively, of the rocket.
- We wish the rocket to take off and reach a target position \var{x_T} with speed \var{v_T} at time \var{T}.
- Furthermore, we wish to accomplish this in an economical fashion, that is, by using as little fuel as possible.


INPUT FORMAT: 

{
    "x_0": x_0,
    "v_0": v_0,
    "x_T": x_T,
    "v_T": v_T,
    "T": T
}

OBJECTIVE: The objective is to minimize the maximum thrust required, which is max_t |a_t|. 

OUTPUT INFO:

- key "x" contains a list of the positions of the rocket at each time step from 0 to \var{T}
- key "v" contains a list of the velocities of the rocket at each time step from 0 to \var{T}
- key "a" contains a list of the accelerations of the rocket at each time step from 0 to \var{T}
- key "fuel_spend" contains the total fuel spent by the rocket

OUTPUT FORMAT:

{
    "x": [x_i for i in 1, ..., T],
    "v": [v_i for i in 1, ..., T],
    "a": [a_i for i in 1, ..., T],
    "fuel_spend": fuel_spent,
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Motion Optimization Model}

Given the discrete-time model for the rocket's motion:

\begin{align}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t,
\end{align}

where \(x_t\), \(v_t\), and \(a_t\) represent the position, velocity, and acceleration of the rocket at time \(t\), respectively, we wish to optimize the rocket's flight to reach a target position and velocity at a specified time.

\subsection*{Parameters}
Let the inputs be defined as follows:

\begin{itemize}
    \item \(x_0\): Initial position of the rocket
    \item \(v_0\): Initial velocity of the rocket
    \item \(x_T\): Target position
    \item \(v_T\): Target velocity
    \item \(T\): Time at which the targets are to be achieved
\end{itemize}

\subsection*{Objective}
We aim to minimize the maximum thrust required during the rocket's flight, represented mathematically as:

\[
\text{Minimize } \max_t |a_t|
\]

\subsection*{Constraints}
The position and velocity must satisfy the following constraints at each time step \(t\):

\begin{align}
    x_0 &= x_0, \\
    v_0 &= v_0, \\
    x_{T} &= x_T, \\
    v_{T} &= v_T.
\end{align}

Additionally, the relationship between subsequent states is given by the equations of motion:

\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \dots, T-1, \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \dots, T-1.
\end{align}

\subsection*{Output}
The solution to the optimization problem will yield:

\begin{itemize}
    \item A list of positions: \(\{x_i\}_{i=0}^{T}\)
    \item A list of velocities: \(\{v_i\}_{i=0}^{T}\)
    \item A list of accelerations: \(\{a_i\}_{i=0}^{T}\)
    \item Total fuel spent: \(fuel\_spent\)
\end{itemize}

The output format will be:

\[
\{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel\_spend": fuel\_spent,
\}
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Motion Optimization Model}

Given the discrete-time model for the rocket's motion:

\begin{align}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t,
\end{align}

where \(x_t\), \(v_t\), and \(a_t\) represent the position, velocity, and acceleration of the rocket at time \(t\), respectively, we wish to optimize the rocket's flight to reach a target position and velocity at a specified time.

\subsection*{Parameters}
Let the inputs be defined as follows:

\begin{itemize}
    \item \(x_0\): Initial position of the rocket
    \item \(v_0\): Initial velocity of the rocket
    \item \(x_T\): Target position
    \item \(v_T\): Target velocity
    \item \(T\): Time at which the targets are to be achieved
\end{itemize}

\subsection*{Objective}
We aim to minimize the maximum thrust required during the rocket's flight, represented mathematically as:

\[
\text{Minimize } \max_t |a_t|
\]

\subsection*{Constraints}
The position and velocity must satisfy the following constraints at each time step \(t\):

\begin{align}
    x_0 &= x_0, \\
    v_0 &= v_0, \\
    x_{T} &= x_T, \\
    v_{T} &= v_T.
\end{align}

Additionally, the relationship between subsequent states is given by the equations of motion:

\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \dots, T-1, \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \dots, T-1.
\end{align}

\subsection*{Output}
The solution to the optimization problem will yield:

\begin{itemize}
    \item A list of positions: \(\{x_i\}_{i=0}^{T}\)
    \item A list of velocities: \(\{v_i\}_{i=0}^{T}\)
    \item A list of accelerations: \(\{a_i\}_{i=0}^{T}\)
    \item Total fuel spent: \(fuel\_spent\)
\end{itemize}

The output format will be:

\[
\{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel\_spend": fuel\_spent,
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

#### Objective function: minimize maximum thrust (acceleration)
max_thrust = pulp.LpVariable('max_thrust', lowBound=0)
problem += max_thrust

#### Constraints
problem += x[0] == x0
problem += v[0] == v0
problem += x[T] == xT
problem += v[T] == vT

#### Motion equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_thrust
    problem += a[t] >= -max_thrust

#### Solve the problem
problem.solve()

#### Collect results
x_sol = [pulp.value(x[t]) for t in range(T + 1)]
v_sol = [pulp.value(v[t]) for t in range(T + 1)]
a_sol = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust)

#### Output the results in the specified format
output = {
    "x": x_sol,
    "v": v_sol,
    "a": a_sol,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

