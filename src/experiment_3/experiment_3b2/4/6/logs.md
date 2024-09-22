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
To solve this problem, we will formulate a Linear Programming (LP) model in order to minimize the total fuel consumption while satisfying the given constraints. This problem involves determining the acceleration of the rocket at each time step such that it reaches the target position and velocity in the most fuel-efficient manner.

We will employ the following variables and constraints:

1. Variables:
   - \( x_t \): position of the rocket at time \( t \).
   - \( v_t \): velocity of the rocket at time \( t \).
   - \( a_t \): acceleration (or thrust) of the rocket at time \( t \).
   - \( u_t \): auxiliary variable to represent the absolute value of acceleration \( |a_t| \).

2. Objective:
   - Minimize the total fuel, which is proportional to the sum of absolute accelerations: \(\sum_{t=0}^{T-1} u_t\).

3. Constraints:
   - Dynamics constraints:
     \[
     x_{t+1} = x_t + v_t \quad \text{for } t = 0, \ldots, T-1
     \]
     \[
     v_{t+1} = v_t + a_t \quad \text{for } t = 0, \ldots, T-1
     \]
   - Absolute value constraints:
     \[
     -u_t \leq a_t \leq u_t \quad \text{for } t = 0, \ldots, T-1
     \]
   - Initial conditions:
     \[
     x_0 = \text{x\_0}
     \]
     \[
     v_0 = \text{v\_0}
     \]
   - Final conditions:
     \[
     x_T = \text{x\_T}
     \]
     \[
     v_T = \text{v\_T}
     \]

Here is the LP model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\[
\begin{align*}
\text{Minimize} \quad & \sum_{t=0}^{T-1} u_t \\
\text{Subject to} \quad & x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
& -u_t \leq a_t \leq u_t, \quad t = 0, \ldots, T-1 \\
& x_0 = x_0 \\
& v_0 = v_0 \\
& x_T = x_T \\
& v_T = v_T \\
\end{align*}
\]

\end{document}
```

This LP formulation can be solved using optimization software to obtain the sequence of accelerations \( a_t \) that meet the problem's requirements. The solution will provide the positions \( x \), velocities \( v \), and accelerations \( a \) at each time step as well as the total fuel spent \( \sum_{t=0}^{T-1} |a_t| \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\[
\begin{align*}
\text{Minimize} \quad & \sum_{t=0}^{T-1} u_t \\
\text{Subject to} \quad & x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
& -u_t \leq a_t \leq u_t, \quad t = 0, \ldots, T-1 \\
& x_0 = x_0 \\
& v_0 = v_0 \\
& x_T = x_T \\
& v_T = v_T \\
\end{align*}
\]

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

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
u = pulp.LpVariable.dicts("u", range(T), lowBound=0)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Objective function
problem += pulp.lpSum(u[t] for t in range(T)), "TotalCost"

#### Constraints
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"
problem += x[T] == x_T, "FinalPosition"
problem += v[T] == v_T, "FinalVelocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}"
    problem += -u[t] <= a[t], f"AccelerationLowerBound_{t}"
    problem += a[t] <= u[t], f"AccelerationUpperBound_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

