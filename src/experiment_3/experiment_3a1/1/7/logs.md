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
\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \).
\end{itemize}

\textbf{Discrete-Time Model:}
\begin{align*}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align*}

\textbf{Initial Conditions:}
\begin{align*}
    x_0 &= x_0 \\
    v_0 &= v_0
\end{align*}

\textbf{Target Conditions:}
\begin{align*}
    x_T &= x_T \\
    v_T &= v_T \\
    T &= T
\end{align*}

\textbf{Objective Function:}
\[
\text{Minimize } \max_{t} |a_t|
\]

\textbf{Fuel Consumption:}
\[
\text{Fuel consumption is proportional to the acceleration: } |a_t| \text{ at time } t
\]

\textbf{Output:}
\begin{itemize}
    \item \( x \) contains positions at each time step from \( 0 \) to \( T \).
    \item \( v \) contains velocities at each time step from \( 0 \) to \( T \).
    \item \( a \) contains accelerations at each time step from \( 0 \) to \( T \).
    \item \( \text{fuel\_spend} \) contains the total fuel spent by the rocket.
\end{itemize}

\textbf{Output Format:}
\[
\{ 
    "x": [x_i \text{ for } i = 1, \ldots, T], \\
    "v": [v_i \text{ for } i = 1, \ldots, T], \\
    "a": [a_i \text{ for } i = 1, \ldots, T], \\
    "fuel\_spend": \text{fuel\_spent}
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

\section*{Rocket Motion Optimization Problem}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_t \) be the position of the rocket at time \( t \).
    \item Let \( v_t \) be the velocity of the rocket at time \( t \).
    \item Let \( a_t \) be the acceleration of the rocket at time \( t \).
\end{itemize}

\textbf{Discrete-Time Model:}
\begin{align*}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align*}

\textbf{Initial Conditions:}
\begin{align*}
    x_0 &= x_0 \\
    v_0 &= v_0
\end{align*}

\textbf{Target Conditions:}
\begin{align*}
    x_T &= x_T \\
    v_T &= v_T \\
    T &= T
\end{align*}

\textbf{Objective Function:}
\[
\text{Minimize } \max_{t} |a_t|
\]

\textbf{Fuel Consumption:}
\[
\text{Fuel consumption is proportional to the acceleration: } |a_t| \text{ at time } t
\]

\textbf{Output:}
\begin{itemize}
    \item \( x \) contains positions at each time step from \( 0 \) to \( T \).
    \item \( v \) contains velocities at each time step from \( 0 \) to \( T \).
    \item \( a \) contains accelerations at each time step from \( 0 \) to \( T \).
    \item \( \text{fuel\_spend} \) contains the total fuel spent by the rocket.
\end{itemize}

\textbf{Output Format:}
\[
\{ 
    "x": [x_i \text{ for } i = 1, \ldots, T], \\
    "v": [v_i \text{ for } i = 1, \ldots, T], \\
    "a": [a_i \text{ for } i = 1, \ldots, T], \\
    "fuel\_spend": \text{fuel\_spent}
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Define the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Variables
T = data['T']
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=None)  #### acceleration

#### Initial conditions
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

#### Target conditions
problem += (x[T] == data['XT'], "Target_Position")
problem += (v[T] == data['VT'], "Target_Velocity")

#### Discrete-time model constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

#### Objective function: Minimize max acceleration
max_acceleration = pulp.LpVariable("max_a", lowBound=0)
for t in range(T + 1):
    problem += (a[t] <= max_acceleration, f"Max_Acceleration_Constraint_{t}")
    problem += (a[t] >= -max_acceleration, f"Min_Acceleration_Constraint_{t}")

problem += max_acceleration, "Minimize_Max_Acceleration"

#### Solve the problem
problem.solve()

#### Collect the output
output = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T + 1)],
    "fuel_spend": sum(abs(a[t].varValue) for t in range(T + 1))
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

