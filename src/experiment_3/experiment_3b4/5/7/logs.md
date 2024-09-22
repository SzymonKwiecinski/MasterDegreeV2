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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Optimization}

\subsection*{Parameters and Variables}

We are given:
\begin{itemize}
    \item Initial position, $x_0$
    \item Initial velocity, $v_0$
    \item Target position at time $T$, $x_T$
    \item Target velocity at time $T$, $v_T$
    \item Time period $T$
\end{itemize}

Define variables:
\begin{align*}
    x_t &: \text{Position of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    v_t &: \text{Velocity of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    a_t &: \text{Acceleration (thrust) of the rocket at time } t, \, t = 1, 2, \ldots, T \\
    M &: \text{Maximum thrust } = \max_t |a_t|, \, t = 1, 2, \ldots, T
\end{align*}

\subsection*{Objective}

Minimize the maximum thrust:
\[
\min M
\]

\subsection*{Constraints}

The system dynamics are modeled by the following constraints:
\begin{align}
    x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \label{eq:position_update} \\
    v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \label{eq:velocity_update}
\end{align}

Initial conditions:
\begin{align}
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity}
\end{align}

Target conditions at time $T$:
\begin{align}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

Thrust constraints:
\begin{align}
    -M &\leq a_t \leq M, \quad t = 1, 2, \ldots, T
\end{align}

Fuel consumption:
\[
\text{Fuel spent} = \sum_{t=1}^{T} |a_t|
\]

\subsection*{Summary}

The goal is to determine:
\begin{itemize}
    \item $x_t$ for all $t = 1, \ldots, T$
    \item $v_t$ for all $t = 1, \ldots, T$
    \item $a_t$ for all $t = 1, \ldots, T$
    \item Total fuel spent
\end{itemize}

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

\section*{Linear Programming Model for Rocket Optimization}

\subsection*{Parameters and Variables}

We are given:
\begin{itemize}
    \item Initial position, $x_0$
    \item Initial velocity, $v_0$
    \item Target position at time $T$, $x_T$
    \item Target velocity at time $T$, $v_T$
    \item Time period $T$
\end{itemize}

Define variables:
\begin{align*}
    x_t &: \text{Position of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    v_t &: \text{Velocity of the rocket at time } t, \, t = 0, 1, \ldots, T \\
    a_t &: \text{Acceleration (thrust) of the rocket at time } t, \, t = 1, 2, \ldots, T \\
    M &: \text{Maximum thrust } = \max_t |a_t|, \, t = 1, 2, \ldots, T
\end{align*}

\subsection*{Objective}

Minimize the maximum thrust:
\[
\min M
\]

\subsection*{Constraints}

The system dynamics are modeled by the following constraints:
\begin{align}
    x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \label{eq:position_update} \\
    v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1 \label{eq:velocity_update}
\end{align}

Initial conditions:
\begin{align}
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity}
\end{align}

Target conditions at time $T$:
\begin{align}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

Thrust constraints:
\begin{align}
    -M &\leq a_t \leq M, \quad t = 1, 2, \ldots, T
\end{align}

Fuel consumption:
\[
\text{Fuel spent} = \sum_{t=1}^{T} |a_t|
\]

\subsection*{Summary}

The goal is to determine:
\begin{itemize}
    \item $x_t$ for all $t = 1, \ldots, T$
    \item $v_t$ for all $t = 1, \ldots, T$
    \item $a_t$ for all $t = 1, \ldots, T$
    \item Total fuel spent
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Extracting the constants
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(1, T + 1), cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

#### Objective
problem += M

#### Constraints
#### Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

#### Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t + 1])

#### Target conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

#### Thrust constraints
for t in range(1, T + 1):
    problem += (-M <= a[t])
    problem += (a[t] <= M)

#### Solve problem
problem.solve()

#### Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

