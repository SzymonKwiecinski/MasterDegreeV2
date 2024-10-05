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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Trajectory Optimization Problem}

\subsection*{Variables}
Let:
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t
\end{align*}

\subsection*{Model Formulation}
The discrete-time model of the rocket's motion can be described by the following equations:
\begin{align}
x_{t+1} = x_t + v_t \\
v_{t+1} = v_t + a_t
\end{align}

\subsection*{Inputs}
The inputs of the problem are:
\begin{align*}
x_0 & : \text{Initial position} \\
v_0 & : \text{Initial velocity} \\
x_T & : \text{Target position} \\
v_T & : \text{Target velocity} \\
T & : \text{Total time steps}
\end{align*}

\subsection*{Objective Function}
The objective is to minimize the total fuel spent, represented by:
\[
\text{minimize } \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints}
We must also satisfy the following constraints to reach the target:
\begin{align*}
x_0 & = x_0 \\
v_0 & = v_0 \\
x_T & = x_T \\
v_T & = v_T
\end{align*}

\subsection*{Output}
The expected output format is:
\begin{verbatim}
{
    "x": [x_i for i in 1, ..., T],
    "v": [v_i for i in 1, ..., T],
    "a": [a_i for i in 1, ..., T],
    "fuel_spend": fuel_spent,
}
\end{verbatim}

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

\section*{Rocket Trajectory Optimization Problem}

\subsection*{Variables}
Let:
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t
\end{align*}

\subsection*{Model Formulation}
The discrete-time model of the rocket's motion can be described by the following equations:
\begin{align}
x_{t+1} = x_t + v_t \\
v_{t+1} = v_t + a_t
\end{align}

\subsection*{Inputs}
The inputs of the problem are:
\begin{align*}
x_0 & : \text{Initial position} \\
v_0 & : \text{Initial velocity} \\
x_T & : \text{Target position} \\
v_T & : \text{Target velocity} \\
T & : \text{Total time steps}
\end{align*}

\subsection*{Objective Function}
The objective is to minimize the total fuel spent, represented by:
\[
\text{minimize } \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints}
We must also satisfy the following constraints to reach the target:
\begin{align*}
x_0 & = x_0 \\
v_0 & = v_0 \\
x_T & = x_T \\
v_T & = v_T
\end{align*}

\subsection*{Output}
The expected output format is:
\begin{verbatim}
{
    "x": [x_i for i in 1, ..., T],
    "v": [v_i for i in 1, ..., T],
    "a": [a_i for i in 1, ..., T],
    "fuel_spend": fuel_spent,
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem setup
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Input data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

#### Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(data['TotalTime'] + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(data['TotalTime'] + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(data['TotalTime'])]

#### Objective Function
problem += pulp.lpSum(pulp.lpSum([pulp.lpSum([a[t] for t in range(data['TotalTime'])])] for t in range(data['TotalTime']))), "TotalFuelSpend"

#### Constraints
problem += (x[0] == data['InitialPosition'], "InitialPosition")
problem += (v[0] == data['InitialVelocity'], "InitialVelocity")
problem += (x[data['TotalTime']] == data['FinalPosition'], "FinalPosition")
problem += (v[data['TotalTime']] == data['FinalVelocity'], "FinalVelocity")

for t in range(data['TotalTime']):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

#### Solve the problem
problem.solve()

#### Output results
result = {
    "x": [pulp.value(x[i]) for i in range(1, data['TotalTime'] + 1)],
    "v": [pulp.value(v[i]) for i in range(1, data['TotalTime'] + 1)],
    "a": [pulp.value(a[i]) for i in range(data['TotalTime'])],
    "fuel_spend": pulp.value(problem.objective),
}

print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

