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
To solve this problem, we need to formulate a Linear Programming (LP) model. The objective is to minimize the maximum thrust required, which corresponds to minimizing the maximum value of \(|a_t|\) across all time steps. We have the following constraints:

1. The position update constraint: \(x_{t+1} = x_t + v_t\)
2. The velocity update constraint: \(v_{t+1} = v_t + a_t\)
3. The initial conditions: \(x(0) = x_0, v(0) = v_0\)
4. The terminal conditions: \(x(T) = x_T, v(T) = v_T\)
5. The objective is to minimize the maximum absolute value of \(a_t\).

Let's define the model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\paragraph{Decision Variables:}
\begin{align*}
x_t &\quad \text{Position of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
v_t &\quad \text{Velocity of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
a_t &\quad \text{Acceleration of the rocket at time } t, \quad t = 0, 1, \ldots, T-1 \\
M &\quad \text{Maximum absolute value of the acceleration, } M \geq |a_t|, \quad t = 0, 1, \ldots, T-1
\end{align*}

\paragraph{Objective:}
\[
\min M
\]

\paragraph{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= x_0, \\
v_0 &= v_0, \\
x_T &= x_T, \\
v_T &= v_T, \\
-M &\leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\end{align*}

\paragraph{Fuel Consumption:}
To calculate total fuel spent, we assume it is proportional to the sum of the absolute values of the accelerations:
\[
\text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

This model captures the necessary constraints and objective to find the optimal trajectory to minimize the maximum thrust required.

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

\paragraph{Decision Variables:}
\begin{align*}
x_t &\quad \text{Position of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
v_t &\quad \text{Velocity of the rocket at time } t, \quad t = 0, 1, \ldots, T \\
a_t &\quad \text{Acceleration of the rocket at time } t, \quad t = 0, 1, \ldots, T-1 \\
M &\quad \text{Maximum absolute value of the acceleration, } M \geq |a_t|, \quad t = 0, 1, \ldots, T-1
\end{align*}

\paragraph{Objective:}
\[
\min M
\]

\paragraph{Subject to:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
x_0 &= x_0, \\
v_0 &= v_0, \\
x_T &= x_T, \\
v_T &= v_T, \\
-M &\leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\end{align*}

\paragraph{Fuel Consumption:}
To calculate total fuel spent, we assume it is proportional to the sum of the absolute values of the accelerations:
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

#### Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("Rocket_Acceleration_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Position", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("Velocity", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("Acceleration", range(T), lowBound=None)
M = pulp.LpVariable("M", lowBound=0)

#### Objective Function
problem += M

#### Initial Conditions
problem += x[0] == X0
problem += v[0] == V0

#### Final Conditions
problem += x[T] == XT
problem += v[T] == VT

#### Dynamics Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

#### Acceleration Bounds
for t in range(T):
    problem += -M <= a[t]
    problem += a[t] <= M

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

