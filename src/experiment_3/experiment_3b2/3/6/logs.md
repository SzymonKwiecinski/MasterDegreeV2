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
To model the problem as a Linear Programming (LP) problem, we'll define the variables, objective function, and constraints. Since we need to minimize the absolute value of acceleration, a common approach is to introduce auxiliary variables to handle the absolute values in linear programming.

Let's set up the mathematical model:

Variables:
- \( x_t \): position of the rocket at time \( t \)
- \( v_t \): velocity of the rocket at time \( t \)
- \( a_t \): acceleration (control input) of the rocket at time \( t \)
- \( u_t \): auxiliary variable to represent \( |a_t| \)

Parameters:
- \( x_0 \): initial position
- \( v_0 \): initial velocity
- \( x_T \): target position at time \( T \)
- \( v_T \): target velocity at time \( T \)
- \( T \): total time

Objective:
- Minimize the total fuel consumption, represented by the sum of \( u_t \).

Constraints:
1. Discrete-time motion equations:
   - \( x_{t+1} = x_t + v_t \)
   - \( v_{t+1} = v_t + a_t \)

2. Boundaries for acceleration to represent absolute value:
    - \( u_t \geq a_t \)
    - \( u_t \geq -a_t \)

3. Initial conditions:
   - \( x_0 \) and \( v_0 \) are given.

4. Final conditions:
   - \( x_T \) and \( v_T \) are specified.

Now, let's express the LP problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Control Problem}

\subsection*{Variables}
\begin{align*}
x_t &: \text{Position of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
v_t &: \text{Velocity of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
a_t &: \text{Acceleration of the rocket at time } t, \quad t = 0, 1, \ldots, T-1 \\
u_t &: \text{Auxiliary variable representing } |a_t|, \quad t = 0, 1, \ldots, T-1
\end{align*}

\subsection*{Objective}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Constraints}
\begin{align*}
\text{Initial Conditions:} \quad & x_0 = \text{given}, \quad v_0 = \text{given} \\
\text{Final Conditions:} \quad & x_T = \text{given}, \quad v_T = \text{given} \\
\text{Motion Equations:} \quad & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
\text{Absolute Value Constraints:} \quad & u_t \geq a_t, \quad t = 0, 1, \ldots, T-1 \\
& u_t \geq -a_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}
```

This LP model enables you to solve for the optimal sequence of accelerations that minimize fuel usage while ensuring the rocket follows the specified trajectory and final conditions. You can use a linear programming solver to obtain the solution.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Control Problem}

\subsection*{Variables}
\begin{align*}
x_t &: \text{Position of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
v_t &: \text{Velocity of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
a_t &: \text{Acceleration of the rocket at time } t, \quad t = 0, 1, \ldots, T-1 \\
u_t &: \text{Auxiliary variable representing } |a_t|, \quad t = 0, 1, \ldots, T-1
\end{align*}

\subsection*{Objective}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Constraints}
\begin{align*}
\text{Initial Conditions:} \quad & x_0 = \text{given}, \quad v_0 = \text{given} \\
\text{Final Conditions:} \quad & x_T = \text{given}, \quad v_T = \text{given} \\
\text{Motion Equations:} \quad & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
\text{Absolute Value Constraints:} \quad & u_t \geq a_t, \quad t = 0, 1, \ldots, T-1 \\
& u_t \geq -a_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

#### Extracting data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Control_Problem", pulp.LpMinimize)

#### Define the variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
u = [pulp.LpVariable(f'u_{t}', lowBound=0) for t in range(T)]

#### Objective function
problem += pulp.lpSum(u[t] for t in range(T)), "Total_Fuel_Consumption"

#### Initial conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

#### Final conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

#### Motion equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Eq_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Eq_{t}"

#### Absolute value constraints
for t in range(T):
    problem += u[t] >= a[t], f"Absolute_Value_Constraint_Pos_{t}"
    problem += u[t] >= -a[t], f"Absolute_Value_Constraint_Neg_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

