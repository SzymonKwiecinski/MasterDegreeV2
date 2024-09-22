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
To model the problem as a Linear Programming (LP) problem, we need to define the objective function and the constraints using the given information.

The objective is to minimize the total fuel spent, which is equivalent to minimizing the sum of the absolute values of the accelerations:

\[
\text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|
\]

We can represent the absolute value using auxiliary variables \( a^+_t \) and \( a^-_t \), where \( a_t = a^+_t - a^-_t \) and \( |a_t| = a^+_t + a^-_t \). Both \( a^+_t \) and \( a^-_t \) are non-negative.

The constraints based on the rocket's motion can be written as:

1. Position update: 
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Velocity update:
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

3. Initial conditions:
   \[
   x_0 = \text{given}, \quad v_0 = \text{given}
   \]

4. Target conditions:
   \[
   x_T = \text{given}, \quad v_T = \text{given}
   \]

5. Absolute value representation:
   \[
   a_t = a^+_t - a^-_t, \quad a^+_t \geq 0, \quad a^-_t \geq 0
   \]

Let's represent this in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:} Minimize the total fuel

\[
\min \sum_{t=0}^{T-1} (a^+_t + a^-_t)
\]

\textbf{Subject to the following constraints:}

\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= \text{given initial position} \\
v_0 &= \text{given initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
a_t &= a^+_t - a^-_t \\
a^+_t &\geq 0, \quad a^-_t \geq 0, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}
```

This LP model defines the problem constraints and objectives that can be solved to find the optimal path and control (acceleration) for the rocket while minimizing the fuel usage.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:} Minimize the total fuel

\[
\min \sum_{t=0}^{T-1} (a^+_t + a^-_t)
\]

\textbf{Subject to the following constraints:}

\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= \text{given initial position} \\
v_0 &= \text{given initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
a_t &= a^+_t - a^-_t \\
a^+_t &\geq 0, \quad a^-_t \geq 0, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create the problem
problem = pulp.LpProblem("Minimize_Total_Fuel", pulp.LpMinimize)

#### Variables
a_plus = pulp.LpVariable.dicts("a_plus", range(T), lowBound=0)
a_minus = pulp.LpVariable.dicts("a_minus", range(T), lowBound=0)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)

#### Objective function
problem += pulp.lpSum(a_plus[t] + a_minus[t] for t in range(T))

#### Initial Conditions
x[0] = x_0
v[0] = v_0

#### Constraints for each time step
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + (a_plus[t] - a_minus[t])

#### Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

