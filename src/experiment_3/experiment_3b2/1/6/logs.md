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
To model this problem as a linear programming (LP) problem, we seek to minimize the absolute value of acceleration at each time step, which represents the fuel consumed. The LP formulation is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total fuel consumption:

\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to:}

1. Discretized motion equations:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = \text{given}
   \]
   \[
   v_0 = \text{given}
   \]

3. Target conditions:
   \[
   x_T = \text{given}
   \]
   \[
   v_T = \text{given}
   \]

4. Absolute value of acceleration:
   To handle the absolute value, introduce auxiliary variables \( u_t \) such that:
   \[
   -u_t \leq a_t \leq u_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   which ensures \( |a_t| \leq u_t \).

5. Rewrite the objective function using auxiliary variables:
   \[
   \min \sum_{t=0}^{T-1} u_t
   \]

\textbf{Decision Variables:} 
- \( x_t \) for position at each time step \( t \),
- \( v_t \) for velocity at each time step \( t \),
- \( a_t \) for acceleration at each time step \( t \),
- \( u_t \) for auxiliary variables representing \( |a_t| \).

\end{document}
```

This LP formulation allows us to compute the optimal trajectory, velocities, accelerations, and fuel spent over the time horizon by solving the linear program. The constraints ensure the motion follows the physical laws, initial and terminal conditions match the requirements, and the objective function is structured to minimize the total fuel consumption.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total fuel consumption:

\[
\min \sum_{t=0}^{T-1} |a_t|
\]

\textbf{Subject to:}

1. Discretized motion equations:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = \text{given}
   \]
   \[
   v_0 = \text{given}
   \]

3. Target conditions:
   \[
   x_T = \text{given}
   \]
   \[
   v_T = \text{given}
   \]

4. Absolute value of acceleration:
   To handle the absolute value, introduce auxiliary variables \( u_t \) such that:
   \[
   -u_t \leq a_t \leq u_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   which ensures \( |a_t| \leq u_t \).

5. Rewrite the objective function using auxiliary variables:
   \[
   \min \sum_{t=0}^{T-1} u_t
   \]

\textbf{Decision Variables:} 
- \( x_t \) for position at each time step \( t \),
- \( v_t \) for velocity at each time step \( t \),
- \( a_t \) for acceleration at each time step \( t \),
- \( u_t \) for auxiliary variables representing \( |a_t| \).

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

#### Create a linear programming problem
problem = pulp.LpProblem("MinimizeFuelConsumption", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]
u = [pulp.LpVariable(f'u_{t}', lowBound=0) for t in range(T)]

#### Objective function
problem += pulp.lpSum(u[t] for t in range(T)), "TotalFuelConsumption"

#### Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

#### Target conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

#### Motion equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"MotionEquation_x_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"MotionEquation_v_{t}")
    
    #### Absolute value constraints
    problem += (-u[t] <= a[t], f"AbsValueLower_{t}")
    problem += (a[t] <= u[t], f"AbsValueUpper_{t}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

