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
To model this problem as a Linear Programming (LP) problem, we'll create a formulation that captures the dynamics of the rocket's motion while minimizing the total fuel consumption. The constraints will ensure that the rocket follows the required path and velocities at each time step.

Here is the mathematical model for the given problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Control}

\subsection*{Given Parameters}
\begin{itemize}
    \item Initial position, $x_0$
    \item Initial velocity, $v_0$
    \item Target position at time $T$, $x_T$
    \item Target velocity at time $T$, $v_T$
    \item Time horizon, $T$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$, for $t = 1, \ldots, T$
    \item $v_t$: Velocity of the rocket at time $t$, for $t = 1, \ldots, T$
    \item $a_t$: Acceleration of the rocket at time $t$, for $t = 0, \ldots, T-1$
\end{itemize}

\subsection*{Objective Function}
Minimize the total fuel consumption, which is proportional to the absolute value of the acceleration:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
    & v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
    & x_0 \text{ is given} \\
    & v_0 \text{ is given} \\
    & x_T \text{ is given} \\
    & v_T \text{ is given}
\end{align}

To transform the absolute value in the objective function, we introduce auxiliary variables $u_t$ such that:
\begin{align}
    & u_t \geq a_t \\
    & u_t \geq -a_t
\end{align}
Thus, the objective function becomes:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\end{document}
```

This LP formulation aims to control the acceleration of a rocket such that it reaches the desired final position and velocity while minimizing fuel consumption. The auxiliary variables $u_t$ are introduced to handle the absolute value in the objective function, converting it into a linear constraint.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Control}

\subsection*{Given Parameters}
\begin{itemize}
    \item Initial position, $x_0$
    \item Initial velocity, $v_0$
    \item Target position at time $T$, $x_T$
    \item Target velocity at time $T$, $v_T$
    \item Time horizon, $T$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$, for $t = 1, \ldots, T$
    \item $v_t$: Velocity of the rocket at time $t$, for $t = 1, \ldots, T$
    \item $a_t$: Acceleration of the rocket at time $t$, for $t = 0, \ldots, T-1$
\end{itemize}

\subsection*{Objective Function}
Minimize the total fuel consumption, which is proportional to the absolute value of the acceleration:
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Constraints}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
    & v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
    & x_0 \text{ is given} \\
    & v_0 \text{ is given} \\
    & x_T \text{ is given} \\
    & v_T \text{ is given}
\end{align}

To transform the absolute value in the objective function, we introduce auxiliary variables $u_t$ such that:
\begin{align}
    & u_t \geq a_t \\
    & u_t \geq -a_t
\end{align}
Thus, the objective function becomes:
\[
\min \sum_{t=0}^{T-1} u_t
\]

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

#### Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create the LP problem
problem = pulp.LpProblem("RocketPathControl", pulp.LpMinimize)

#### Decision variables
x_t = pulp.LpVariable.dicts("x", range(T+1))
v_t = pulp.LpVariable.dicts("v", range(T+1))
a_t = pulp.LpVariable.dicts("a", range(T))
u_t = pulp.LpVariable.dicts("u", range(T), lowBound=0)

#### Objective function
problem += pulp.lpSum(u_t[t] for t in range(T)), "TotalFuelConsumption"

#### Constraints
problem += (x_t[0] == x_0), "InitialPosition"
problem += (v_t[0] == v_0), "InitialVelocity"
problem += (x_t[T] == x_T), "FinalPosition"
problem += (v_t[T] == v_T), "FinalVelocity"

for t in range(T):
    problem += (x_t[t+1] == x_t[t] + v_t[t]), f"PositionUpdate_{t}"
    problem += (v_t[t+1] == v_t[t] + a_t[t]), f"VelocityUpdate_{t}"
    problem += (u_t[t] >= a_t[t]), f"Auxiliary_1_{t}"
    problem += (u_t[t] >= -a_t[t]), f"Auxiliary_2_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

