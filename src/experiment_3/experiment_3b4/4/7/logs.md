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
To model this problem as a linear programming problem in LaTeX, we need to define our decision variables, the objective function, and the constraints. Here's how the LP formulation can be presented:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Trajectory Optimization}

\subsection*{Problem Formulation}

We are given the following discrete-time dynamics of a rocket:

\begin{align*}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t,
\end{align*}

where:
- \( t = 0, 1, \ldots, T-1 \)
- \( x_0 \) and \( v_0 \) are the initial position and velocity,
- \( x_T \) and \( v_T \) are the target position and velocity at time \( T \),
- \( a_t \) is the control input (acceleration).

\subsection*{Objective}

Minimize the maximum thrust, which is proportional to fuel consumption:

\[
\min \max_{t} |a_t|
\]

\subsection*{Constraints}

1. Dynamics constraints:
    \[
    x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
    \]
    \[
    v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
    \]

2. Initial conditions:
    \[
    x_0 = \text{given } x_0, \quad v_0 = \text{given } v_0
    \]

3. Target conditions:
    \[
    x_T = \text{given } x_T, \quad v_T = \text{given } v_T
    \]

4. Linearize the absolute value for the optimization:
    \[
    a_t \leq u, \quad -a_t \leq u \quad \text{for } t = 0, 1, \ldots, T-1
    \]

where \( u \) is an auxiliary variable representing the maximum magnitude of \( a_t \).

\subsection*{Variables}

- Decision variables: \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
- Auxiliary variable: \( u \)

\subsection*{Objective Function in LP Form}

\[
\min u
\]

\subsection*{Solution Output}

The output of the optimization will include:
- Positions: \( x_1, x_2, \ldots, x_T \)
- Velocities: \( v_1, v_2, \ldots, v_T \)
- Accelerations: \( a_0, a_1, \ldots, a_{T-1} \)
- Total fuel spent, approximated by: 
  \[
  \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
  \]

\end{document}
```

This formulation sets up a linear programming problem where the goal is to minimize the maximum acceleration \( |a_t| \), under the dynamics constraints, initial conditions, and final target conditions. The absolute value in the objective is handled by introducing auxiliary variables and constraints.

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

\subsection*{Problem Formulation}

We are given the following discrete-time dynamics of a rocket:

\begin{align*}
    x_{t+1} &= x_t + v_t, \\
    v_{t+1} &= v_t + a_t,
\end{align*}

where:
- \( t = 0, 1, \ldots, T-1 \)
- \( x_0 \) and \( v_0 \) are the initial position and velocity,
- \( x_T \) and \( v_T \) are the target position and velocity at time \( T \),
- \( a_t \) is the control input (acceleration).

\subsection*{Objective}

Minimize the maximum thrust, which is proportional to fuel consumption:

\[
\min \max_{t} |a_t|
\]

\subsection*{Constraints}

1. Dynamics constraints:
    \[
    x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
    \]
    \[
    v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
    \]

2. Initial conditions:
    \[
    x_0 = \text{given } x_0, \quad v_0 = \text{given } v_0
    \]

3. Target conditions:
    \[
    x_T = \text{given } x_T, \quad v_T = \text{given } v_T
    \]

4. Linearize the absolute value for the optimization:
    \[
    a_t \leq u, \quad -a_t \leq u \quad \text{for } t = 0, 1, \ldots, T-1
    \]

where \( u \) is an auxiliary variable representing the maximum magnitude of \( a_t \).

\subsection*{Variables}

- Decision variables: \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
- Auxiliary variable: \( u \)

\subsection*{Objective Function in LP Form}

\[
\min u
\]

\subsection*{Solution Output}

The output of the optimization will include:
- Positions: \( x_1, x_2, \ldots, x_T \)
- Velocities: \( v_1, v_2, \ldots, v_T \)
- Accelerations: \( a_0, a_1, \ldots, a_{T-1} \)
- Total fuel spent, approximated by: 
  \[
  \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
  \]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
u = pulp.LpVariable("u", lowBound=0, cat='Continuous')

#### Objective
problem += u, "Minimize_maximum_thrust"

#### Constraints

#### Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

#### Target conditions
problem += (x[T] == XT, "Target_Position")
problem += (v[T] == VT, "Target_Velocity")

#### Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Dynamics_Velocity_{t}")

#### Absolute value linearization
for t in range(T):
    problem += (a[t] <= u, f"Abs_Upper_{t}")
    problem += (-a[t] <= u, f"Abs_Lower_{t}")

#### Solve
problem.solve()

#### Print Results
positions = [x[t].varValue for t in range(T+1)]
velocities = [v[t].varValue for t in range(T+1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spend = sum(abs(a[t].varValue) for t in range(T))

print(f"Positions: {positions}")
print(f"Velocities: {velocities}")
print(f"Accelerations: {accelerations}")
print(f"Fuel Spend: {fuel_spend}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

