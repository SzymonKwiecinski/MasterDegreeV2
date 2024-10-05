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

\section*{Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The evolution of the rocket's state can be described by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

Where the acceleration \( a_t \) is controlled through thrust, and its magnitude \( |a_t| \) is proportional to the rate of fuel consumption at time \( t \).

Given the initial conditions:

\[
x_0 = \text{initial position}
\]
\[
v_0 = \text{initial velocity}
\]

We want to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). The goal is to minimize the maximum thrust required, which can be expressed mathematically as:

\[
\text{Minimize} \quad M = \max_{t=0}^{T} |a_t|
\]

######### Subject to the constraints:

1. Position and velocity constraints:
   \[
   x_{t+1} = x_t + v_t, \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t, \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Boundary conditions:
   \[
   x_0 = x_0, \quad v_0 = v_0
   \]
   \[
   x_T = x_T, \quad v_T = v_T
   \]

3. Acceleration thrust bounds:
   \[
   -M \leq a_t \leq M, \quad \text{for } t = 0, 1, \ldots, T-1
   \]

######### Output Information

The output should be structured as follows:

\[
\text{Output} = 
\begin{cases}
x = [x_i \text{ for } i = 0, 1, \ldots, T] \\
v = [v_i \text{ for } i = 0, 1, \ldots, T] \\
a = [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{fuel\_spend} = \text{total fuel consumed}
\end{cases}
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

\section*{Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The evolution of the rocket's state can be described by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

Where the acceleration \( a_t \) is controlled through thrust, and its magnitude \( |a_t| \) is proportional to the rate of fuel consumption at time \( t \).

Given the initial conditions:

\[
x_0 = \text{initial position}
\]
\[
v_0 = \text{initial velocity}
\]

We want to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). The goal is to minimize the maximum thrust required, which can be expressed mathematically as:

\[
\text{Minimize} \quad M = \max_{t=0}^{T} |a_t|
\]

######### Subject to the constraints:

1. Position and velocity constraints:
   \[
   x_{t+1} = x_t + v_t, \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t, \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Boundary conditions:
   \[
   x_0 = x_0, \quad v_0 = v_0
   \]
   \[
   x_T = x_T, \quad v_T = v_T
   \]

3. Acceleration thrust bounds:
   \[
   -M \leq a_t \leq M, \quad \text{for } t = 0, 1, \ldots, T-1
   \]

######### Output Information

The output should be structured as follows:

\[
\text{Output} = 
\begin{cases}
x = [x_i \text{ for } i = 0, 1, \ldots, T] \\
v = [v_i \text{ for } i = 0, 1, \ldots, T] \\
a = [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{fuel\_spend} = \text{total fuel consumed}
\end{cases}
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
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

#### Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

#### Terminal conditions
problem += (x[T] == xT)
problem += (v[T] == vT)

#### Constraints and dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] >= -M)
    problem += (a[t] <= M)

#### Objective
problem += M

#### Solve the problem
problem.solve()

#### Extract solution and output results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spend = sum(abs(a_val) for a_val in a_values)

#### Display the results
print(f"x = {x_values}")
print(f"v = {v_values}")
print(f"a = {a_values}")
print(f"fuel_spend = {fuel_spend}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

