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

\section*{Mathematical Model for Rocket Motion}

We define the following variables:

\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time dynamics of the rocket can be expressed as:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

Given the initial conditions:

\[
x_0, \quad v_0
\]

and the target conditions:

\[
x_T, \quad v_T, \quad T
\]

we aim to minimize the total fuel used, represented by the sum of the absolute values of the accelerations:

\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

subject to the constraints:

\begin{align*}
x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1 \\
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity}
\end{align*}

The objective can be formulated as follows:

\begin{equation}
\text{Objective:} \quad \min \left( \sum_{t=0}^{T-1} |a_t| \right)
\end{equation}

\textbf{Output:} 

The results will yield:

\begin{itemize}
    \item \( x \): a list of positions \( [x_i \text{ for } i = 0, \ldots, T] \)
    \item \( v \): a list of velocities \( [v_i \text{ for } i = 0, \ldots, T] \)
    \item \( a \): a list of accelerations \( [a_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{fuel\_spend} \): total fuel spent
\end{itemize}

Output format:

\[
\left\{
\begin{array}{l}
"x": [x_0, x_1, \ldots, x_T], \\
"v": [v_0, v_1, \ldots, v_T], \\
"a": [a_0, a_1, \ldots, a_T], \\
"fuel\_spend": \text{total fuel spent}
\end{array}
\right.
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

We define the following variables:

\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time dynamics of the rocket can be expressed as:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

Given the initial conditions:

\[
x_0, \quad v_0
\]

and the target conditions:

\[
x_T, \quad v_T, \quad T
\]

we aim to minimize the total fuel used, represented by the sum of the absolute values of the accelerations:

\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

subject to the constraints:

\begin{align*}
x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1 \\
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity}
\end{align*}

The objective can be formulated as follows:

\begin{equation}
\text{Objective:} \quad \min \left( \sum_{t=0}^{T-1} |a_t| \right)
\end{equation}

\textbf{Output:} 

The results will yield:

\begin{itemize}
    \item \( x \): a list of positions \( [x_i \text{ for } i = 0, \ldots, T] \)
    \item \( v \): a list of velocities \( [v_i \text{ for } i = 0, \ldots, T] \)
    \item \( a \): a list of accelerations \( [a_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{fuel\_spend} \): total fuel spent
\end{itemize}

Output format:

\[
\left\{
\begin{array}{l}
"x": [x_0, x_1, \ldots, x_T], \\
"v": [v_0, v_1, \ldots, v_T], \\
"a": [a_0, a_1, \ldots, a_T], \\
"fuel\_spend": \text{total fuel spent}
\end{array}
\right.
\]

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Extract parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion_Problem", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity

#### Objective function: Minimize the total fuel used (sum of absolute values of accelerations)
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "MinimizeFuel"

#### Constraints
#### Initial conditions
problem += x[0] == x0, "InitialPosition"
problem += v[0] == v0, "InitialVelocity"

#### Dynamics
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionDynamics_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityDynamics_{t}"

#### Target conditions
problem += x[T] == xT, "FinalPosition"
problem += v[T] == vT, "FinalVelocity"

#### Solve the problem
problem.solve()

#### Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spend = pulp.value(problem.objective)

#### Output the results
result = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spend
}

print(f' (Objective Value): <OBJ>{fuel_spend}</OBJ>')
```

