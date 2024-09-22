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

\section*{Rocket Motion Optimization Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively.

The discrete-time dynamics of the rocket can be described as follows:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We control the acceleration \( a_t \) and its magnitude \( |a_t| \) is proportional to the fuel consumption at time \( t \).

Given the initial conditions:
\[
x_0, \quad v_0
\]

We aim to reach a target position \( x_T \) with speed \( v_T \) at time \( T \), expressed mathematically as:

\[
x_T = x_{T-1} + v_{T-1}
\]
\[
v_T = v_{T-1} + a_{T-1}
\]

The goal is to minimize the total fuel consumption over the time period, which can be stated as:

\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

Subject to the constraints:

1. \( x_{t+1} = x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1 \)
2. \( v_{t+1} = v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1 \)
3. \( x_T = x_{T-1} + v_{T-1} \)
4. \( v_T = v_{T-1} + a_{T-1} \)

With given inputs:
\[
\begin{align*}
x_0 & : \text{initial position} \\
v_0 & : \text{initial velocity} \\
x_T & : \text{target position} \\
v_T & : \text{target velocity} \\
T & : \text{total time}
\end{align*}
\]

The output will consist of:
\[
\begin{align*}
\text{"x"} & : [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & : [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & : [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & : \text{total fuel spent}
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

\section*{Rocket Motion Optimization Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively.

The discrete-time dynamics of the rocket can be described as follows:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We control the acceleration \( a_t \) and its magnitude \( |a_t| \) is proportional to the fuel consumption at time \( t \).

Given the initial conditions:
\[
x_0, \quad v_0
\]

We aim to reach a target position \( x_T \) with speed \( v_T \) at time \( T \), expressed mathematically as:

\[
x_T = x_{T-1} + v_{T-1}
\]
\[
v_T = v_{T-1} + a_{T-1}
\]

The goal is to minimize the total fuel consumption over the time period, which can be stated as:

\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

Subject to the constraints:

1. \( x_{t+1} = x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1 \)
2. \( v_{t+1} = v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1 \)
3. \( x_T = x_{T-1} + v_{T-1} \)
4. \( v_T = v_{T-1} + a_{T-1} \)

With given inputs:
\[
\begin{align*}
x_0 & : \text{initial position} \\
v_0 & : \text{initial velocity} \\
x_T & : \text{target position} \\
v_T & : \text{target velocity} \\
T & : \text{total time}
\end{align*}
\]

The output will consist of:
\[
\begin{align*}
\text{"x"} & : [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & : [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & : [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & : \text{total fuel spent}
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create the optimization problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', cat='Continuous') for t in range(T)]

#### Objective function: minimize total fuel consumption
problem += pulp.lpSum([pulp.abs(a[t]) for t in range(T)])

#### Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

#### Constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  #### Position update
    problem += (v[t + 1] == v[t] + a[t])  #### Velocity update

#### Final conditions
problem += (x[T] == x[T - 1] + v[T - 1])  #### Final position
problem += (v[T] == v[T - 1] + a[T - 1])  #### Final velocity

#### Solve the problem
problem.solve()

#### Output results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
total_fuel_spent = pulp.value(problem.objective)

#### Print objective
print(f' (Objective Value): <OBJ>{total_fuel_spent}</OBJ>')

#### Print the results
print("x:", x_values)
print("v:", v_values)
print("a:", a_values)
print("total_fuel_spent:", total_fuel_spent)
```

