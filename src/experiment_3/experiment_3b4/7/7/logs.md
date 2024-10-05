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
The problem described is a time-discretized control problem for a rocket, modeled as a linear program to minimize the maximum thrust (acceleration). We can set up the Linear Programming model in LaTeX format as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Problem Description}

We are given a rocket with:
\begin{itemize}
    \item Initial position \( x_0 \) and initial velocity \( v_0 \).
    \item Target position \( x_T \) and target velocity \( v_T \) at time \( T \).
\end{itemize}

Our goal is to minimize the maximum thrust required, i.e., \( \max_t |a_t| \).

\subsection*{Variables}

\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \).
    \item \( v_t \): Velocity of the rocket at time \( t \).
    \item \( a_t \): Acceleration (thrust) of the rocket at time \( t \).
\end{itemize}

\subsection*{Constraints}

For \( t = 0, 1, \ldots, T-1 \):
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Initial conditions:
\begin{align}
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity}
\end{align}

Final conditions:
\begin{align}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

Objective:
\begin{align}
    \text{Minimize } z = \max_{0 \le t < T} |a_t|
\end{align}

\subsection*{Linearization of Objective}

Introduce auxiliary variable \( z \) such that:
\begin{align}
    z \geq a_t &\quad \forall t \\
    z \geq -a_t &\quad \forall t
\end{align}

Thus, the linear programming problem becomes:
\begin{align}
    \text{Minimize } z
\end{align}

\subsection*{Fuel Consumption}

The total fuel spent, which is proportional to the absolute sum of accelerations, can be calculated as:
\begin{align}
    \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
\end{align}

\end{document}
```

This LaTeX code sets up a linear programming model to determine the discrete-time control inputs \( a_t \) that lead to the desired trajectory for the rocket while minimizing the maximum acceleration needed. The constraints ensure that the rocket follows the correct dynamics, starting and ending at the specified positions and velocities. The linearization introduces an auxiliary variable \( z \) to handle the minimization of the maximum absolute acceleration.

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

\subsection*{Problem Description}

We are given a rocket with:
\begin{itemize}
    \item Initial position \( x_0 \) and initial velocity \( v_0 \).
    \item Target position \( x_T \) and target velocity \( v_T \) at time \( T \).
\end{itemize}

Our goal is to minimize the maximum thrust required, i.e., \( \max_t |a_t| \).

\subsection*{Variables}

\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \).
    \item \( v_t \): Velocity of the rocket at time \( t \).
    \item \( a_t \): Acceleration (thrust) of the rocket at time \( t \).
\end{itemize}

\subsection*{Constraints}

For \( t = 0, 1, \ldots, T-1 \):
\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Initial conditions:
\begin{align}
    x_0 &= \text{given initial position} \\
    v_0 &= \text{given initial velocity}
\end{align}

Final conditions:
\begin{align}
    x_T &= \text{target position} \\
    v_T &= \text{target velocity}
\end{align}

Objective:
\begin{align}
    \text{Minimize } z = \max_{0 \le t < T} |a_t|
\end{align}

\subsection*{Linearization of Objective}

Introduce auxiliary variable \( z \) such that:
\begin{align}
    z \geq a_t &\quad \forall t \\
    z \geq -a_t &\quad \forall t
\end{align}

Thus, the linear programming problem becomes:
\begin{align}
    \text{Minimize } z
\end{align}

\subsection*{Fuel Consumption}

The total fuel spent, which is proportional to the absolute sum of accelerations, can be calculated as:
\begin{align}
    \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Initialize the problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Auxiliary variable for maximum thrust
z = pulp.LpVariable('z', lowBound=0)

#### Objective
problem += z, "Minimize maximum thrust"

#### Constraints
#### Initial conditions
problem += (x[0] == x0), "Initial_Position"
problem += (v[0] == v0), "Initial_Velocity"

#### Dynamics equations
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Update_Time_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Update_Time_{t}"

#### Final conditions
problem += (x[T] == xT), "Final_Position"
problem += (v[T] == vT), "Final_Velocity"

#### Maximum thrust constraints
for t in range(T):
    problem += (z >= a[t]), f"Max_Thrust_Positive_Time_{t}"
    problem += (z >= -a[t]), f"Max_Thrust_Negative_Time_{t}"

#### Solve the problem
problem.solve()

#### Print the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

