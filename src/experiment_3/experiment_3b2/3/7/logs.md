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
To address this problem through linear programming, we need to develop a mathematical model that minimizes the maximum thrust while ensuring that the rocket reaches the target position and speed in the given time frame. Let's establish the model in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

We are given the following data:
\begin{align*}
x_0 &= \text{initial position of the rocket}, \\
v_0 &= \text{initial velocity of the rocket}, \\
x_T &= \text{target position at time } T, \\
v_T &= \text{target velocity at time } T, \\
T &= \text{time horizon}.
\end{align*}

We aim to minimize the maximum thrust, denoted by $\max_t |a_t|$, subjected to the discrete-time rocket equations:
\begin{align}
x_{t+1} &= x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1, \\
v_{t+1} &= v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1,
\end{align}
with the initial conditions:
\begin{align}
x_0 &= x_0, \\
v_0 &= v_0,
\end{align}
and the final conditions:
\begin{align}
x_T &= x_T, \\
v_T &= v_T.
\end{align}

Additionally, let us introduce a variable $M$ to represent the maximum absolute acceleration. Our objective function becomes:
\[
\min M
\]

Subject to the constraints:
\begin{align}
-M &\leq a_t \leq M, \quad \forall t = 0, 1, \ldots, T-1, \\
x_{t+1} &= x_t + v_t, \\
v_{t+1} &= v_t + a_t, \\
x_0 &= x_0, \quad v_0 = v_0, \\
x_T &= x_T, \quad v_T = v_T.
\end{align}

The fuel consumption is proportional to the absolute acceleration. Thus, the total fuel spent, $F$, can be calculated as:
\[
F = \sum_{t=0}^{T-1} |a_t|
\]

This completes the linear programming formulation of the rocket problem.

\end{document}
``` 

This linear programming model aims to minimize the maximum thrust required for the rocket to reach the desired position and velocity while ensuring that fuel consumption is accounted for by integrating the absolute value of the acceleration over time.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

We are given the following data:
\begin{align*}
x_0 &= \text{initial position of the rocket}, \\
v_0 &= \text{initial velocity of the rocket}, \\
x_T &= \text{target position at time } T, \\
v_T &= \text{target velocity at time } T, \\
T &= \text{time horizon}.
\end{align*}

We aim to minimize the maximum thrust, denoted by $\max_t |a_t|$, subjected to the discrete-time rocket equations:
\begin{align}
x_{t+1} &= x_t + v_t, \quad \forall t = 0, 1, \ldots, T-1, \\
v_{t+1} &= v_t + a_t, \quad \forall t = 0, 1, \ldots, T-1,
\end{align}
with the initial conditions:
\begin{align}
x_0 &= x_0, \\
v_0 &= v_0,
\end{align}
and the final conditions:
\begin{align}
x_T &= x_T, \\
v_T &= v_T.
\end{align}

Additionally, let us introduce a variable $M$ to represent the maximum absolute acceleration. Our objective function becomes:
\[
\min M
\]

Subject to the constraints:
\begin{align}
-M &\leq a_t \leq M, \quad \forall t = 0, 1, \ldots, T-1, \\
x_{t+1} &= x_t + v_t, \\
v_{t+1} &= v_t + a_t, \\
x_0 &= x_0, \quad v_0 = v_0, \\
x_T &= x_T, \quad v_T = v_T.
\end{align}

The fuel consumption is proportional to the absolute acceleration. Thus, the total fuel spent, $F$, can be calculated as:
\[
F = \sum_{t=0}^{T-1} |a_t|
\]

This completes the linear programming formulation of the rocket problem.

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

#### Define variables
M = pulp.LpVariable("M", lowBound=0)
a = pulp.LpVariable.dicts("a", range(T-1), lowBound=None)  #### Acceleration
x = pulp.LpVariable.dicts("x", range(T), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T), lowBound=None)  #### Velocity

#### Objective function
problem += M  #### Minimize the maximum thrust

#### Constraints
problem += x[0] == x_0  #### Initial position constraint
problem += v[0] == v_0  #### Initial velocity constraint

for t in range(T-1):
    problem += x[t + 1] == x[t] + v[t]  #### Position update
    problem += v[t + 1] == v[t] + a[t]  #### Velocity update
    problem += -M <= a[t]  #### Lower bound on acceleration
    problem += a[t] <= M  #### Upper bound on acceleration

#### Final conditions
problem += x[T-1] == x_T  #### Final position constraint
problem += v[T-1] == v_T  #### Final velocity constraint

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

