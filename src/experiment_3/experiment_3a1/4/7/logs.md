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

\section*{Rocket Trajectory Optimization Problem}

Let \( x_t \), \( v_t \), and \( a_t \) be the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model can be formulated as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

We are given the initial conditions:

\begin{align*}
    x_0 & = \text{initial position} \\
    v_0 & = \text{initial velocity} \\
\end{align*}

The objective is to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). The goal is to minimize the maximum thrust required, which can be expressed as:

\[
\text{Minimize} \quad \max_{t=0}^{T} |a_t|
\]

\text{Subject to:}

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

The variables are defined as follows:

- \( a_t \) is controlled acceleration, reflecting fuel consumption.
- We aim to minimize the fuel spent given by the maximum of the absolute values of acceleration over time.

The output of the model will be summarized as follows:

\begin{align*}
    \text{Output:} \\
    & \text{"x"}: [x_i \text{ for } i = 0, \ldots, T] \\
    & \text{"v"}: [v_i \text{ for } i = 0, \ldots, T] \\
    & \text{"a"}: [a_i \text{ for } i = 0, \ldots, T] \\
    & \text{"fuel\_spend"}: \text{total fuel spent by the rocket}
\end{align*}

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

\section*{Rocket Trajectory Optimization Problem}

Let \( x_t \), \( v_t \), and \( a_t \) be the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model can be formulated as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

We are given the initial conditions:

\begin{align*}
    x_0 & = \text{initial position} \\
    v_0 & = \text{initial velocity} \\
\end{align*}

The objective is to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). The goal is to minimize the maximum thrust required, which can be expressed as:

\[
\text{Minimize} \quad \max_{t=0}^{T} |a_t|
\]

\text{Subject to:}

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

The variables are defined as follows:

- \( a_t \) is controlled acceleration, reflecting fuel consumption.
- We aim to minimize the fuel spent given by the maximum of the absolute values of acceleration over time.

The output of the model will be summarized as follows:

\begin{align*}
    \text{Output:} \\
    & \text{"x"}: [x_i \text{ for } i = 0, \ldots, T] \\
    & \text{"v"}: [v_i \text{ for } i = 0, \ldots, T] \\
    & \text{"a"}: [a_i \text{ for } i = 0, \ldots, T] \\
    & \text{"fuel\_spend"}: \text{total fuel spent by the rocket}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create the linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Define decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity

#### Set initial conditions
x[0] = X0
v[0] = V0

#### Objective function to minimize maximum acceleration (thrust)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

#### Constraints for each time step
for t in range(T):
    #### Position and velocity update equations
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    
    #### Constrain max thrust
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

#### Constraints for reaching target position and velocity
problem += x[T] == XT
problem += v[T] == VT

#### Solve the problem
problem.solve()

#### Collect results
result_x = [pulp.value(x[t]) for t in range(T + 1)]
result_v = [pulp.value(v[t]) for t in range(T + 1)]
result_a = [pulp.value(a[t]) for t in range(T)]

#### Total fuel spent
fuel_spend = pulp.value(problem.objective)

#### Output summary
print(f'Output:')
print(f'{"x"}: {result_x}')
print(f'{"v"}: {result_v}')
print(f'{"a"}: {result_a}')
print(f'{"fuel_spend"}: {fuel_spend}')

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

