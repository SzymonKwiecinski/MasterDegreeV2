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

\section*{Rocket Dynamics Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \), which is under our control.
\end{itemize}

\textbf{Dynamics Model:}
The dynamics of the rocket can be described by the following equations:
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

\textbf{Initial Conditions:}
The initial conditions are given as:
\begin{align*}
    x_0 &= \text{initial position} \\
    v_0 &= \text{initial velocity}
\end{align*}

\textbf{Target Conditions:}
We wish to reach the target position \( x_T \) with target velocity \( v_T \) at time \( T \):
\begin{align*}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align*}

\textbf{Objective Function:}
The objective is to minimize the total fuel consumed:
\[
\text{Minimize } \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Constraints:}
The variables must satisfy the following constraints:
\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1 \\
    x_0 &= \text{given} \\
    v_0 &= \text{given} \\
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

\textbf{Output:}
The output consists of:
\begin{itemize}
    \item A list of positions: \( x = [x_i \text{ for } i = 0, 1, \ldots, T] \)
    \item A list of velocities: \( v = [v_i \text{ for } i = 0, 1, \ldots, T] \)
    \item A list of accelerations: \( a = [a_i \text{ for } i = 0, 1, \ldots, T] \)
    \item Total fuel spent: \( \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t| \)
\end{itemize}

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

\section*{Rocket Dynamics Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \), which is under our control.
\end{itemize}

\textbf{Dynamics Model:}
The dynamics of the rocket can be described by the following equations:
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

\textbf{Initial Conditions:}
The initial conditions are given as:
\begin{align*}
    x_0 &= \text{initial position} \\
    v_0 &= \text{initial velocity}
\end{align*}

\textbf{Target Conditions:}
We wish to reach the target position \( x_T \) with target velocity \( v_T \) at time \( T \):
\begin{align*}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align*}

\textbf{Objective Function:}
The objective is to minimize the total fuel consumed:
\[
\text{Minimize } \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Constraints:}
The variables must satisfy the following constraints:
\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1 \\
    x_0 &= \text{given} \\
    v_0 &= \text{given} \\
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

\textbf{Output:}
The output consists of:
\begin{itemize}
    \item A list of positions: \( x = [x_i \text{ for } i = 0, 1, \ldots, T] \)
    \item A list of velocities: \( v = [v_i \text{ for } i = 0, 1, \ldots, T] \)
    \item A list of accelerations: \( a = [a_i \text{ for } i = 0, 1, \ldots, T] \)
    \item Total fuel spent: \( \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t| \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Problem definition
T = data['TotalTime']
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Dynamics_Optimization", pulp.LpMinimize)

#### Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

#### Objective function: minimize total fuel consumed
problem += pulp.lpSum([pulp.lpSum([a[t], -a[t]]) for t in range(T)])

#### Initial conditions
x[0] = x0
v[0] = v0

#### Dynamics constraints
for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

#### Target conditions
problem += x[T] == xT
problem += v[T] == vT

#### Solve the problem
problem.solve()

#### Output results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

#### Total fuel spent
fuel_spent = sum(abs(acc) for acc in accelerations)

#### Print results
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelerations: {accelerations}')
print(f'Fuel spent: {fuel_spent}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

