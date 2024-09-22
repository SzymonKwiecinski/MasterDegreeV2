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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time dynamics of the rocket can be expressed as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Given the problem parameters:
- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Time horizon: \( T \)

The goal is to minimize the maximum thrust required, denoted as \( \max_t |a_t| \).

\subsection*{Objective Function}
The objective is to minimize the maximum absolute acceleration:

\[
\text{Minimize } Z = \max_{t=0, \ldots, T} |a_t|
\]

\subsection*{Constraints}
The evolution of the rocket's state can be constrained as follows:
1. For each time step \( t \) from \( 0 \) to \( T-1 \):
   \begin{align}
       x_{t+1} &= x_t + v_t \\
       v_{t+1} &= v_t + a_t
   \end{align}
   
2. At the final time step \( T \):
   \begin{align}
       x_T &= x_T \\
       v_T &= v_T
   \end{align}

3. The thrust constraints can be modeled as:
   \[
   -Z \leq a_t \leq Z, \quad \forall t = 0, 1, \ldots, T
   \]

\subsection*{Output Variables}
The output variables are defined as:
\begin{itemize}
    \item \( \text{"x"}: [x_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"v"}: [v_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"a"}: [a_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"fuel\_spend"}: \text{total fuel spent} \)
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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time dynamics of the rocket can be expressed as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

Given the problem parameters:
- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Time horizon: \( T \)

The goal is to minimize the maximum thrust required, denoted as \( \max_t |a_t| \).

\subsection*{Objective Function}
The objective is to minimize the maximum absolute acceleration:

\[
\text{Minimize } Z = \max_{t=0, \ldots, T} |a_t|
\]

\subsection*{Constraints}
The evolution of the rocket's state can be constrained as follows:
1. For each time step \( t \) from \( 0 \) to \( T-1 \):
   \begin{align}
       x_{t+1} &= x_t + v_t \\
       v_{t+1} &= v_t + a_t
   \end{align}
   
2. At the final time step \( T \):
   \begin{align}
       x_T &= x_T \\
       v_T &= v_T
   \end{align}

3. The thrust constraints can be modeled as:
   \[
   -Z \leq a_t \leq Z, \quad \forall t = 0, 1, \ldots, T
   \]

\subsection*{Output Variables}
The output variables are defined as:
\begin{itemize}
    \item \( \text{"x"}: [x_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"v"}: [v_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"a"}: [a_i \text{ for } i = 0, \ldots, T] \)
    \item \( \text{"fuel\_spend"}: \text{total fuel spent} \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Define decision variables
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=None)
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
Z = pulp.LpVariable("Z", lowBound=0)

#### Objective Function: Minimize the maximum absolute acceleration
problem += Z

#### Constraints
#### Initial conditions
problem += x[0] == X0
problem += v[0] == V0

#### Dynamics and thrust constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += -Z <= a[t]
    problem += a[t] <= Z

#### Final conditions
problem += x[T] == XT
problem += v[T] == VT

#### Solve the problem
problem.solve()

#### Output results
for t in range(T + 1):
    print(f"x[{t}]: {x[t].varValue}, v[{t}]: {v[t].varValue}, a[{t}]: {a[t].varValue}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

