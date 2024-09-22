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

\section*{Rocket Trajectory Optimization Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The rocket's motion is governed by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We have control over the acceleration \( a_t \), which is proportional to the rate of fuel consumption at time \( t \). Given the initial conditions \( x_0 \) and \( v_0 \), we seek to reach the target position \( x_T \) with the target velocity \( v_T \) at time \( T \) while minimizing the maximum thrust required, given by \( \max_t |a_t| \).

\subsection*{Input Parameters}
The input parameters are defined as follows:

\begin{itemize}
    \item \( x_0 \): Initial position of the rocket
    \item \( v_0 \): Initial velocity of the rocket
    \item \( x_T \): Target position of the rocket
    \item \( v_T \): Target velocity of the rocket
    \item \( T \): Total time
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which can be expressed mathematically as:

\[
\text{Minimize } \max_{t=0,1,\ldots,T} |a_t|
\]

\subsection*{Output Variables}
The output variables, which represent the rocket's trajectory and total fuel spent, are defined as follows:

\begin{itemize}
    \item \( x = [x_i, \; i = 0, \ldots, T] \): List of positions at each time step
    \item \( v = [v_i, \; i = 0, \ldots, T] \): List of velocities at each time step
    \item \( a = [a_i, \; i = 0, \ldots, T] \): List of accelerations at each time step
    \item \text{fuel\_spend}: Total fuel spent by the rocket
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

\section*{Rocket Trajectory Optimization Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The rocket's motion is governed by the following discrete-time equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We have control over the acceleration \( a_t \), which is proportional to the rate of fuel consumption at time \( t \). Given the initial conditions \( x_0 \) and \( v_0 \), we seek to reach the target position \( x_T \) with the target velocity \( v_T \) at time \( T \) while minimizing the maximum thrust required, given by \( \max_t |a_t| \).

\subsection*{Input Parameters}
The input parameters are defined as follows:

\begin{itemize}
    \item \( x_0 \): Initial position of the rocket
    \item \( v_0 \): Initial velocity of the rocket
    \item \( x_T \): Target position of the rocket
    \item \( v_T \): Target velocity of the rocket
    \item \( T \): Total time
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which can be expressed mathematically as:

\[
\text{Minimize } \max_{t=0,1,\ldots,T} |a_t|
\]

\subsection*{Output Variables}
The output variables, which represent the rocket's trajectory and total fuel spent, are defined as follows:

\begin{itemize}
    \item \( x = [x_i, \; i = 0, \ldots, T] \): List of positions at each time step
    \item \( v = [v_i, \; i = 0, \ldots, T] \): List of velocities at each time step
    \item \( a = [a_i, \; i = 0, \ldots, T] \): List of accelerations at each time step
    \item \text{fuel\_spend}: Total fuel spent by the rocket
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Define variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T + 1)]
max_a = pulp.LpVariable("max_a", lowBound=0)

#### Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

#### Dynamic equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])

#### Target conditions
problem += (x[T] == xT)
problem += (v[T] == vT)

#### Objective: Minimize the maximum thrust required
for t in range(T + 1):
    problem += (max_a >= a[t])

problem += pulp.lpSum([max_a])  #### Minimize max_a

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

