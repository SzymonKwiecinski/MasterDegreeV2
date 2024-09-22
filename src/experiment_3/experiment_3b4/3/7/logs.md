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
To solve this problem, we will construct a linear programming model that minimizes the maximum acceleration \(|a_t|\) over the discrete time periods \(t = 0, 1, \ldots, T-1\). This will indirectly minimize the fuel consumption by minimizing the maximum thrust requirement. Below is the mathematical formulation of this Linear Programming (LP) problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{align*}
    x_0 & : \text{Initial position of the rocket} \\
    v_0 & : \text{Initial velocity of the rocket} \\
    x_T & : \text{Target position at time } T \\
    v_T & : \text{Target velocity at time } T \\
    T   & : \text{Time horizon} 
\end{align*}

\subsection*{Variables}
\begin{align*}
    x_t & : \text{Position of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    v_t & : \text{Velocity of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    a_t & : \text{Acceleration of the rocket at time } t, \, t = 0, 1, \ldots, T-1 \\
    M   & : \text{Maximum thrust required (objective variable)}
\end{align*}

\subsection*{Objective}
Minimize the maximum acceleration magnitude:
\[
\min M
\]

\subsection*{Constraints}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
    & v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
    & x_0 = x_0, \quad v_0 = v_0 \\
    & x_T = x_T, \quad v_T = v_T \\
    & -M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\end{align}

The total fuel spent, which is the integral of the absolute value of thrust over time, can be approximated by:
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

This LP model minimizes the maximum absolute acceleration, which controls the fuel consumption by minimizing the largest single requirement for thrust. The constraints ensure the correct updating of position and velocity at each time step, satisfying the boundary conditions for initial and final states. The variable \(M\) captures the maximum absolute acceleration to be minimized.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{align*}
    x_0 & : \text{Initial position of the rocket} \\
    v_0 & : \text{Initial velocity of the rocket} \\
    x_T & : \text{Target position at time } T \\
    v_T & : \text{Target velocity at time } T \\
    T   & : \text{Time horizon} 
\end{align*}

\subsection*{Variables}
\begin{align*}
    x_t & : \text{Position of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    v_t & : \text{Velocity of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    a_t & : \text{Acceleration of the rocket at time } t, \, t = 0, 1, \ldots, T-1 \\
    M   & : \text{Maximum thrust required (objective variable)}
\end{align*}

\subsection*{Objective}
Minimize the maximum acceleration magnitude:
\[
\min M
\]

\subsection*{Constraints}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
    & v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
    & x_0 = x_0, \quad v_0 = v_0 \\
    & x_T = x_T, \quad v_T = v_T \\
    & -M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\end{align}

The total fuel spent, which is the integral of the absolute value of thrust over time, can be approximated by:
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

#### Problem data
data = {
    'X0': 0,
    'V0': 0,
    'XT': 1,
    'VT': 0,
    'T': 20
}

#### Create the LP problem
problem = pulp.LpProblem("Rocket_Minimum_Thrust", pulp.LpMinimize)

#### Variables
x = {t: pulp.LpVariable(f"x_{t}") for t in range(data['T'] + 1)}
v = {t: pulp.LpVariable(f"v_{t}") for t in range(data['T'] + 1)}
a = {t: pulp.LpVariable(f"a_{t}", lowBound=None) for t in range(data['T'])}
M = pulp.LpVariable("M", lowBound=0)

#### Objective
problem += M, "Minimize_Maximum_Acceleration"

#### Constraints
#### Initial conditions
problem += x[0] == data['X0'], "Initial_Position"
problem += v[0] == data['V0'], "Initial_Velocity"

#### Dynamics over time
for t in range(data['T']):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= M, f"Acceleration_Positive_Constraint_{t}"
    problem += -a[t] <= M, f"Acceleration_Negative_Constraint_{t}"

#### Final conditions
problem += x[data['T']] == data['XT'], "Final_Position"
problem += v[data['T']] == data['VT'], "Final_Velocity"

#### Solve the problem
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

