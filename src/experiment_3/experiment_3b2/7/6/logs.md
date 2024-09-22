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
To solve this problem, we will create a linear programming model using the given constraints and objective. We want to minimize the total fuel expenditure, which is proportional to the sum of absolute accelerations. We will use the variables \(x_t\), \(v_t\), and \(a_t\) to represent the position, velocity, and acceleration at time \(t\), respectively.

Here is the mathematical model written in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\subsection*{Decision Variables}
\begin{align*}
x_t & : \text{Position of the rocket at time } t, \quad t = 0, \ldots, T \\
v_t & : \text{Velocity of the rocket at time } t, \quad t = 0, \ldots, T \\
a_t & : \text{Acceleration of the rocket at time } t, \quad t = 0, \ldots, T-1 \\
u_t & : \text{Auxiliary variable for } |a_t|, \quad t = 0, \ldots, T-1 \\
\end{align*}

\subsection*{Objective Function}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Constraints}
\begin{align*}
& x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
& x_0 = \text{given initial position}, \\
& v_0 = \text{given initial velocity}, \\
& x_T = \text{desired final position}, \\
& v_T = \text{desired final velocity}, \\
& u_t \geq a_t, \quad t = 0, \ldots, T-1 \\
& u_t \geq -a_t, \quad t = 0, \ldots, T-1 \\
\end{align*}

\subsection*{Additional Remarks}
- The auxiliary variables \(u_t\) are introduced to linearize the absolute value of acceleration \(a_t\).
- The constraints ensure the dynamic behavior of the rocket and the achievement of terminal conditions.

\end{document}
```

This LaTeX code represents the linear programming formulation for optimizing the trajectory of a rocket given an initial position and velocity, with constraints to reach a target position and velocity, while minimizing fuel consumption. The auxiliary variable \(u_t\) is used for linearizing the absolute value of acceleration, enabling the problem to remain linear.

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

\subsection*{Decision Variables}
\begin{align*}
x_t & : \text{Position of the rocket at time } t, \quad t = 0, \ldots, T \\
v_t & : \text{Velocity of the rocket at time } t, \quad t = 0, \ldots, T \\
a_t & : \text{Acceleration of the rocket at time } t, \quad t = 0, \ldots, T-1 \\
u_t & : \text{Auxiliary variable for } |a_t|, \quad t = 0, \ldots, T-1 \\
\end{align*}

\subsection*{Objective Function}
Minimize the total fuel consumption:
\[
\min \sum_{t=0}^{T-1} u_t
\]

\subsection*{Constraints}
\begin{align*}
& x_{t+1} = x_t + v_t, \quad t = 0, \ldots, T-1 \\
& v_{t+1} = v_t + a_t, \quad t = 0, \ldots, T-1 \\
& x_0 = \text{given initial position}, \\
& v_0 = \text{given initial velocity}, \\
& x_T = \text{desired final position}, \\
& v_T = \text{desired final velocity}, \\
& u_t \geq a_t, \quad t = 0, \ldots, T-1 \\
& u_t \geq -a_t, \quad t = 0, \ldots, T-1 \\
\end{align*}

\subsection*{Additional Remarks}
- The auxiliary variables \(u_t\) are introduced to linearize the absolute value of acceleration \(a_t\).
- The constraints ensure the dynamic behavior of the rocket and the achievement of terminal conditions.

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Problem definition
problem = pulp.LpProblem("RocketTrajectoryOptimization", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
u = [pulp.LpVariable(f'u_{t}', lowBound=0) for t in range(T)]

#### Objective Function
problem += pulp.lpSum(u[t] for t in range(T))

#### Initial Conditions
problem += x[0] == x0
problem += v[0] == v0

#### Final Conditions
problem += x[T] == xT
problem += v[T] == vT

#### Dynamic Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += u[t] >= a[t]  #### Ensuring u_t >= a_t
    problem += u[t] >= -a[t] #### Ensuring u_t >= -a_t

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

