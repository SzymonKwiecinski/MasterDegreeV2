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

\section*{Mathematical Model of the Rocket Problem}

\subsection*{Variables}
Let:
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t \\
\end{align*}

\subsection*{Parameters}
Given:
\begin{align*}
x_0 & : \text{Initial position of the rocket} \\
v_0 & : \text{Initial velocity of the rocket} \\
x_T & : \text{Target position of the rocket at time } T \\
v_T & : \text{Target velocity of the rocket at time } T \\
T & : \text{Total time steps} \\
\end{align*}

\subsection*{Dynamic Equations}
The dynamics of the rocket is described by the following equations:
\begin{align}
x_{t+1} &= x_t + v_t \label{eq:position} \\
v_{t+1} &= v_t + a_t \label{eq:velocity}
\end{align}

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which can be expressed as:
\begin{equation}
\min \max_{t} |a_t| \label{eq:objective}
\end{equation}

\subsection*{Constraints}
The final conditions we wish to achieve are:
\begin{align}
x_T &= x_T \label{eq:final_position} \\
v_T &= v_T \label{eq:final_velocity}
\end{align}

\subsection*{Fuel Consumption}
The fuel consumption is related to the acceleration as follows:
\begin{equation}
\text{Fuel Spent} = \sum_{t=0}^{T-1} |a_t| \label{eq:fuel}
\end{equation}

\subsection*{Output Variables}
The output should contain:
\begin{align*}
x & : [x_i \text{ for } i = 0, ..., T] \\
v & : [v_i \text{ for } i = 0, ..., T] \\
a & : [a_i \text{ for } i = 0, ..., T] \\
\text{fuel\_spend} & : \text{Total fuel spent by the rocket}
\end{align*}

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

\section*{Mathematical Model of the Rocket Problem}

\subsection*{Variables}
Let:
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t \\
\end{align*}

\subsection*{Parameters}
Given:
\begin{align*}
x_0 & : \text{Initial position of the rocket} \\
v_0 & : \text{Initial velocity of the rocket} \\
x_T & : \text{Target position of the rocket at time } T \\
v_T & : \text{Target velocity of the rocket at time } T \\
T & : \text{Total time steps} \\
\end{align*}

\subsection*{Dynamic Equations}
The dynamics of the rocket is described by the following equations:
\begin{align}
x_{t+1} &= x_t + v_t \label{eq:position} \\
v_{t+1} &= v_t + a_t \label{eq:velocity}
\end{align}

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which can be expressed as:
\begin{equation}
\min \max_{t} |a_t| \label{eq:objective}
\end{equation}

\subsection*{Constraints}
The final conditions we wish to achieve are:
\begin{align}
x_T &= x_T \label{eq:final_position} \\
v_T &= v_T \label{eq:final_velocity}
\end{align}

\subsection*{Fuel Consumption}
The fuel consumption is related to the acceleration as follows:
\begin{equation}
\text{Fuel Spent} = \sum_{t=0}^{T-1} |a_t| \label{eq:fuel}
\end{equation}

\subsection*{Output Variables}
The output should contain:
\begin{align*}
x & : [x_i \text{ for } i = 0, ..., T] \\
v & : [v_i \text{ for } i = 0, ..., T] \\
a & : [a_i \text{ for } i = 0, ..., T] \\
\text{fuel\_spend} & : \text{Total fuel spent by the rocket}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = json.loads('{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}')
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

#### Objective Function: Minimize maximum acceleration
max_a = pulp.LpVariable("max_a", lowBound=0)
problem += max_a

#### Dynamic Equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

#### Initial Conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

#### Final Conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

#### Constraints for the maximum thrust
for t in range(T):
    problem += a[t] <= max_a, f"Max_Thrust_Upper_{t}"
    problem += a[t] >= -max_a, f"Max_Thrust_Lower_{t}"

#### Solve the problem
problem.solve()

#### Output the results
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

print(f"x: {x_values}")
print(f"v: {v_values}")
print(f"a: {a_values}")
print(f"fuel_spent: {fuel_spent}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

