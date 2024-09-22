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

\section*{Rocket Motion Linear Programming Model}

Let \( x_t \), \( v_t \), and \( a_t \) be the position, velocity, and acceleration of the rocket at time \( t \). The dynamical equations governing the motion of the rocket are defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We aim to control the acceleration \( a_t \), which is related to the fuel consumption. Our goal is to minimize the maximum thrust required, represented as \( \max_t |a_t| \).

Given the initial conditions and target specifications, we define the following parameters:

- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Total time: \( T \)

We can summarize the linear programming model as follows:

\subsection*{Objective Function}

Minimize the maximum thrust:

\[
\text{Minimize} \quad M
\]

where:

\[
M \geq |a_t| \quad \forall t = 0, 1, \ldots, T
\]

\subsection*{Constraints}

1. Initial conditions:
    \[
    x_0 \text{ (given)}, \quad v_0 \text{ (given)}
    \]

2. State update equations for each time step \( t \):
    \[
    x_{t+1} = x_t + v_t \quad \forall t = 0, 1, \ldots, T-1
    \]

    \[
    v_{t+1} = v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
    \]

3. Final conditions:
    \[
    x_T = x_T \text{ (given)}, \quad v_T = v_T \text{ (given)}
    \]

4. Control variable bounds:
    \[
    -M \leq a_t \leq M \quad \forall t = 0, 1, \ldots, T
    \]

\subsection*{Output Specification}

The outputs of the model will be:

\[
\begin{align*}
\text{"x"} &: [x_i \text{ for } i = 0, \ldots, T] \\
\text{"v"} &: [v_i \text{ for } i = 0, \ldots, T] \\
\text{"a"} &: [a_i \text{ for } i = 0, \ldots, T] \\
\text{"fuel\_spend"} &: \text{Total fuel spent}
\end{align*}
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

\section*{Rocket Motion Linear Programming Model}

Let \( x_t \), \( v_t \), and \( a_t \) be the position, velocity, and acceleration of the rocket at time \( t \). The dynamical equations governing the motion of the rocket are defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We aim to control the acceleration \( a_t \), which is related to the fuel consumption. Our goal is to minimize the maximum thrust required, represented as \( \max_t |a_t| \).

Given the initial conditions and target specifications, we define the following parameters:

- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Total time: \( T \)

We can summarize the linear programming model as follows:

\subsection*{Objective Function}

Minimize the maximum thrust:

\[
\text{Minimize} \quad M
\]

where:

\[
M \geq |a_t| \quad \forall t = 0, 1, \ldots, T
\]

\subsection*{Constraints}

1. Initial conditions:
    \[
    x_0 \text{ (given)}, \quad v_0 \text{ (given)}
    \]

2. State update equations for each time step \( t \):
    \[
    x_{t+1} = x_t + v_t \quad \forall t = 0, 1, \ldots, T-1
    \]

    \[
    v_{t+1} = v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
    \]

3. Final conditions:
    \[
    x_T = x_T \text{ (given)}, \quad v_T = v_T \text{ (given)}
    \]

4. Control variable bounds:
    \[
    -M \leq a_t \leq M \quad \forall t = 0, 1, \ldots, T
    \]

\subsection*{Output Specification}

The outputs of the model will be:

\[
\begin{align*}
\text{"x"} &: [x_i \text{ for } i = 0, \ldots, T] \\
\text{"v"} &: [v_i \text{ for } i = 0, \ldots, T] \\
\text{"a"} &: [a_i \text{ for } i = 0, \ldots, T] \\
\text{"fuel\_spend"} &: \text{Total fuel spent}
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion", pulp.LpMinimize)

#### Define variables
M = pulp.LpVariable("M", lowBound=0)  #### Maximum thrust
a = [pulp.LpVariable(f'a_{t}', lowBound=-M, upBound=M) for t in range(T + 1)]  #### Acceleration at each time step
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]  #### Position at each time step
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]  #### Velocity at each time step

#### Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

#### State update equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}")

#### Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

#### Maximum thrust constraints
for t in range(T + 1):
    problem += (M >= pulp.lpSum([a[t]]), f"Max_Thrust_Constraint_{t}")

#### Objective function
problem += M  #### Minimize the maximum thrust

#### Solve the problem
problem.solve()

#### Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T + 1)]
fuel_spend = pulp.value(M) * (T + 1)  #### This can be defined based on specific fuel consumption logic.

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Positions: {x_values}')
print(f'Velocities: {v_values}')
print(f'Accelerations: {a_values}')
print(f'Total Fuel Spent: {fuel_spend}')
```

