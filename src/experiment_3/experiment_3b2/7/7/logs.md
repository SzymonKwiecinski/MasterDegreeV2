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
To formulate the given problem as a linear programming (LP) model, we need to define the objective function and constraints based on the problem description.

Objective: Minimize the maximum thrust required, which is \( \max_t |a_t| \).

Constraints:

1. Position update constraint:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Velocity update constraint:
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

3. Initial conditions:
   \[
   x_0 = \text{given}
   \]
   \[
   v_0 = \text{given}
   \]

4. Final conditions:
   \[
   x_T = \text{given}
   \]
   \[
   v_T = \text{given}
   \]

5. Absolute value constraint for acceleration (to linearize the problem, we introduce auxiliary variables):
   \[
   a_t^+ \geq a_t
   \]
   \[
   a_t^- \geq -a_t
   \]
   \[
   |a_t| = a_t^+ + a_t^-
   \]

6. The goal is to minimize the maximum of these absolute values over all time steps:
   \[
   \min z
   \]
   subject to:
   \[
   z \geq a_t^+ + a_t^- \quad \text{for } t = 0, 1, \ldots, T-1
   \]

Let's put this into a \(\LaTeX\) format for the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket LP Model}

\subsection*{Objective}
Minimize the maximum thrust:
\[
\min z
\]

\subsection*{Constraints}
\begin{align}
x_{t+1} &= x_t + v_t && \text{for } t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t && \text{for } t = 0, 1, \ldots, T-1 \\
x_0 &= x_0 \\
v_0 &= v_0 \\
x_T &= x_T \\
v_T &= v_T \\
a_t^+ &\geq a_t \quad && \text{for } t = 0, 1, \ldots, T-1 \\
a_t^- &\geq -a_t \quad && \text{for } t = 0, 1, \ldots, T-1 \\
z &\geq a_t^+ + a_t^- && \text{for } t = 0, 1, \ldots, T-1
\end{align}

\subsection*{Fuel Consumption}
The total fuel consumption is given by:
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]

\end{document}
```

The above \(\LaTeX\) code sets out the constraints and objective for the linear programming problem, intended to minimize the maximum absolute acceleration while meeting initial and final position and velocity requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket LP Model}

\subsection*{Objective}
Minimize the maximum thrust:
\[
\min z
\]

\subsection*{Constraints}
\begin{align}
x_{t+1} &= x_t + v_t && \text{for } t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t && \text{for } t = 0, 1, \ldots, T-1 \\
x_0 &= x_0 \\
v_0 &= v_0 \\
x_T &= x_T \\
v_T &= v_T \\
a_t^+ &\geq a_t \quad && \text{for } t = 0, 1, \ldots, T-1 \\
a_t^- &\geq -a_t \quad && \text{for } t = 0, 1, \ldots, T-1 \\
z &\geq a_t^+ + a_t^- && \text{for } t = 0, 1, \ldots, T-1
\end{align}

\subsection*{Fuel Consumption}
The total fuel consumption is given by:
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = '{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}'
params = json.loads(data)

#### Parameters
X0 = params['X0']
V0 = params['V0']
XT = params['XT']
VT = params['VT']
T = params['T']

#### Create the LP problem
problem = pulp.LpProblem("Rocket_LP_Model", pulp.LpMinimize)

#### Decision Variables
a_plus = pulp.LpVariable.dicts("a_plus", range(T), lowBound=0)
a_minus = pulp.LpVariable.dicts("a_minus", range(T), lowBound=0)
z = pulp.LpVariable("z", lowBound=0)

#### State variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=0)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=0)

#### Objective Function
problem += z

#### Constraints
#### Initial conditions
problem += x[0] == X0
problem += v[0] == V0

#### Dynamic constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + (a_plus[t] - a_minus[t])

#### Final conditions
problem += x[T] == XT
problem += v[T] == VT

#### Thrust constraints
for t in range(T):
    problem += a_plus[t] >= 0
    problem += a_minus[t] >= 0
    problem += z >= a_plus[t] + a_minus[t]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

