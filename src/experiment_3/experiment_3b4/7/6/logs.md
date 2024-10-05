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
To formulate this problem as a Linear Programming (LP) problem, we need to describe the system of equations and constraints according to the given information and objective. We aim to minimize the total fuel consumption subject to the given dynamics and constraints.

The mathematical model in LaTeX format is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Optimization Problem}

\subsection*{Problem Formulation}

Given:
\begin{align*}
    & x_0 \quad \text{(initial position)} \\
    & v_0 \quad \text{(initial velocity)} \\
    & x_T \quad \text{(target position at time } T\text{)} \\
    & v_T \quad \text{(target velocity at time } T\text{)} \\
    & T \quad \text{(final time)}
\end{align*}

We are tasked with determining the sequence of accelerations \( a_t \) that minimizes the total fuel consumption:

\[
\min \sum_{t=0}^{T-1} |a_t|
\]

Subject to the discrete-time dynamics:
\begin{align*}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
\end{align*}

And the boundary conditions:
\begin{align*}
    x_0 &= \text{given} \\
    v_0 &= \text{given} \\
    x_T &= \text{given} \\
    v_T &= \text{given}
\end{align*}

To incorporate the absolute value into the linear program, we represent each \( |a_t| \) using an auxiliary variable \( u_t \):

\begin{align*}
    a_t &\leq u_t \quad \forall t = 0, 1, \ldots, T-1 \\
    -a_t &\leq u_t \quad \forall t = 0, 1, \ldots, T-1
\end{align*}

Thus, the objective function becomes:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Solution Format}

The output will be represented as:
\begin{itemize}
    \item \texttt{x}: List of positions at each time step from 0 to \( T \).
    \item \texttt{v}: List of velocities at each time step from 0 to \( T \).
    \item \texttt{a}: List of accelerations at each time step from 0 to \( T \).
    \item \texttt{fuel\_spend}: Total fuel spent.
\end{itemize}

\end{document}
```

This LaTeX document outlines the LP formulation for minimizing the rocket's fuel consumption while achieving the given constraints on position and velocity. The auxiliary variables \( u_t \) are used to transform the absolute values in the objective function into a linear form suitable for LP.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Optimization Problem}

\subsection*{Problem Formulation}

Given:
\begin{align*}
    & x_0 \quad \text{(initial position)} \\
    & v_0 \quad \text{(initial velocity)} \\
    & x_T \quad \text{(target position at time } T\text{)} \\
    & v_T \quad \text{(target velocity at time } T\text{)} \\
    & T \quad \text{(final time)}
\end{align*}

We are tasked with determining the sequence of accelerations \( a_t \) that minimizes the total fuel consumption:

\[
\min \sum_{t=0}^{T-1} |a_t|
\]

Subject to the discrete-time dynamics:
\begin{align*}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
\end{align*}

And the boundary conditions:
\begin{align*}
    x_0 &= \text{given} \\
    v_0 &= \text{given} \\
    x_T &= \text{given} \\
    v_T &= \text{given}
\end{align*}

To incorporate the absolute value into the linear program, we represent each \( |a_t| \) using an auxiliary variable \( u_t \):

\begin{align*}
    a_t &\leq u_t \quad \forall t = 0, 1, \ldots, T-1 \\
    -a_t &\leq u_t \quad \forall t = 0, 1, \ldots, T-1
\end{align*}

Thus, the objective function becomes:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Solution Format}

The output will be represented as:
\begin{itemize}
    \item \texttt{x}: List of positions at each time step from 0 to \( T \).
    \item \texttt{v}: List of velocities at each time step from 0 to \( T \).
    \item \texttt{a}: List of accelerations at each time step from 0 to \( T \).
    \item \texttt{fuel\_spend}: Total fuel spent.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Define parameters
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create a linear programming problem
problem = pulp.LpProblem('RocketOptimization', pulp.LpMinimize)

#### Define variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None, upBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, upBound=None, cat='Continuous')
u = pulp.LpVariable.dicts("u", range(T), lowBound=0, upBound=None, cat='Continuous')  #### Auxiliary variables for |a_t|

#### Objective function: Minimize the total fuel consumption
problem += pulp.lpSum(u[t] for t in range(T))

#### Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

#### Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Dynamics_Velocity_{t}")

#### Boundary conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

#### Constraints for absolute value representation
for t in range(T):
    problem += (a[t] <= u[t], f"Abs_Constraint_Pos_{t}")
    problem += (-a[t] <= u[t], f"Abs_Constraint_Neg_{t}")

#### Solve the problem
problem.solve()

#### Extract the results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]

#### Calculate total fuel spent
fuel_spent = pulp.value(problem.objective)

#### Print the results
print(f"x: {x_values}")
print(f"v: {v_values}")
print(f"a: {a_values}")
print(f"fuel_spend: {fuel_spent}")

#### Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')
```

