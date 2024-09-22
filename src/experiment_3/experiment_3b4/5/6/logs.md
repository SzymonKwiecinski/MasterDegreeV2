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
To model the given problem as a linear programming problem, we need to formulate the objective function and the constraints. Here, we'll present this in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Optimization}

\subsection*{Objective:}
Minimize the total fuel spent, which is the sum of the absolute values of the accelerations over the time period from $t = 0$ to $t = T-1$.

\[
\text{Minimize } \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Subject to:}
1. Dynamics of the rocket:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = x_0 \quad \text{(given)}
   \]
   \[
   v_0 = v_0 \quad \text{(given)}
   \]

3. Final conditions:
   \[
   x_T = x_T \quad \text{(target position)}
   \]
   \[
   v_T = v_T \quad \text{(target velocity)}
   \]

\subsection*{Variables:}
\[
x_t, v_t, a_t \text{ for } t = 0, 1, \ldots, T
\]

\end{document}
```

The given model describes the motion of a rocket, including its position and velocity dynamics over discrete time steps. The decision variables of this problem are the accelerations at each time step, which are controlled to minimize fuel usage while ensuring the rocket reaches the target position and velocity at the final time step. The problem also accounts for absolute acceleration, a proxy for fuel consumption, which is minimized across all time steps.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Path Optimization}

\subsection*{Objective:}
Minimize the total fuel spent, which is the sum of the absolute values of the accelerations over the time period from $t = 0$ to $t = T-1$.

\[
\text{Minimize } \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Subject to:}
1. Dynamics of the rocket:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = x_0 \quad \text{(given)}
   \]
   \[
   v_0 = v_0 \quad \text{(given)}
   \]

3. Final conditions:
   \[
   x_T = x_T \quad \text{(target position)}
   \]
   \[
   v_T = v_T \quad \text{(target velocity)}
   \]

\subsection*{Variables:}
\[
x_t, v_t, a_t \text{ for } t = 0, 1, \ldots, T
\]

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

#### Model setup
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

#### Parameters
T = data['TotalTime']

#### Variables
x = pulp.LpVariable.dicts('x', range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts('v', range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts('a', range(T), cat='Continuous')
abs_a = pulp.LpVariable.dicts('abs_a', range(T), lowBound=0, cat='Continuous')

#### Objective: Minimize the total fuel spent (sum of absolute accelerations)
problem += pulp.lpSum(abs_a[t] for t in range(T))

#### Constraints

#### Dynamics of the rocket
for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"Dynamics_position_{t}"
    problem += v[t+1] == v[t] + a[t], f"Dynamics_velocity_{t}"

#### Initial conditions
problem += x[0] == data['InitialPosition'], "Initial_position"
problem += v[0] == data['InitialVelocity'], "Initial_velocity"

#### Final conditions
problem += x[T] == data['FinalPosition'], "Final_position"
problem += v[T] == data['FinalVelocity'], "Final_velocity"

#### Absolute value constraints for acceleration
for t in range(T):
    problem += abs_a[t] >= a[t], f"Abs_acceleration_pos_{t}"
    problem += abs_a[t] >= -a[t], f"Abs_acceleration_neg_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
objective_value = pulp.value(problem.objective)
print(f'<OBJ>{objective_value}</OBJ>')
```

