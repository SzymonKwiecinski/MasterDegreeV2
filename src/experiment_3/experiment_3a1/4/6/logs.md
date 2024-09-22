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

\section*{Mathematical Model for Rocket Motion}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is given by the equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

The acceleration \( a_t \) is determined by the thrust of the rocket and is under our control. We aim to minimize the total fuel used, which is proportional to the magnitudes of acceleration:

\[
\text{Objective:} \quad \min \sum_{t=0}^{T-1} |a_t|
\]

Subject to the following constraints:

- Initial conditions:
  \[
  x_0 \quad \text{(initial position)}
  \]
  \[
  v_0 \quad \text{(initial velocity)}
  \]

- Final conditions to reach the target:
  \[
  x_T \quad \text{(target position)}
  \]
  \[
  v_T \quad \text{(target velocity)}
  \]

- Time constraint:
  \[
  t = 0, 1, \ldots, T-1
  \]

Thus our problem can be summarized as follows:

\begin{align*}
\text{Minimize:} & \quad \sum_{t=0}^{T-1} |a_t| \\
\text{Subject to:} & \\
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
& x_0 \text{ given}, \quad v_0 \text{ given} \\
& x_T \text{ desired}, \quad v_T \text{ desired}
\end{align*}

The output of the model will provide:
\begin{itemize}
    \item A list of positions \( [x_i \text{ for } i = 0, \ldots, T] \)
    \item A list of velocities \( [v_i \text{ for } i = 0, \ldots, T] \)
    \item A list of accelerations \( [a_i \text{ for } i = 0, \ldots, T] \)
    \item Total fuel spent \( \text{fuel\_spent} \)
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

\section*{Mathematical Model for Rocket Motion}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is given by the equations:

\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

The acceleration \( a_t \) is determined by the thrust of the rocket and is under our control. We aim to minimize the total fuel used, which is proportional to the magnitudes of acceleration:

\[
\text{Objective:} \quad \min \sum_{t=0}^{T-1} |a_t|
\]

Subject to the following constraints:

- Initial conditions:
  \[
  x_0 \quad \text{(initial position)}
  \]
  \[
  v_0 \quad \text{(initial velocity)}
  \]

- Final conditions to reach the target:
  \[
  x_T \quad \text{(target position)}
  \]
  \[
  v_T \quad \text{(target velocity)}
  \]

- Time constraint:
  \[
  t = 0, 1, \ldots, T-1
  \]

Thus our problem can be summarized as follows:

\begin{align*}
\text{Minimize:} & \quad \sum_{t=0}^{T-1} |a_t| \\
\text{Subject to:} & \\
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1 \\
& x_0 \text{ given}, \quad v_0 \text{ given} \\
& x_T \text{ desired}, \quad v_T \text{ desired}
\end{align*}

The output of the model will provide:
\begin{itemize}
    \item A list of positions \( [x_i \text{ for } i = 0, \ldots, T] \)
    \item A list of velocities \( [v_i \text{ for } i = 0, \ldots, T] \)
    \item A list of accelerations \( [a_i \text{ for } i = 0, \ldots, T] \)
    \item Total fuel spent \( \text{fuel\_spent} \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data 
data = {'InitialPosition': 0, 
        'InitialVelocity': 0, 
        'FinalPosition': 1, 
        'FinalVelocity': 0, 
        'TotalTime': 20}

#### Extract data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create the problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### Acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### Velocity

#### Objective function: Minimize fuel used (sum of absolute accelerations)
problem += pulp.lpSum([pulp.lpSum([a[t] for t in range(T)])]), "TotalFuel"

#### Initial conditions
problem += x[0] == x0, "InitialPosition"
problem += v[0] == v0, "InitialVelocity"

#### Dynamic equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionConstraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityConstraint_{t}"

#### Final conditions
problem += x[T] == xT, "FinalPosition"
problem += v[T] == vT, "FinalVelocity"

#### Solve the problem
problem.solve()

#### Collect results
positions = [x[i].varValue for i in range(T + 1)]
velocities = [v[i].varValue for i in range(T + 1)]
accelerations = [a[i].varValue for i in range(T)]

#### Total fuel spent
fuel_spent = pulp.value(problem.objective)

#### Printing Output
print(f'Positions: {positions}')
print(f'Velocities: {velocities}')
print(f'Accelarations: {accelerations}')
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')
```

