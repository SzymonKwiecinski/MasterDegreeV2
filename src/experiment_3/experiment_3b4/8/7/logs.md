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
To model this problem as a Linear Programming (LP) problem, we need to define the decision variables, the objective function, and the constraints. The decision variables are the accelerations \( a_t \) for \( t = 0, 1, \ldots, T-1 \), and the positions \( x_t \) and velocities \( v_t \) for \( t = 1, \ldots, T \). 

We aim to minimize the maximum magnitude of acceleration, which translates to minimizing the maximum thrust required \(\text{max}_t |a_t|\). The total fuel spent is the sum of the absolute values of the accelerations over all time periods.

Here is how you can formulate the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\textbf{Objective:}
\[
\min \max_{t=0, \ldots, T-1} |a_t|
\]

\textbf{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= x_0 \quad \text{(Given)} \\
v_0 &= v_0 \quad \text{(Given)} \\
x_T &= x_T \quad \text{(Target position)} \\
v_T &= v_T \quad \text{(Target velocity)} \\
|a_t| &\leq M, \quad t = 0, 1, \ldots, T-1
\end{align*}

\textbf{Where:}
\begin{align*}
x_t &: \text{position of the rocket at time } t \\
v_t &: \text{velocity of the rocket at time } t \\
a_t &: \text{acceleration (control variable) at time } t \\
M &: \text{maximum allowable thrust (fuel consumption)} \\
\end{align*}

\textbf{Fuel Consumption:}
\[
\text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

In this formulation:
- The objective function is minimizing the maximum thrust required.
- The constraints include the dynamic equations for position and velocity, the initial conditions, and the final conditions.
- We use \( M \) as the variable for the maximum absolute value of the accelerations, which is the thrust to minimize.
- Finally, the total fuel spent is calculated as the sum of absolute accelerations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\textbf{Objective:}
\[
\min \max_{t=0, \ldots, T-1} |a_t|
\]

\textbf{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= x_0 \quad \text{(Given)} \\
v_0 &= v_0 \quad \text{(Given)} \\
x_T &= x_T \quad \text{(Target position)} \\
v_T &= v_T \quad \text{(Target velocity)} \\
|a_t| &\leq M, \quad t = 0, 1, \ldots, T-1
\end{align*}

\textbf{Where:}
\begin{align*}
x_t &: \text{position of the rocket at time } t \\
v_t &: \text{velocity of the rocket at time } t \\
a_t &: \text{acceleration (control variable) at time } t \\
M &: \text{maximum allowable thrust (fuel consumption)} \\
\end{align*}

\textbf{Fuel Consumption:}
\[
\text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Initialize problem
problem = pulp.LpProblem("Rocket_Landing_Optimization", pulp.LpMinimize)

#### Define variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1))
v = pulp.LpVariable.dicts("v", range(data['T'] + 1))
a = pulp.LpVariable.dicts("a", range(data['T']), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

#### Objective Function
problem += M

#### Constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t]), f"Position_Constraint_{t}"
    problem += (v[t + 1] == v[t] + a[t]), f"Velocity_Constraint_{t}"
    problem += (a[t] <= M), f"Max_Thrust_Constraint_Pos_{t}"
    problem += (a[t] >= -M), f"Max_Thrust_Constraint_Neg_{t}"

#### Initial conditions
problem += (x[0] == data['X0']), "Initial_Position"
problem += (v[0] == data['V0']), "Initial_Velocity"

#### Final conditions
problem += (x[data['T']] == data['XT']), "Final_Position"
problem += (v[data['T']] == data['VT']), "Final_Velocity"

#### Solve problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

