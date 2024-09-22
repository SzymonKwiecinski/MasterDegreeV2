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
To form a mathematical model for the problem, we will construct a linear programming model that minimizes the fuel consumption while ensuring the rocket reaches its target position and velocity at time \( T \).

Let's define the variables and constraints formally:

######### Variables
- \( x_t \) for \( t = 0, 1, \ldots, T \): Position of the rocket at time \( t \).
- \( v_t \) for \( t = 0, 1, \ldots, T \): Velocity of the rocket at time \( t \).
- \( a_t \) for \( t = 0, 1, \ldots, T-1 \): Acceleration of the rocket at time \( t \).

######### Objective
Minimize the total fuel consumption:
\[
\text{Minimize } \sum_{t=0}^{T-1} |a_t|
\]

######### Constraints
1. Initial conditions:
   - \( x_0 = \) given initial position
   - \( v_0 = \) given initial velocity

2. Final conditions:
   - \( x_T = \) target position
   - \( v_T = \) target velocity

3. Discrete-time dynamic equations:
   - \( x_{t+1} = x_t + v_t \) for \( t = 0, 1, \ldots, T-1 \)
   - \( v_{t+1} = v_t + a_t \) for \( t = 0, 1, \ldots, T-1 \)

######### Linear Programming Formulation

To handle the absolute value in the objective function, we introduce auxiliary variables \( u_t \) to represent the absolute value of \( a_t \):
- \( u_t \geq a_t \)
- \( u_t \geq -a_t \)

The linear programming model becomes:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize } & \sum_{t=0}^{T-1} u_t \\
\text{subject to: } \\
& x_0 = \text{given initial position,} \\
& v_0 = \text{given initial velocity,} \\
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
& u_t \geq a_t, \quad t = 0, 1, \ldots, T-1, \\
& u_t \geq -a_t, \quad t = 0, 1, \ldots, T-1, \\
& x_T = \text{target position,} \\
& v_T = \text{target velocity.}
\end{align*}

\end{document}
```

This model ensures that the rocket reaches the specified final position and velocity while minimizing the absolute value of the accelerations used, which corresponds to minimizing fuel consumption. The auxiliary variables \( u_t \) allow encoding the absolute value condition within the linear programming framework.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize } & \sum_{t=0}^{T-1} u_t \\
\text{subject to: } \\
& x_0 = \text{given initial position,} \\
& v_0 = \text{given initial velocity,} \\
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
& u_t \geq a_t, \quad t = 0, 1, \ldots, T-1, \\
& u_t \geq -a_t, \quad t = 0, 1, \ldots, T-1, \\
& x_T = \text{target position,} \\
& v_T = \text{target velocity.}
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

#### Variables
T = data['TotalTime']
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
u = pulp.LpVariable.dicts("u", range(T), lowBound=0)

#### Problem
problem = pulp.LpProblem("MinimizeAcceleration", pulp.LpMinimize)

#### Objective function
problem += pulp.lpSum(u[t] for t in range(T))

#### Constraints
problem += (x[0] == data['InitialPosition'])
problem += (v[0] == data['InitialVelocity'])

for t in range(T-1):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (u[t] >= a[t])
    problem += (u[t] >= -a[t])

problem += (x[T] == data['FinalPosition'])
problem += (v[T] == data['FinalVelocity'])

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

