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

OBJECTIVE: The objective is to minimize the total fuel \sum_{t=0}^{\var{T}-1} |\var{a_t}| spent subject to the preceding constraints.

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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) denote the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

Assuming that the acceleration \( a_t \) is under our control and is proportional to the rate of fuel consumption, we aim to minimize the total fuel used over a time horizon from \( t = 0 \) to \( t = T-1 \). 

Given the inputs:
\begin{itemize}
    \item Initial position: \( x_0 \)
    \item Initial velocity: \( v_0 \)
    \item Target position: \( x_T \)
    \item Target velocity: \( v_T \)
    \item Total time steps: \( T \)
\end{itemize}

The optimization problem can be formulated as follows:

\textbf{Objective:}
Minimize the total fuel consumption:
\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1 \\
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
\end{align*}

\textbf{Output:}
The solution includes:
\begin{itemize}
    \item \( x \): positions of the rocket at each time step from \( 0 \) to \( T \)
    \item \( v \): velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item \( a \): accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item \( \text{fuel\_spend} \): total fuel spent by the rocket
\end{itemize}

The output format will be:
\[
\{ 
    "x": [x_i \, | \, i = 1, \ldots, T], 
    "v": [v_i \, | \, i = 1, \ldots, T], 
    "a": [a_i \, | \, i = 1, \ldots, T], 
    "fuel\_spend": \text{fuel\_spent} 
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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) denote the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

Assuming that the acceleration \( a_t \) is under our control and is proportional to the rate of fuel consumption, we aim to minimize the total fuel used over a time horizon from \( t = 0 \) to \( t = T-1 \). 

Given the inputs:
\begin{itemize}
    \item Initial position: \( x_0 \)
    \item Initial velocity: \( v_0 \)
    \item Target position: \( x_T \)
    \item Target velocity: \( v_T \)
    \item Total time steps: \( T \)
\end{itemize}

The optimization problem can be formulated as follows:

\textbf{Objective:}
Minimize the total fuel consumption:
\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1 \\
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
\end{align*}

\textbf{Output:}
The solution includes:
\begin{itemize}
    \item \( x \): positions of the rocket at each time step from \( 0 \) to \( T \)
    \item \( v \): velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item \( a \): accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item \( \text{fuel\_spend} \): total fuel spent by the rocket
\end{itemize}

The output format will be:
\[
\{ 
    "x": [x_i \, | \, i = 1, \ldots, T], 
    "v": [v_i \, | \, i = 1, \ldots, T], 
    "a": [a_i \, | \, i = 1, \ldots, T], 
    "fuel\_spend": \text{fuel\_spent} 
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create the problem variable
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

#### Objective function: Minimize total fuel consumption
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

#### Constraints
#### Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

#### State transition equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

#### Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

#### Solve the problem
problem.solve()

#### Collect results
result = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

#### Output the result
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

