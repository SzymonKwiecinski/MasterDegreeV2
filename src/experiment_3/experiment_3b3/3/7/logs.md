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

\section*{Rocket Motion Optimization Problem}

We are given a rocket that travels along a straight path, and we define the following variables at time \( t \):
\begin{itemize}
    \item \( x_t \): Position of the rocket
    \item \( v_t \): Velocity of the rocket
    \item \( a_t \): Acceleration of the rocket
\end{itemize}

The discrete-time dynamics of the rocket can be modeled as follows:
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Where the acceleration \( a_t \) is under our control, as it is determined by the rocket thrust. We assume that the magnitude \( |a_t| \) of the acceleration is proportional to the rate of fuel consumption at time \( t \).

Given the initial conditions:
\[
x_0, \quad v_0
\]
and the target conditions:
\[
x_T, \quad v_T \quad \text{at time} \quad T
\]

We formulate the objective of our optimization problem as minimizing the maximum thrust required, represented mathematically as:
\[
\text{Minimize } \max_{t} |a_t|
\]

The optimization will also be subject to the following constraints derived from the dynamics of the rocket:
\begin{align}
    x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity} \\
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

We will denote the total fuel spent as `fuel_spent`, which can be represented as:
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

The output will include:
\begin{itemize}
    \item key "x": A list of positions of the rocket at each time step from \( 0 \) to \( T \)
    \item key "v": A list of velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item key "a": A list of accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item key "fuel\_spend": Total fuel spent by the rocket
\end{itemize}

The output format will be as follows:
\[
\{
    "x": [x_i \text{ for } i = 0, 1, \ldots, T],
    "v": [v_i \text{ for } i = 0, 1, \ldots, T],
    "a": [a_i \text{ for } i = 0, 1, \ldots, T],
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

\section*{Rocket Motion Optimization Problem}

We are given a rocket that travels along a straight path, and we define the following variables at time \( t \):
\begin{itemize}
    \item \( x_t \): Position of the rocket
    \item \( v_t \): Velocity of the rocket
    \item \( a_t \): Acceleration of the rocket
\end{itemize}

The discrete-time dynamics of the rocket can be modeled as follows:
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Where the acceleration \( a_t \) is under our control, as it is determined by the rocket thrust. We assume that the magnitude \( |a_t| \) of the acceleration is proportional to the rate of fuel consumption at time \( t \).

Given the initial conditions:
\[
x_0, \quad v_0
\]
and the target conditions:
\[
x_T, \quad v_T \quad \text{at time} \quad T
\]

We formulate the objective of our optimization problem as minimizing the maximum thrust required, represented mathematically as:
\[
\text{Minimize } \max_{t} |a_t|
\]

The optimization will also be subject to the following constraints derived from the dynamics of the rocket:
\begin{align}
    x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity} \\
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

We will denote the total fuel spent as `fuel_spent`, which can be represented as:
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

The output will include:
\begin{itemize}
    \item key "x": A list of positions of the rocket at each time step from \( 0 \) to \( T \)
    \item key "v": A list of velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item key "a": A list of accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item key "fuel\_spend": Total fuel spent by the rocket
\end{itemize}

The output format will be as follows:
\[
\{
    "x": [x_i \text{ for } i = 0, 1, \ldots, T],
    "v": [v_i \text{ for } i = 0, 1, \ldots, T],
    "a": [a_i \text{ for } i = 0, 1, \ldots, T],
    "fuel\_spend": \text{fuel\_spent}
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Extracting data
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Define problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1))
v = pulp.LpVariable.dicts("v", range(T + 1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Auxiliary variables for thrust
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0)

#### Objective function: Minimize the maximum thrust required
max_abs_a = pulp.LpVariable("max_abs_a", lowBound=0)
problem += max_abs_a

#### Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_dynamics_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_dynamics_{t}"
    problem += abs_a[t] >= a[t], f"Positive_abs_a_{t}"
    problem += abs_a[t] >= -a[t], f"Negative_abs_a_{t}"
    problem += max_abs_a >= abs_a[t], f"Max_abs_a_constraint_{t}"

#### Initial conditions
problem += x[0] == X0, "Initial_position"
problem += v[0] == V0, "Initial_velocity"

#### Target conditions
problem += x[T] == XT, "Target_position"
problem += v[T] == VT, "Target_velocity"

#### Solve the problem
problem.solve()

#### Calculate total fuel spent
fuel_spent = sum(abs_a[t].varValue for t in range(T))

#### Prepare output
output = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

