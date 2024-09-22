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
To address this problem, we need to formulate a Linear Programming (LP) model. The goal is to minimize the maximum thrust required, which is equivalent to minimizing the maximum magnitude of acceleration |a_t| over the given time horizon. Let's define the LP model accordingly:

1. **Decision Variables:**
    - \( x_t \): position of the rocket at time \( t \).
    - \( v_t \): velocity of the rocket at time \( t \).
    - \( a_t \): acceleration of the rocket at time \( t \).
    - \( M \): an auxiliary variable representing the maximum magnitude of acceleration.

2. **Objective Function:**
    - Minimize \( M \).

3. **Constraints:**
    - Discrete-time dynamics:
      \[
      \begin{align*}
      x_{t+1} &= x_t + v_t, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
      v_{t+1} &= v_t + a_t, \quad \forall t \in \{0, 1, \ldots, T-1\}
      \end{align*}
      \]
    - Magnitude of acceleration:
      \[
      |a_t| \leq M, \quad \forall t \in \{0, 1, \ldots, T-1\}
      \]
    - Boundary conditions:
      \[
      x_0 = \text{{given initial position}}, \quad v_0 = \text{{given initial velocity}}
      \]
      \[
      x_T = \text{{given target position}}, \quad v_T = \text{{given target velocity}}
      \]

4. **Fuel Consumption:**
    - Total fuel spent is given by the sum of |a_t| over all time steps:
      \[
      \text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
      \]

The complete LP model in LaTeX format is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize \( M \)

\subsection*{Subject to}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
v_{t+1} &= v_t + a_t, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
|a_t| &\leq M, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
x_0 &= x_0, \quad v_0 = v_0 \\
x_T &= x_T, \quad v_T = v_T
\end{align*}

\subsection*{Fuel Consumption}
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

This model provides a framework for implementing the solution using LP solvers, which can output the trajectory, velocities, accelerations, and fuel consumption over time.

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

\subsection*{Objective}
Minimize \( M \)

\subsection*{Subject to}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
v_{t+1} &= v_t + a_t, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
|a_t| &\leq M, \quad \forall t \in \{0, 1, \ldots, T-1\} \\
x_0 &= x_0, \quad v_0 = v_0 \\
x_T &= x_T, \quad v_T = v_T
\end{align*}

\subsection*{Fuel Consumption}
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'X0': 0, 
    'V0': 0, 
    'XT': 1, 
    'VT': 0, 
    'T': 20
}

#### Define the LP problem
problem = pulp.LpProblem("Minimize_M", pulp.LpMinimize)

#### Define variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(data['T'] + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(data['T'] + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(data['T'])]
M = pulp.LpVariable('M', lowBound=0, cat='Continuous')

#### Objective function
problem += M

#### Constraints
problem += (x[0] == data['X0'])
problem += (v[0] == data['V0'])
problem += (x[data['T']] == data['XT'])
problem += (v[data['T']] == data['VT'])

for t in range(data['T']):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] <= M)
    problem += (-a[t] <= M)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

