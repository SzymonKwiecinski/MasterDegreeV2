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

Let:
\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
    \item \( x_0 \): initial position of the rocket
    \item \( v_0 \): initial velocity of the rocket
    \item \( x_T \): target position of the rocket
    \item \( v_T \): target velocity of the rocket
    \item \( T \): final time
\end{itemize}

The dynamic equations of motion over discrete time increments can be expressed as:
\[
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t
\end{align*}
\]

The goal is to minimize the maximum thrust required, which is represented as:
\[
\text{Objective:} \quad \min \max_{t} |a_t|
\]

Subject to the initial conditions:
\[
\begin{align*}
x_0 & = x_0 \\
v_0 & = v_0 \\
\end{align*}
\]

And the boundary conditions at time \( T \):
\[
\begin{align*}
x_T & = x_T \\
v_T & = v_T \\
\end{align*}
\]

The fuel consumption is proportional to the absolute value of the acceleration:
\[
\text{Fuel spent:} \quad \text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( a_t \): acceleration at time \( t \) for \( t = 0, 1, \ldots, T-1 \)
    \item \( x_t \): position at time \( t \) for \( t = 0, 1, \ldots, T \)
    \item \( v_t \): velocity at time \( t \) for \( t = 0, 1, \ldots, T \)
\end{itemize}

Finally, the output format for the solution will be:
\[
\{
    \text{"x"}: [x_i \text{ for } i = 0, 1, \ldots, T],
    \text{"v"}: [v_i \text{ for } i = 0, 1, \ldots, T],
    \text{"a"}: [a_i \text{ for } i = 0, 1, \ldots, T],
    \text{"fuel\_spend"}: \text{fuel\_spent}
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

\section*{Mathematical Model for Rocket Trajectory Optimization}

Let:
\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
    \item \( x_0 \): initial position of the rocket
    \item \( v_0 \): initial velocity of the rocket
    \item \( x_T \): target position of the rocket
    \item \( v_T \): target velocity of the rocket
    \item \( T \): final time
\end{itemize}

The dynamic equations of motion over discrete time increments can be expressed as:
\[
\begin{align*}
x_{t+1} & = x_t + v_t \\
v_{t+1} & = v_t + a_t
\end{align*}
\]

The goal is to minimize the maximum thrust required, which is represented as:
\[
\text{Objective:} \quad \min \max_{t} |a_t|
\]

Subject to the initial conditions:
\[
\begin{align*}
x_0 & = x_0 \\
v_0 & = v_0 \\
\end{align*}
\]

And the boundary conditions at time \( T \):
\[
\begin{align*}
x_T & = x_T \\
v_T & = v_T \\
\end{align*}
\]

The fuel consumption is proportional to the absolute value of the acceleration:
\[
\text{Fuel spent:} \quad \text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( a_t \): acceleration at time \( t \) for \( t = 0, 1, \ldots, T-1 \)
    \item \( x_t \): position at time \( t \) for \( t = 0, 1, \ldots, T \)
    \item \( v_t \): velocity at time \( t \) for \( t = 0, 1, \ldots, T \)
\end{itemize}

Finally, the output format for the solution will be:
\[
\{
    \text{"x"}: [x_i \text{ for } i = 0, 1, \ldots, T],
    \text{"v"}: [v_i \text{ for } i = 0, 1, \ldots, T],
    \text{"a"}: [a_i \text{ for } i = 0, 1, \ldots, T],
    \text{"fuel\_spend"}: \text{fuel\_spent}
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity

#### Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

#### Dynamic equations of motion
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}")

#### Boundary conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

#### Objective: Minimize the maximum thrust (max |a_t|)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
for t in range(T):
    problem += (max_thrust >= a[t], f"MaxThrustConstraint_{t}")
    problem += (max_thrust >= -a[t], f"MaxThrustNegativeConstraint_{t}")

problem += pulp.lpSum([abs(a[t]) for t in range(T)])  #### Fuel consumption

#### Solve the problem
problem.solve()

#### Extract results
x_result = [x[i].varValue for i in range(T + 1)]
v_result = [v[i].varValue for i in range(T + 1)]
a_result = [a[i].varValue for i in range(T)]

#### Calculate fuel spent
fuel_spent = sum(abs(a[i].varValue) for i in range(T))

#### Output the results
output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spent
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

