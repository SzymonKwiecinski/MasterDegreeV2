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
To solve this problem, we need to formulate it as a linear programming (LP) problem. The objective is to minimize the total fuel consumption, which is equivalent to minimizing the sum of the absolute values of the accelerations over the time period. Given the constraints on the dynamics of the rocket, we can establish an LP model as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Fuel Minimization Problem}

We define the following variables:
- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)

Given:
- \( x_0 \) and \( v_0 \) as the initial position and velocity
- \( x_T \) and \( v_T \) as the target position and velocity at time \( T \)
- \( T \) as the time horizon

\subsection*{Objective:}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints:}

1. Dynamics of the rocket:
   \[
   x_{t+1} = x_t + v_t \quad \forall t = 0, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \forall t = 0, \ldots, T-1
   \]

2. Boundary conditions:
   \[
   x_0 = \text{given}
   \]
   \[
   v_0 = \text{given}
   \]
   \[
   x_T = \text{given}
   \]
   \[
   v_T = \text{given}
   \]

3. Absolute value constraint for accelerations:
   \[
   a_t^+ - a_t^- = a_t, \quad a_t^+, a_t^- \geq 0, \quad \forall t = 0, \ldots, T-1
   \]
   \[
   |a_t| = a_t^+ + a_t^-
   \]

With this setup, we formulate the LP as:
\[
\min \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]
Subject to:
\[
x_{t+1} = x_t + v_t \quad \forall t = 0, \ldots, T-1
\]
\[
v_{t+1} = v_t + a_t \quad \forall t = 0, \ldots, T-1
\]
\[
a_t = a_t^+ - a_t^- \quad \forall t = 0, \ldots, T-1
\]
\[
a_t^+, a_t^- \geq 0 \quad \forall t = 0, \ldots, T-1
\]
\[
x_0 = \text{given}, \ v_0 = \text{given}
\]
\[
x_T = \text{given}, \ v_T = \text{given}
\]

This model can be solved by standard linear programming solvers to obtain the positions, velocities, accelerations, and the total fuel spent.

\end{document}
```

In this formulation, we use \(a_t^+\) and \(a_t^-\) to represent the positive and negative parts of \(a_t\) so that \(|a_t| = a_t^+ + a_t^-\). This allows us to maintain linearity suitable for LP solvers. The solution of the LP will provide the positions \(x\), velocities \(v\), accelerations \(a\), and the total fuel spent.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Fuel Minimization Problem}

We define the following variables:
- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)

Given:
- \( x_0 \) and \( v_0 \) as the initial position and velocity
- \( x_T \) and \( v_T \) as the target position and velocity at time \( T \)
- \( T \) as the time horizon

\subsection*{Objective:}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints:}

1. Dynamics of the rocket:
   \[
   x_{t+1} = x_t + v_t \quad \forall t = 0, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \forall t = 0, \ldots, T-1
   \]

2. Boundary conditions:
   \[
   x_0 = \text{given}
   \]
   \[
   v_0 = \text{given}
   \]
   \[
   x_T = \text{given}
   \]
   \[
   v_T = \text{given}
   \]

3. Absolute value constraint for accelerations:
   \[
   a_t^+ - a_t^- = a_t, \quad a_t^+, a_t^- \geq 0, \quad \forall t = 0, \ldots, T-1
   \]
   \[
   |a_t| = a_t^+ + a_t^-
   \]

With this setup, we formulate the LP as:
\[
\min \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]
Subject to:
\[
x_{t+1} = x_t + v_t \quad \forall t = 0, \ldots, T-1
\]
\[
v_{t+1} = v_t + a_t \quad \forall t = 0, \ldots, T-1
\]
\[
a_t = a_t^+ - a_t^- \quad \forall t = 0, \ldots, T-1
\]
\[
a_t^+, a_t^- \geq 0 \quad \forall t = 0, \ldots, T-1
\]
\[
x_0 = \text{given}, \ v_0 = \text{given}
\]
\[
x_T = \text{given}, \ v_T = \text{given}
\]

This model can be solved by standard linear programming solvers to obtain the positions, velocities, accelerations, and the total fuel spent.

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create the linear programming problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

#### Define decision variables
a_pos = pulp.LpVariable.dicts("a_pos", range(T), lowBound=0)
a_neg = pulp.LpVariable.dicts("a_neg", range(T), lowBound=0)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)

#### Objective function: Minimize total fuel consumption
problem += pulp.lpSum([a_pos[t] + a_neg[t] for t in range(T)]), "Total_Fuel"

#### Initial conditions
x[0] = x_0
v[0] = v_0

#### Constraints for dynamics and boundary conditions
for t in range(T):
    #### Position and velocity dynamics
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + (a_pos[t] - a_neg[t]), f"Velocity_Constraint_{t}"

#### Boundary conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

#### Absolute value constraints for accelerations
for t in range(T):
    problem += (a_pos[t] - a_neg[t]) == (a_pos[t] - a_neg[t]), f"Acceleration_Constraint_{t}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

