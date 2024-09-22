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

\section*{Rocket Movement Optimization Problem}

We define the following variables:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time model can be described as follows:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

The objective of our problem is to minimize the total fuel consumption, which is expressed as:
\[
\text{Minimize } Z = \sum_{t=0}^{T-1} |a_t|
\]

Subject to the constraints:
\begin{align*}
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
T &= \text{total time}
\end{align*}

The output of the optimization problem is structured as follows:

\begin{itemize}
    \item \( x \): List of positions of the rocket at each time step from \( 0 \) to \( T \)
    \item \( v \): List of velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item \( a \): List of accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item \text{fuel\_spend}: Total fuel spent by the rocket
\end{itemize}

The expected output format is:
\[
\{
    "x": [x_i \text{ for } i \text{ in } 1, ..., T],
    "v": [v_i \text{ for } i \text{ in } 1, ..., T],
    "a": [a_i \text{ for } i \text{ in } 1, ..., T],
    "fuel\_spend": \text{fuel\_spent},
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

\section*{Rocket Movement Optimization Problem}

We define the following variables:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time model can be described as follows:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

The objective of our problem is to minimize the total fuel consumption, which is expressed as:
\[
\text{Minimize } Z = \sum_{t=0}^{T-1} |a_t|
\]

Subject to the constraints:
\begin{align*}
x_0 &= \text{initial position} \\
v_0 &= \text{initial velocity} \\
x_T &= \text{target position} \\
v_T &= \text{target velocity} \\
T &= \text{total time}
\end{align*}

The output of the optimization problem is structured as follows:

\begin{itemize}
    \item \( x \): List of positions of the rocket at each time step from \( 0 \) to \( T \)
    \item \( v \): List of velocities of the rocket at each time step from \( 0 \) to \( T \)
    \item \( a \): List of accelerations of the rocket at each time step from \( 0 \) to \( T \)
    \item \text{fuel\_spend}: Total fuel spent by the rocket
\end{itemize}

The expected output format is:
\[
\{
    "x": [x_i \text{ for } i \text{ in } 1, ..., T],
    "v": [v_i \text{ for } i \text{ in } 1, ..., T],
    "a": [a_i \text{ for } i \text{ in } 1, ..., T],
    "fuel\_spend": \text{fuel\_spent},
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create a Linear Programming Problem
problem = pulp.LpProblem("Rocket_Movement_Optimization", pulp.LpMinimize)

#### Define decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

#### Define absolute acceleration variables
abs_a = [pulp.LpVariable(f"abs_a_{t}", lowBound=0, cat='Continuous') for t in range(T)]

#### Objective function: Minimize total fuel consumption
problem += pulp.lpSum(abs_a)

#### Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

#### Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

#### Motion equations and absolute value constraints
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]
    problem += abs_a[t] >= a[t]
    problem += abs_a[t] >= -a[t]

#### Solve the problem
problem.solve()

#### Collect the results
result = {
    "x": [pulp.value(x[t]) for t in range(T + 1)],
    "v": [pulp.value(v[t]) for t in range(T + 1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective),
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

