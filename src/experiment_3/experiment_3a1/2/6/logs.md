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

We define the following variables:
\begin{align*}
    x_t & : \text{position of the rocket at time } t, \\
    v_t & : \text{velocity of the rocket at time } t, \\
    a_t & : \text{acceleration of the rocket at time } t.
\end{align*}

The motion of the rocket is described by the following discrete-time equations:
\begin{align}
    x_{t+1} = x_t + v_t, \\
    v_{t+1} = v_t + a_t.
\end{align}

We want to control the acceleration \( a_t \) at each time step. We have the following initial conditions:
\begin{align*}
    x_0 & : \text{initial position}, \\
    v_0 & : \text{initial velocity}.
\end{align*}

The goal is to reach a target position \( x_T \) with a final velocity \( v_T \) at time \( T \):
\begin{align*}
    x_T & : \text{target position}, \\
    v_T & : \text{target velocity}.
\end{align*}

The optimization problem can be formulated as follows:

\textbf{Objective:}
Minimize the total fuel consumption (total acceleration) over the time period:
\begin{equation}
    \text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|.
\end{equation}

\textbf{Subject to:}
\begin{align}
    x_{t+1} = x_t + v_t, \quad & t = 0, 1, \ldots, T-1, \\
    v_{t+1} = v_t + a_t, \quad & t = 0, 1, \ldots, T-1, \\
    x_0 = & \text{given initial position}, \\
    v_0 = & \text{given initial velocity}, \\
    x_T = & \text{target position}, \\
    v_T = & \text{target velocity}.
\end{align}

The output should include:
\begin{align*}
    "x" & : \text{list of positions from } x_0 \text{ to } x_T, \\
    "v" & : \text{list of velocities from } v_0 \text{ to } v_T, \\
    "a" & : \text{list of accelerations over time,} \\
    "fuel\_spend" & : \text{total fuel spent}.
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

We define the following variables:
\begin{align*}
    x_t & : \text{position of the rocket at time } t, \\
    v_t & : \text{velocity of the rocket at time } t, \\
    a_t & : \text{acceleration of the rocket at time } t.
\end{align*}

The motion of the rocket is described by the following discrete-time equations:
\begin{align}
    x_{t+1} = x_t + v_t, \\
    v_{t+1} = v_t + a_t.
\end{align}

We want to control the acceleration \( a_t \) at each time step. We have the following initial conditions:
\begin{align*}
    x_0 & : \text{initial position}, \\
    v_0 & : \text{initial velocity}.
\end{align*}

The goal is to reach a target position \( x_T \) with a final velocity \( v_T \) at time \( T \):
\begin{align*}
    x_T & : \text{target position}, \\
    v_T & : \text{target velocity}.
\end{align*}

The optimization problem can be formulated as follows:

\textbf{Objective:}
Minimize the total fuel consumption (total acceleration) over the time period:
\begin{equation}
    \text{Minimize} \quad \sum_{t=0}^{T-1} |a_t|.
\end{equation}

\textbf{Subject to:}
\begin{align}
    x_{t+1} = x_t + v_t, \quad & t = 0, 1, \ldots, T-1, \\
    v_{t+1} = v_t + a_t, \quad & t = 0, 1, \ldots, T-1, \\
    x_0 = & \text{given initial position}, \\
    v_0 = & \text{given initial velocity}, \\
    x_T = & \text{target position}, \\
    v_T = & \text{target velocity}.
\end{align}

The output should include:
\begin{align*}
    "x" & : \text{list of positions from } x_0 \text{ to } x_T, \\
    "v" & : \text{list of velocities from } v_0 \text{ to } v_T, \\
    "a" & : \text{list of accelerations over time,} \\
    "fuel\_spend" & : \text{total fuel spent}.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data dictionary
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Extract data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create the LP problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Define variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### Acceleration
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  #### Velocity

#### Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

#### Objective function: minimize total fuel consumption (total acceleration)
problem += pulp.lpSum(pulp.abs(a[t]) for t in range(T)), "TotalFuelConsumption"

#### Constraints for motion
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"PositionConstraint_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"VelocityConstraint_{t}"

#### Final conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

#### Solve the problem
problem.solve()

#### Collect the results
positions = [pulp.value(x[t]) for t in range(T+1)]
velocities = [pulp.value(v[t]) for t in range(T+1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

#### Total fuel spent
total_fuel = pulp.value(problem.objective)

#### Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": total_fuel
}

print(f' (Objective Value): <OBJ>{total_fuel}</OBJ>')
```

