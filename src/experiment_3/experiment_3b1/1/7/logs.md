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

\section*{Mathematical Model for Rocket Trajectory Control}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
\end{itemize}

\subsection*{Discretized Model}
The dynamics of the rocket can be represented using the following equations:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which is represented as:
\[
\min \max_t |a_t|
\]

\subsection*{Constraints}
Given:
\begin{itemize}
    \item Initial position and velocity: \( x_0, v_0 \)
    \item Target position and velocity: \( x_T, v_T \)
    \item Total time: \( T \)
\end{itemize}

The model must satisfy the following conditions:
\[
x_T = x_T \quad \text{(target position)}
\]
\[
v_T = v_T \quad \text{(target velocity)}
\]

The fuel consumption at each time step is proportional to the acceleration:
\[
\text{Fuel Spent} = \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Inputs}
The input format is:
\[
\{ 
    x_0, 
    v_0, 
    x_T, 
    v_T, 
    T 
\}
\]

\subsection*{Outputs}
The outputs required are:
\[
\{ 
    x = [x_i \, \forall i \in \{0, 1, \ldots, T\}], 
    v = [v_i \, \forall i \in \{0, 1, \ldots, T\}], 
    a = [a_i \, \forall i \in \{0, 1, \ldots, T\}], 
    \text{fuel\_spend} = \text{Total fuel spent} 
\}
\]

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

\section*{Mathematical Model for Rocket Trajectory Control}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
\end{itemize}

\subsection*{Discretized Model}
The dynamics of the rocket can be represented using the following equations:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which is represented as:
\[
\min \max_t |a_t|
\]

\subsection*{Constraints}
Given:
\begin{itemize}
    \item Initial position and velocity: \( x_0, v_0 \)
    \item Target position and velocity: \( x_T, v_T \)
    \item Total time: \( T \)
\end{itemize}

The model must satisfy the following conditions:
\[
x_T = x_T \quad \text{(target position)}
\]
\[
v_T = v_T \quad \text{(target velocity)}
\]

The fuel consumption at each time step is proportional to the acceleration:
\[
\text{Fuel Spent} = \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Inputs}
The input format is:
\[
\{ 
    x_0, 
    v_0, 
    x_T, 
    v_T, 
    T 
\}
\]

\subsection*{Outputs}
The outputs required are:
\[
\{ 
    x = [x_i \, \forall i \in \{0, 1, \ldots, T\}], 
    v = [v_i \, \forall i \in \{0, 1, \ldots, T\}], 
    a = [a_i \, \forall i \in \{0, 1, \ldots, T\}], 
    \text{fuel\_spend} = \text{Total fuel spent} 
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("Rocket_Trajectory_Control", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)      #### acceleration
max_a = pulp.LpVariable("max_a", lowBound=0)                 #### max acceleration

#### Objective Function
problem += max_a, "Minimize_Max_Thrust"

#### Constraints
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"
    problem += a[t] <= max_a, f"Max_Thrust_Upper_{t}"
    problem += a[t] >= -max_a, f"Max_Thrust_Lower_{t}"

problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

#### Solve the problem
problem.solve()

#### Collecting Outputs
x_values = [x[t].varValue for t in range(T + 1)]
v_values = [v[t].varValue for t in range(T + 1)]
a_values = [a[t].varValue for t in range(T)]
fuel_spent = sum(abs(a[t].varValue) for t in range(T))

#### Print Results
print(f"x = {x_values}")
print(f"v = {v_values}")
print(f"a = {a_values}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total fuel spent: {fuel_spent}')
```

