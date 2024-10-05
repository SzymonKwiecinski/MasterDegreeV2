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
To solve this problem, we need to formulate a linear programming model that minimizes the total fuel consumption subject to the constraints of the rocket's motion. We will define the decision variables, objective function, and constraints based on the problem's requirements.

Let's define the decision variables:
- \( x_t \) for the position of the rocket at each time step \( t \).
- \( v_t \) for the velocity of the rocket at each time step \( t \).
- \( a_t \) for the acceleration (and thus control input) of the rocket at each time step \( t \).

Given these, the linear programming model in LaTeX format will be as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\textbf{Objective:} Minimize the total fuel consumption,
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to the constraints:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \text{for } t = 0, 1, \ldots, T-1, \\
v_{t+1} &= v_t + a_t, \quad \text{for } t = 0, 1, \ldots, T-1, \\
x_0 &= \text{given initial position}, \\
v_0 &= \text{given initial velocity}, \\
x_T &= \text{target position at time } T, \\
v_T &= \text{target velocity at time } T.
\end{align*}

\textbf{Decision variables:}
- \( x_t \) for \( t = 0, 1, \ldots, T \)
- \( v_t \) for \( t = 0, 1, \ldots, T \)
- \( a_t \) for \( t = 0, 1, \ldots, T-1 \)

\textbf{Remarks:}
- \( |a_t| \) represents the absolute value of acceleration, relevant for fuel consumption.
- The absolute value can be handled in linear programming by introducing additional variables and constraints, e.g., \( a_t = a_t^+ - a_t^- \) with \( a_t^+, a_t^- \geq 0 \) and minimizing \( a_t^+ + a_t^- \).

\end{document}
```

In this linear program, the absolute value of acceleration \( |a_t| \) is managed using auxiliary variables to ensure linear constraints. This model captures all the necessary dynamics and constraints of the rocket's motion in discrete-time, meeting the problem's requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\textbf{Objective:} Minimize the total fuel consumption,
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to the constraints:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad \text{for } t = 0, 1, \ldots, T-1, \\
v_{t+1} &= v_t + a_t, \quad \text{for } t = 0, 1, \ldots, T-1, \\
x_0 &= \text{given initial position}, \\
v_0 &= \text{given initial velocity}, \\
x_T &= \text{target position at time } T, \\
v_T &= \text{target velocity at time } T.
\end{align*}

\textbf{Decision variables:}
- \( x_t \) for \( t = 0, 1, \ldots, T \)
- \( v_t \) for \( t = 0, 1, \ldots, T \)
- \( a_t \) for \( t = 0, 1, \ldots, T-1 \)

\textbf{Remarks:}
- \( |a_t| \) represents the absolute value of acceleration, relevant for fuel consumption.
- The absolute value can be handled in linear programming by introducing additional variables and constraints, e.g., \( a_t = a_t^+ - a_t^- \) with \( a_t^+, a_t^- \geq 0 \) and minimizing \( a_t^+ + a_t^- \).

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Extracting parameters
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Initialize the problem
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  #### position variables
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  #### velocity variables
a_plus = pulp.LpVariable.dicts("a_plus", range(T), lowBound=0)  #### acceleration positive part
a_minus = pulp.LpVariable.dicts("a_minus", range(T), lowBound=0)  #### acceleration negative part

#### Objective Function
problem += pulp.lpSum(a_plus[t] + a_minus[t] for t in range(T))  #### minimizing total fuel consumption

#### Constraints
problem += (x[0] == x0)  #### Initial position constraint
problem += (v[0] == v0)  #### Initial velocity constraint

#### Dynamics equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  #### Position update
    problem += (v[t + 1] == v[t] + a_plus[t] - a_minus[t])  #### Velocity update

#### Final conditions
problem += (x[T] == xT)  #### Final position constraint
problem += (v[T] == vT)  #### Final velocity constraint

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

