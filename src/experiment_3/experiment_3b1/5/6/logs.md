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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Rocket Motion Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$
    \item $v_t$: Velocity of the rocket at time $t$
    \item $a_t$: Acceleration of the rocket at time $t$
\end{itemize}

\textbf{Given:}
\begin{itemize}
    \item Initial position: $x_0$
    \item Initial velocity: $v_0$
    \item Target position: $x_T$
    \item Target velocity: $v_T$
    \item Total time: $T$
\end{itemize}

\textbf{Model:}
The discrete-time motion model of the rocket can be expressed as:
\[
\begin{align*}
x_{t+1} &= x_t + v_t \\
v_{t+1} &= v_t + a_t
\end{align*}
\]

\textbf{Objective:}
Minimize the total fuel consumed, which is proportional to the total acceleration over time:
\[
\text{Minimize } Z = \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Constraints:}
\begin{align*}
x_0 &= x_0 \\
v_0 &= v_0 \\
x_T &= x_T \\
v_T &= v_T \\
\end{align*}
The relationship between position, velocity, and acceleration must hold for each time step:
\[
\begin{align*}
x_{t+1} - x_t &= v_t \\
v_{t+1} - v_t &= a_t
\end{align*}
\]

The fuel consumption must be non-negative and can be expressed as:
\[
|a_t| \geq 0
\]

\textbf{Output:}
The output will consist of:
\begin{itemize}
    \item A list of positions: $x = [x_i \text{ for } i = 0, \ldots, T]$
    \item A list of velocities: $v = [v_i \text{ for } i = 0, \ldots, T]$
    \item A list of accelerations: $a = [a_i \text{ for } i = 0, \ldots, T]$
    \item Total fuel spent: $\text{fuel\_spend} = Z$
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

\section*{Rocket Motion Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item $x_t$: Position of the rocket at time $t$
    \item $v_t$: Velocity of the rocket at time $t$
    \item $a_t$: Acceleration of the rocket at time $t$
\end{itemize}

\textbf{Given:}
\begin{itemize}
    \item Initial position: $x_0$
    \item Initial velocity: $v_0$
    \item Target position: $x_T$
    \item Target velocity: $v_T$
    \item Total time: $T$
\end{itemize}

\textbf{Model:}
The discrete-time motion model of the rocket can be expressed as:
\[
\begin{align*}
x_{t+1} &= x_t + v_t \\
v_{t+1} &= v_t + a_t
\end{align*}
\]

\textbf{Objective:}
Minimize the total fuel consumed, which is proportional to the total acceleration over time:
\[
\text{Minimize } Z = \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Constraints:}
\begin{align*}
x_0 &= x_0 \\
v_0 &= v_0 \\
x_T &= x_T \\
v_T &= v_T \\
\end{align*}
The relationship between position, velocity, and acceleration must hold for each time step:
\[
\begin{align*}
x_{t+1} - x_t &= v_t \\
v_{t+1} - v_t &= a_t
\end{align*}
\]

The fuel consumption must be non-negative and can be expressed as:
\[
|a_t| \geq 0
\]

\textbf{Output:}
The output will consist of:
\begin{itemize}
    \item A list of positions: $x = [x_i \text{ for } i = 0, \ldots, T]$
    \item A list of velocities: $v = [v_i \text{ for } i = 0, \ldots, T]$
    \item A list of accelerations: $a = [a_i \text{ for } i = 0, \ldots, T]$
    \item Total fuel spent: $\text{fuel\_spend} = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"InitialPosition": 0, "InitialVelocity": 0, "FinalPosition": 1, "FinalVelocity": 0, "TotalTime": 20}')
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create the LP problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Define the decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=0)          #### Acceleration (non-negative)

#### Initial Conditions
problem += x[0] == x_0
problem += v[0] == v_0

#### Final Conditions
problem += x[T] == x_T
problem += v[T] == v_T

#### Objective Function: Minimize total fuel consumption (acceleration)
problem += pulp.lpSum(a[t] for t in range(T))

#### Motion Constraints
for t in range(T):
    problem += x[t + 1] - x[t] == v[t]  #### Position
    problem += v[t + 1] - v[t] == a[t]  #### Velocity

#### Solve the problem
problem.solve()

#### Retrieve the results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

