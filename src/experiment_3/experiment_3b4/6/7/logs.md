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
To formulate the given problem as a linear programming (LP) model, we aim to minimize the maximum thrust required, represented by \(\max_t |a_t|\), subject to the discretized system dynamics and initial and final conditions. Here's the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Optimization}

\subsection*{Given:}
\begin{itemize}
    \item Initial position: \(x_0\)
    \item Initial velocity: \(v_0\)
    \item Target position at time \(T\): \(x_T\)
    \item Target velocity at time \(T\): \(v_T\)
    \item Time horizon: \(T\)
\end{itemize}

\subsection*{Objective:}
Minimize the maximum thrust required, i.e., \(\max_{t} |a_t|\).

\subsection*{Constraints:}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
    & v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
    & x_0 \text{ is given}, \\
    & v_0 \text{ is given}, \\
    & x_T \text{ is given}, \\
    & v_T \text{ is given}.
\end{align}

\subsection*{Decision Variables:}
\begin{align}
    & x_t, \quad \text{position of the rocket at time } t, \\
    & v_t, \quad \text{velocity of the rocket at time } t, \\
    & a_t, \quad \text{acceleration (thrust) of the rocket at time } t.
\end{align}

\subsection*{Objective Function:}
\begin{align}
    \text{Minimize } & M, \\
    \text{subject to } & -M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1.
\end{align}

\subsection*{Fuel Spend:}
The total fuel spent is equivalent to the sum of the magnitude of accelerations:
\begin{align}
    \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|.
\end{align}

\end{document}
```

This model captures the dynamics of the rocket's movement and allows for the minimization of the maximum absolute acceleration, which correlates to minimizing the maximum thrust and, consequently, the fuel consumption. The total fuel spend is calculated as the sum of the absolute values of the accelerations across the time horizon.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Optimization}

\subsection*{Given:}
\begin{itemize}
    \item Initial position: \(x_0\)
    \item Initial velocity: \(v_0\)
    \item Target position at time \(T\): \(x_T\)
    \item Target velocity at time \(T\): \(v_T\)
    \item Time horizon: \(T\)
\end{itemize}

\subsection*{Objective:}
Minimize the maximum thrust required, i.e., \(\max_{t} |a_t|\).

\subsection*{Constraints:}
\begin{align}
    & x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
    & v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
    & x_0 \text{ is given}, \\
    & v_0 \text{ is given}, \\
    & x_T \text{ is given}, \\
    & v_T \text{ is given}.
\end{align}

\subsection*{Decision Variables:}
\begin{align}
    & x_t, \quad \text{position of the rocket at time } t, \\
    & v_t, \quad \text{velocity of the rocket at time } t, \\
    & a_t, \quad \text{acceleration (thrust) of the rocket at time } t.
\end{align}

\subsection*{Objective Function:}
\begin{align}
    \text{Minimize } & M, \\
    \text{subject to } & -M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1.
\end{align}

\subsection*{Fuel Spend:}
The total fuel spent is equivalent to the sum of the magnitude of accelerations:
\begin{align}
    \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|.
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse JSON data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Parameters
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create a LP minimization problem
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T))
M = pulp.LpVariable("M", lowBound=0)

#### Objective Function: Minimize maximum thrust required
problem += M, "Minimize_Maximum_Thrust"

#### Constraints

#### Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

#### Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

#### Dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (-M <= a[t], f"Negative_Thrust_Bound_{t}")
    problem += (a[t] <= M, f"Positive_Thrust_Bound_{t}")

#### Solve the problem
problem.solve()

#### Get the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


