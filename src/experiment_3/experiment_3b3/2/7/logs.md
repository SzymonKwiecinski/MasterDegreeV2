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

\section*{Rocket Trajectory Optimization Model}

We define the variables involved in the problem:

\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \).
    \item The initial position and velocity are given as \( x_0 \) and \( v_0 \).
    \item The target position and velocity at time \( T \) are given as \( x_T \) and \( v_T \).
\end{itemize}

The dynamical equations governing the motion of the rocket are given by:

\[
\begin{aligned}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t.
\end{aligned}
\]

The objective is to minimize the maximum thrust required, which is represented as:

\[
\text{minimize} \quad \max_{t} |a_t|.
\]

Subject to the following constraints for \( t = 0, 1, 2, \ldots, T-1 \):

\[
\begin{aligned}
    x_0 &= x_0, \\
    v_0 &= v_0, \\
    x_T &= x_T, \\
    v_T &= v_T, \\
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t.
\end{aligned}
\]

The total fuel spent, denoted as \( \text{fuel\_spent} \), is proportional to the total acceleration applied, which can be represented as:

\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|.
\]

The expected output format after solving the optimization problem will be:

\[
\{
    x: [x_i \text{ for } i = 0, 1, \ldots, T],
    v: [v_i \text{ for } i = 0, 1, \ldots, T],
    a: [a_i \text{ for } i = 0, 1, \ldots, T],
    fuel\_spend: \text{fuel\_spent},
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

\section*{Rocket Trajectory Optimization Model}

We define the variables involved in the problem:

\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \).
    \item The initial position and velocity are given as \( x_0 \) and \( v_0 \).
    \item The target position and velocity at time \( T \) are given as \( x_T \) and \( v_T \).
\end{itemize}

The dynamical equations governing the motion of the rocket are given by:

\[
\begin{aligned}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t.
\end{aligned}
\]

The objective is to minimize the maximum thrust required, which is represented as:

\[
\text{minimize} \quad \max_{t} |a_t|.
\]

Subject to the following constraints for \( t = 0, 1, 2, \ldots, T-1 \):

\[
\begin{aligned}
    x_0 &= x_0, \\
    v_0 &= v_0, \\
    x_T &= x_T, \\
    v_T &= v_T, \\
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t.
\end{aligned}
\]

The total fuel spent, denoted as \( \text{fuel\_spent} \), is proportional to the total acceleration applied, which can be represented as:

\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|.
\]

The expected output format after solving the optimization problem will be:

\[
\{
    x: [x_i \text{ for } i = 0, 1, \ldots, T],
    v: [v_i \text{ for } i = 0, 1, \ldots, T],
    a: [a_i \text{ for } i = 0, 1, \ldots, T],
    fuel\_spend: \text{fuel\_spent},
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Unpack data
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]
max_thrust = pulp.LpVariable('max_thrust', lowBound=0, cat='Continuous')

#### Objective
problem += max_thrust

#### Initial and final conditions
problem += (x[0] == x0)
problem += (v[0] == v0)
problem += (x[T] == xT)
problem += (v[T] == vT)

#### Dynamical equations and thrust constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] <= max_thrust)
    problem += (-a[t] <= max_thrust)

#### Solve
problem.solve()

#### Calculate fuel spent
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

#### Collect results
result = {
    'x': [pulp.value(x[t]) for t in range(T + 1)],
    'v': [pulp.value(v[t]) for t in range(T + 1)],
    'a': [pulp.value(a[t]) for t in range(T)],
    'fuel_spend': fuel_spent,
}

#### Output
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

