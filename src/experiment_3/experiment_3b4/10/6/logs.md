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
To solve the given problem, we must formulate a linear programming model that aims to minimize the total fuel consumption, represented by the absolute value of acceleration, while considering the constraints given by the discrete-time motion equations and the initial and final conditions.

Below is the LaTeX representation of the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\subsection*{Objective:}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints:}

1. Initial conditions:
   \[
   x_0 = \text{given}, \quad v_0 = \text{given}
   \]

2. Motion equations for \( t = 0, 1, 2, \ldots, T-1 \):
   \[
   x_{t+1} = x_t + v_t 
   \]
   \[
   v_{t+1} = v_t + a_t
   \]

3. Final conditions:
   \[
   x_T = \text{given}, \quad v_T = \text{given}
   \]

\subsection*{Variables:}
- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)

\subsection*{Note:}
The absolute value constraint on the acceleration \(|a_t|\) can be linearized by introducing auxiliary variables and constraints:
Let \( a_t^+ \geq 0 \) and \( a_t^- \geq 0 \).

Then, express \( a_t = a_t^+ - a_t^- \) and add the constraint:
\[
a_t^+ + a_t^- = |a_t|
\]

The new objective becomes:
\[
\min \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]

The LP model now includes these auxiliary variables for each time step to handle the absolute value constraint linearly.

\end{document}
```

This model outlines the constraints and objective function necessary for minimizing the total fuel consumption subject to the given motion dynamics and initial/final conditions. The transformation of the absolute value into linear constraints using auxiliary variables allows the problem to be handled by standard linear programming solvers.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\subsection*{Objective:}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints:}

1. Initial conditions:
   \[
   x_0 = \text{given}, \quad v_0 = \text{given}
   \]

2. Motion equations for \( t = 0, 1, 2, \ldots, T-1 \):
   \[
   x_{t+1} = x_t + v_t 
   \]
   \[
   v_{t+1} = v_t + a_t
   \]

3. Final conditions:
   \[
   x_T = \text{given}, \quad v_T = \text{given}
   \]

\subsection*{Variables:}
- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)

\subsection*{Note:}
The absolute value constraint on the acceleration \(|a_t|\) can be linearized by introducing auxiliary variables and constraints:
Let \( a_t^+ \geq 0 \) and \( a_t^- \geq 0 \).

Then, express \( a_t = a_t^+ - a_t^- \) and add the constraint:
\[
a_t^+ + a_t^- = |a_t|
\]

The new objective becomes:
\[
\min \sum_{t=0}^{T-1} (a_t^+ + a_t^-)
\]

The LP model now includes these auxiliary variables for each time step to handle the absolute value constraint linearly.

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

#### Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Initialize the LP problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Create variables for position, velocity, and acceleration
x = [pulp.LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a_plus = [pulp.LpVariable(f'a_plus_{t}', lowBound=0, cat='Continuous') for t in range(T)]
a_minus = [pulp.LpVariable(f'a_minus_{t}', lowBound=0, cat='Continuous') for t in range(T)]

#### Objective function: Minimize total fuel consumption
problem += pulp.lpSum(a_plus[t] + a_minus[t] for t in range(T))

#### Initial conditions
problem += x[0] == x_0, "Initial_Position"
problem += v[0] == v_0, "Initial_Velocity"

#### Motion equations
for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t+1] == v[t] + a_plus[t] - a_minus[t], f"Velocity_Constraint_{t}"

#### Final conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

