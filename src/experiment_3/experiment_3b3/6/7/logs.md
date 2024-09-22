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

\section*{Mathematical Model for Rocket Motion}

Consider a rocket that travels along a straight path with the following variables:

\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$.
    \item $v_t$: Velocity of the rocket at time $t$.
    \item $a_t$: Acceleration of the rocket at time $t$.
\end{itemize}

The discretized equations of motion for the rocket can be expressed as:

\begin{align}
    x_{t+1} &= x_t + v_t \tag{1} \\
    v_{t+1} &= v_t + a_t \tag{2}
\end{align}

The acceleration $a_t$ is under our control, determined by the thrust of the rocket. We assume:

\[
|a_t| \propto \text{fuel consumption at time } t \tag{3}
\]

Given the initial conditions:

\begin{align*}
    x_0 & : \text{Initial position} \\
    v_0 & : \text{Initial velocity}
\end{align*}

The goal is to reach a target position $x_T$ with speed $v_T$ at time $T$, while minimizing the maximum thrust required:

\[
\text{Minimize } \max_{t} |a_t| \tag{4}
\]

The output required includes:

\begin{itemize}
    \item Key "x": A list of positions $[x_0, x_1, \ldots, x_T]$.
    \item Key "v": A list of velocities $[v_0, v_1, \ldots, v_T]$.
    \item Key "a": A list of accelerations $[a_0, a_1, \ldots, a_T]$.
    \item Key "fuel\_spend": Total fuel spent by the rocket.
\end{itemize}

The mathematical description of the output format is:

\[
\begin{aligned}
    \text{Output} &: \{ \\
    &\quad "x": [x_i \text{ for } i = 0, \ldots, T], \\
    &\quad "v": [v_i \text{ for } i = 0, \ldots, T], \\
    &\quad "a": [a_i \text{ for } i = 0, \ldots, T], \\
    &\quad "fuel\_spend": \text{total fuel spent} \\
    &\}
\end{aligned}
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

\section*{Mathematical Model for Rocket Motion}

Consider a rocket that travels along a straight path with the following variables:

\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$.
    \item $v_t$: Velocity of the rocket at time $t$.
    \item $a_t$: Acceleration of the rocket at time $t$.
\end{itemize}

The discretized equations of motion for the rocket can be expressed as:

\begin{align}
    x_{t+1} &= x_t + v_t \tag{1} \\
    v_{t+1} &= v_t + a_t \tag{2}
\end{align}

The acceleration $a_t$ is under our control, determined by the thrust of the rocket. We assume:

\[
|a_t| \propto \text{fuel consumption at time } t \tag{3}
\]

Given the initial conditions:

\begin{align*}
    x_0 & : \text{Initial position} \\
    v_0 & : \text{Initial velocity}
\end{align*}

The goal is to reach a target position $x_T$ with speed $v_T$ at time $T$, while minimizing the maximum thrust required:

\[
\text{Minimize } \max_{t} |a_t| \tag{4}
\]

The output required includes:

\begin{itemize}
    \item Key "x": A list of positions $[x_0, x_1, \ldots, x_T]$.
    \item Key "v": A list of velocities $[v_0, v_1, \ldots, v_T]$.
    \item Key "a": A list of accelerations $[a_0, a_1, \ldots, a_T]$.
    \item Key "fuel\_spend": Total fuel spent by the rocket.
\end{itemize}

The mathematical description of the output format is:

\[
\begin{aligned}
    \text{Output} &: \{ \\
    &\quad "x": [x_i \text{ for } i = 0, \ldots, T], \\
    &\quad "v": [v_i \text{ for } i = 0, \ldots, T], \\
    &\quad "a": [a_i \text{ for } i = 0, \ldots, T], \\
    &\quad "fuel\_spend": \text{total fuel spent} \\
    &\}
\end{aligned}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Creating the LP problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Variables
x = [pulp.LpVariable(f'x_{t}', cat=pulp.LpContinuous) for t in range(data['T'] + 1)]
v = [pulp.LpVariable(f'v_{t}', cat=pulp.LpContinuous) for t in range(data['T'] + 1)]
a = [pulp.LpVariable(f'a_{t}', cat=pulp.LpContinuous) for t in range(data['T'])]
max_thrust = pulp.LpVariable('max_thrust', lowBound=0, cat=pulp.LpContinuous)

#### Objective
problem += max_thrust, "Minimize maximum thrust"

#### Initial conditions
problem += (x[0] == data['X0'], "Initial position")
problem += (v[0] == data['V0'], "Initial velocity")

#### Constraints for motion equations
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t], f"Position at time {t+1}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity at time {t+1}")

#### Target constraints
problem += (x[data['T']] == data['XT'], "Target position")
problem += (v[data['T']] == data['VT'], "Target velocity")

#### Constraints on acceleration
for t in range(data['T']):
    problem += (a[t] <= max_thrust, f"Max thrust constraint (positive) at {t}")
    problem += (-a[t] <= max_thrust, f"Max thrust constraint (negative) at {t}")

#### Solve the problem
problem.solve()

#### Collect the results
result_x = [pulp.value(x[t]) for t in range(data['T'] + 1)]
result_v = [pulp.value(v[t]) for t in range(data['T'] + 1)]
result_a = [pulp.value(a[t]) for t in range(data['T'])]
fuel_spend = sum(abs(pulp.value(a[t])) for t in range(data['T']))

#### Output in required format
output = {
    "x": result_x,
    "v": result_v,
    "a": result_a,
    "fuel_spend": fuel_spend
}

print(output)

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

