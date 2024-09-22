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

\section*{Rocket Motion Optimization Problem}

\textbf{Variables:}
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t 
\end{align*}

\textbf{Discretized Model:}
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t 
\end{align*}

\textbf{Parameters:}
\begin{align*}
x_0 & : \text{Initial position} \\
v_0 & : \text{Initial velocity} \\
x_T & : \text{Target position} \\
v_T & : \text{Target velocity} \\
T & : \text{Time duration}
\end{align*}

\textbf{Objective:} 
Minimize the maximum thrust required, which is represented as:
\[
\min \max_{t} |a_t|
\]

\textbf{Constraints:}
\begin{align*}
x_0 & = \text{initial position} \\
v_0 & = \text{initial velocity} \\
x_T & = \text{final position} \\
v_T & = \text{final velocity} \\
\end{align*}

Additionally, for all time steps \( t \):
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t 
\end{align*}

\textbf{Output Variables:}
\begin{align*}
\text{"x"} & : [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & : [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & : [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & : \text{total fuel spent}
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

\section*{Rocket Motion Optimization Problem}

\textbf{Variables:}
\begin{align*}
x_t & : \text{Position of the rocket at time } t \\
v_t & : \text{Velocity of the rocket at time } t \\
a_t & : \text{Acceleration of the rocket at time } t 
\end{align*}

\textbf{Discretized Model:}
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t 
\end{align*}

\textbf{Parameters:}
\begin{align*}
x_0 & : \text{Initial position} \\
v_0 & : \text{Initial velocity} \\
x_T & : \text{Target position} \\
v_T & : \text{Target velocity} \\
T & : \text{Time duration}
\end{align*}

\textbf{Objective:} 
Minimize the maximum thrust required, which is represented as:
\[
\min \max_{t} |a_t|
\]

\textbf{Constraints:}
\begin{align*}
x_0 & = \text{initial position} \\
v_0 & = \text{initial velocity} \\
x_T & = \text{final position} \\
v_T & = \text{final velocity} \\
\end{align*}

Additionally, for all time steps \( t \):
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t 
\end{align*}

\textbf{Output Variables:}
\begin{align*}
\text{"x"} & : [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & : [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & : [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & : \text{total fuel spent}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Objective variable: maximum absolute acceleration
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)

#### Objective function: minimize the maximum thrust
problem += max_thrust

#### Constraints
problem += x[0] == x0
problem += v[0] == v0
problem += x[T] == xT
problem += v[T] == vT

#### Dynamics constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    
#### Maximum thrust constraints
for t in range(T):
    problem += a[t] <= max_thrust
    problem += -a[t] <= max_thrust

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

