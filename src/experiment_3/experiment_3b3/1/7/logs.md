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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The dynamics of the system can be described by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

The objective is to minimize the maximum thrust required, which can be expressed as:

\[
\text{minimize } \max_{t} |a_t|
\]

We are subject to the following constraints:

\begin{align*}
x_0 & = \text{initial position} \\
v_0 & = \text{initial velocity} \\
x_T & = \text{target position at time } T \\
v_T & = \text{target velocity at time } T \\
T   & = \text{total time}
\end{align*}

The optimization problem can be formulated as follows:

\begin{align*}
\text{Minimize} & \quad M \\
\text{Subject to:} & \\
x_{t+1} & = x_t + v_t \quad \forall t \in \{0, 1, \ldots, T-1\} \\
v_{t+1} & = v_t + a_t \quad \forall t \in \{0, 1, \ldots, T-1\} \\
|a_t| & \leq M \quad \forall t \in \{0, 1, \ldots, T-1\} \\
x_0 & = x_0 \\
v_0 & = v_0 \\
x_T & = x_T \\
v_T & = v_T
\end{align*}

The output of the model consists of:

\begin{itemize}
    \item A list of positions:
    \[
    x = [x_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item A list of velocities:
    \[
    v = [v_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item A list of accelerations:
    \[
    a = [a_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item Total fuel spent:
    \[
    \text{fuel\_spend} = \text{total fuel consumed}
    \]
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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The dynamics of the system can be described by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

The objective is to minimize the maximum thrust required, which can be expressed as:

\[
\text{minimize } \max_{t} |a_t|
\]

We are subject to the following constraints:

\begin{align*}
x_0 & = \text{initial position} \\
v_0 & = \text{initial velocity} \\
x_T & = \text{target position at time } T \\
v_T & = \text{target velocity at time } T \\
T   & = \text{total time}
\end{align*}

The optimization problem can be formulated as follows:

\begin{align*}
\text{Minimize} & \quad M \\
\text{Subject to:} & \\
x_{t+1} & = x_t + v_t \quad \forall t \in \{0, 1, \ldots, T-1\} \\
v_{t+1} & = v_t + a_t \quad \forall t \in \{0, 1, \ldots, T-1\} \\
|a_t| & \leq M \quad \forall t \in \{0, 1, \ldots, T-1\} \\
x_0 & = x_0 \\
v_0 & = v_0 \\
x_T & = x_T \\
v_T & = v_T
\end{align*}

The output of the model consists of:

\begin{itemize}
    \item A list of positions:
    \[
    x = [x_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item A list of velocities:
    \[
    v = [v_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item A list of accelerations:
    \[
    a = [a_i \text{ for } i = 0, 1, \ldots, T]
    \]
    \item Total fuel spent:
    \[
    \text{fuel\_spend} = \text{total fuel consumed}
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(data['T'] + 1), lowBound=None, cat='Continuous')
a = pulp.LpVariable.dicts("a", range(data['T']), lowBound=None, cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

#### Objective
problem += M, "Minimize maximum thrust"

#### Constraints
problem += (x[0] == data['X0']), "Initial position"
problem += (v[0] == data['V0']), "Initial velocity"
problem += (x[data['T']] == data['XT']), "Target position"
problem += (v[data['T']] == data['VT']), "Target velocity"

#### Dynamics constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t]), f"Position update at time {t}"
    problem += (v[t + 1] == v[t] + a[t]), f"Velocity update at time {t}"
    problem += (pulp.lpSum([a[t]]) <= M), f"Maximum thrust {t}"
    problem += (pulp.lpSum([-a[t]]) <= M), f"Minimum thrust {-t}"

#### Solve problem
problem.solve()

#### Output results
x_values = [pulp.value(x[t]) for t in range(data['T'] + 1)]
v_values = [pulp.value(v[t]) for t in range(data['T'] + 1)]
a_values = [pulp.value(a[t]) for t in range(data['T'])]
fuel_spend = sum(abs(av) for av in a_values)

print("Positions:", x_values)
print("Velocities:", v_values)
print("Accelerations:", a_values)
print("Fuel Spend:", fuel_spend)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

