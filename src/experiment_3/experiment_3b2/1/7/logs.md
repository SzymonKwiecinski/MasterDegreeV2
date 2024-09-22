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

\subsection*{Given Data and Problem Description}

We consider a rocket traveling along a straight path with the following parameters:
- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Time horizon: \( T \)

The state of the rocket at time \( t \) is represented by:
- Position: \( x_t \)
- Velocity: \( v_t \)
- Acceleration: \( a_t \)

The relationships between these variables over discrete time increments are given by:
\begin{align*}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align*}

The acceleration \( a_t \) is controlled by the rocket's thrust, and we aim to minimize the maximum thrust required over the course of the flight, denoted as \( \max_t |a_t| \).

\subsection*{Objective}

Minimize the maximum thrust:

\[
\min \max_t |a_t|, \quad t = 0, 1, \ldots, T-1
\]

\subsection*{Constraints}

The constraints for the rocket's trajectory are:
1. Initial and target conditions for position and velocity:
   \begin{align*}
       x_0 &= \text{given} \\
       v_0 &= \text{given} \\
       x_T &= \text{given target position} \\
       v_T &= \text{given target velocity}
   \end{align*}

2. Dynamics of the motion for \( t = 0, 1, \ldots, T-1 \):
   \begin{align*}
       x_{t+1} &= x_t + v_t \\
       v_{t+1} &= v_t + a_t
   \end{align*}

3. Fuel consumption is proportional to the absolute value of acceleration \( |a_t| \).

\subsection*{Decision Variables}

- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)
- \( |a_t| \leq M \) with \( M = \max_t |a_t| \)

\subsection*{Output Information}

The solution to the problem will provide:
- A list of the positions \( x_t \) for \( t = 1, \ldots, T \)
- A list of the velocities \( v_t \) for \( t = 1, \ldots, T \)
- A list of the accelerations \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
- The total fuel spent, computed as:
  \[
  \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
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

\subsection*{Given Data and Problem Description}

We consider a rocket traveling along a straight path with the following parameters:
- Initial position: \( x_0 \)
- Initial velocity: \( v_0 \)
- Target position: \( x_T \)
- Target velocity: \( v_T \)
- Time horizon: \( T \)

The state of the rocket at time \( t \) is represented by:
- Position: \( x_t \)
- Velocity: \( v_t \)
- Acceleration: \( a_t \)

The relationships between these variables over discrete time increments are given by:
\begin{align*}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align*}

The acceleration \( a_t \) is controlled by the rocket's thrust, and we aim to minimize the maximum thrust required over the course of the flight, denoted as \( \max_t |a_t| \).

\subsection*{Objective}

Minimize the maximum thrust:

\[
\min \max_t |a_t|, \quad t = 0, 1, \ldots, T-1
\]

\subsection*{Constraints}

The constraints for the rocket's trajectory are:
1. Initial and target conditions for position and velocity:
   \begin{align*}
       x_0 &= \text{given} \\
       v_0 &= \text{given} \\
       x_T &= \text{given target position} \\
       v_T &= \text{given target velocity}
   \end{align*}

2. Dynamics of the motion for \( t = 0, 1, \ldots, T-1 \):
   \begin{align*}
       x_{t+1} &= x_t + v_t \\
       v_{t+1} &= v_t + a_t
   \end{align*}

3. Fuel consumption is proportional to the absolute value of acceleration \( |a_t| \).

\subsection*{Decision Variables}

- \( x_t \): Position of the rocket at time \( t \)
- \( v_t \): Velocity of the rocket at time \( t \)
- \( a_t \): Acceleration of the rocket at time \( t \)
- \( |a_t| \leq M \) with \( M = \max_t |a_t| \)

\subsection*{Output Information}

The solution to the problem will provide:
- A list of the positions \( x_t \) for \( t = 1, \ldots, T \)
- A list of the velocities \( v_t \) for \( t = 1, \ldots, T \)
- A list of the accelerations \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
- The total fuel spent, computed as:
  \[
  \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
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
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create the linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       #### Acceleration
M = pulp.LpVariable("M", lowBound=0)                          #### Maximum thrust

#### Objective function
problem += M

#### Initial conditions
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")

#### Target conditions
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

#### Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

    #### Constraints on acceleration
    problem += (a[t] <= M, f"Max_Thrust_Upper_{t}")
    problem += (a[t] >= -M, f"Max_Thrust_Lower_{t}")

#### Objective Value Print
problem.solve()

#### Output information
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]

total_fuel_spend = sum(abs(a[t].varValue) for t in range(T))

#### Print output
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelerations: {accelerations}')
print(f'Total Fuel Spend: {total_fuel_spend}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

