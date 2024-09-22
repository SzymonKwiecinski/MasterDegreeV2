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
To solve the given problem, we can formulate it as a Linear Programming (LP) problem. We want to minimize the total fuel consumption, which is proportional to the sum of absolute values of the acceleration at each time step. Below is the mathematical model and the corresponding LaTeX code for the LP formulation:

######### Decision Variables:
- \( x_t \): Position of the rocket at time \( t \).
- \( v_t \): Velocity of the rocket at time \( t \).
- \( a_t \): Acceleration of the rocket at time \( t \).
- \( u_t \): Auxiliary variable to handle the absolute value of \( a_t \), where \( u_t \geq |a_t| \).

######### Objective Function:
Minimize the total fuel consumption:
\[ \text{minimize} \quad \sum_{t=0}^{T-1} u_t \]

######### Constraints:
1. Initial conditions:
   \[
   x_0 = \text{given initial position}
   \]
   \[
   v_0 = \text{given initial velocity}
   \]

2. Dynamics equations for \( t = 0, \ldots, T-1 \):
   \[
   x_{t+1} = x_t + v_t
   \]
   \[
   v_{t+1} = v_t + a_t
   \]

3. Final conditions:
   \[
   x_T = \text{given target position}
   \]
   \[
   v_T = \text{given target velocity}
   \]

4. Absolute value constraints:
   \[
   u_t \geq a_t, \quad u_t \geq -a_t
   \]

The following is the LaTeX representation of the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Control}

\subsection*{Objective:}

Minimize the total fuel consumption:
\[
\min \quad \sum_{t=0}^{T-1} u_t
\]

\subsection*{Subject to:}

\begin{align*}
& \text{Initial conditions:} \\
& x_0 = x_0 \quad \text{(given initial position)} \\
& v_0 = v_0 \quad \text{(given initial velocity)} \\

& \text{Dynamics equations for } t = 0, \ldots, T-1: \\
& x_{t+1} = x_t + v_t \\
& v_{t+1} = v_t + a_t \\

& \text{Final conditions:} \\
& x_T = x_T \quad \text{(given target position)} \\
& v_T = v_T \quad \text{(given target velocity)} \\

& \text{Absolute value constraints:} \\
& u_t \geq a_t, \quad u_t \geq -a_t \quad \text{for } t = 0, \ldots, T-1.
\end{align*}

\end{document}
```

This LP model can be solved using any standard linear programming solver to find the optimal sequences of positions, velocities, accelerations, and the total fuel consumption over the given time period.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Control}

\subsection*{Objective:}

Minimize the total fuel consumption:
\[
\min \quad \sum_{t=0}^{T-1} u_t
\]

\subsection*{Subject to:}

\begin{align*}
& \text{Initial conditions:} \\
& x_0 = x_0 \quad \text{(given initial position)} \\
& v_0 = v_0 \quad \text{(given initial velocity)} \\

& \text{Dynamics equations for } t = 0, \ldots, T-1: \\
& x_{t+1} = x_t + v_t \\
& v_{t+1} = v_t + a_t \\

& \text{Final conditions:} \\
& x_T = x_T \quad \text{(given target position)} \\
& v_T = v_T \quad \text{(given target velocity)} \\

& \text{Absolute value constraints:} \\
& u_t \geq a_t, \quad u_t \geq -a_t \quad \text{for } t = 0, \ldots, T-1.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

#### Problem setup
problem = pulp.LpProblem("Rocket_Control", pulp.LpMinimize)

#### Decision variables
T = data['TotalTime']
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
u = [pulp.LpVariable(f"u_{t}", lowBound=0, cat='Continuous') for t in range(T)]

#### Objective function
problem += pulp.lpSum(u)

#### Constraints
problem += (x[0] == data['InitialPosition'], "Initial_Position")
problem += (v[0] == data['InitialVelocity'], "Initial_Velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Dynamics_Position_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Dynamics_Velocity_{t}")
    problem += (u[t] >= a[t], f"Abs_Constraint_Pos_{t}")
    problem += (u[t] >= -a[t], f"Abs_Constraint_Neg_{t}")

problem += (x[T] == data['FinalPosition'], "Final_Position")
problem += (v[T] == data['FinalVelocity'], "Final_Velocity")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

