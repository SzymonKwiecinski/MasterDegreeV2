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

\section*{Mathematical Model for Rocket Trajectory}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined by the following equations:

\begin{align}
x_{t+1} &= x_t + v_t, \tag{1} \\
v_{t+1} &= v_t + a_t. \tag{2}
\end{align}

The acceleration \( a_t \) is under our control, which is influenced by the rocket thrust. The magnitude of the acceleration \( |a_t| \) can be related to fuel consumption.

Given the initial conditions:

\[
x_0 \quad \text{(initial position)}
\]
\[
v_0 \quad \text{(initial velocity)}
\]

We aim for the rocket to reach a target position \( x_T \) with speed \( v_T \) at time \( T \).

\subsection*{Objective Function}

Our objective is to minimize the maximum thrust required, expressed as:

\[
\min \max_{t = 0, \ldots, T} |a_t|. \tag{3}
\]

\subsection*{Constraints}

We need to satisfy the following constraints at time \( T \):

1. Position constraint:
\[
x_T = x_0 + \sum_{t=0}^{T-1} v_t \tag{4}
\]

2. Velocity constraint:
\[
v_T = v_0 + \sum_{t=0}^{T-1} a_t. \tag{5}
\]

3. Acceleration limits (if any):
\[
|a_t| \leq A \quad \text{for all } t, \tag{6}
\]
where \( A \) is the maximum allowable acceleration.

\subsection*{Decision Variables}

The decision variables for this problem are:
\[
\begin{align*}
a_t & \quad \text{(acceleration at time } t\text{)} \\
x_t & \quad \text{(position at time } t\text{)} \\
v_t & \quad \text{(velocity at time } t\text{)}
\end{align*}
\]

\subsection*{Output Format}

The output will consist of:

\begin{align*}
\text{"x"} & = [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & = [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & = [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & = \text{total fuel spent}
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

\section*{Mathematical Model for Rocket Trajectory}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined by the following equations:

\begin{align}
x_{t+1} &= x_t + v_t, \tag{1} \\
v_{t+1} &= v_t + a_t. \tag{2}
\end{align}

The acceleration \( a_t \) is under our control, which is influenced by the rocket thrust. The magnitude of the acceleration \( |a_t| \) can be related to fuel consumption.

Given the initial conditions:

\[
x_0 \quad \text{(initial position)}
\]
\[
v_0 \quad \text{(initial velocity)}
\]

We aim for the rocket to reach a target position \( x_T \) with speed \( v_T \) at time \( T \).

\subsection*{Objective Function}

Our objective is to minimize the maximum thrust required, expressed as:

\[
\min \max_{t = 0, \ldots, T} |a_t|. \tag{3}
\]

\subsection*{Constraints}

We need to satisfy the following constraints at time \( T \):

1. Position constraint:
\[
x_T = x_0 + \sum_{t=0}^{T-1} v_t \tag{4}
\]

2. Velocity constraint:
\[
v_T = v_0 + \sum_{t=0}^{T-1} a_t. \tag{5}
\]

3. Acceleration limits (if any):
\[
|a_t| \leq A \quad \text{for all } t, \tag{6}
\]
where \( A \) is the maximum allowable acceleration.

\subsection*{Decision Variables}

The decision variables for this problem are:
\[
\begin{align*}
a_t & \quad \text{(acceleration at time } t\text{)} \\
x_t & \quad \text{(position at time } t\text{)} \\
v_t & \quad \text{(velocity at time } t\text{)}
\end{align*}
\]

\subsection*{Output Format}

The output will consist of:

\begin{align*}
\text{"x"} & = [x_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"v"} & = [v_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"a"} & = [a_i \text{ for } i = 0, 1, \ldots, T] \\
\text{"fuel\_spend"} & = \text{total fuel spent}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0, V0, XT, VT, T = data['X0'], data['V0'], data['XT'], data['VT'], data['T']

#### Create a Linear Programming Problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable.dicts("a", (range(T)), lowBound=None, upBound=None, cat='Continuous')
x = pulp.LpVariable.dicts("x", (range(T + 1)), lowBound=None, upBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", (range(T + 1)), lowBound=None, upBound=None, cat='Continuous')

#### Auxiliary Variable for Objective Function
max_abs_a = pulp.LpVariable("max_abs_a", lowBound=0, cat='Continuous')

#### Objective Function: Minimize the maximum acceleration magnitude
problem += max_abs_a, "Minimize_Max_Acceleration"

#### Constraints

#### Initial conditions
problem += x[0] == X0, "Initial_Position"
problem += v[0] == V0, "Initial_Velocity"

#### Dynamical model
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Equation_at_t_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Equation_at_t_{t}"

    #### Maximum acceleration constraint
    problem += a[t] <= max_abs_a, f"Max_Acceleration_Positive_at_t_{t}"
    problem += -a[t] <= max_abs_a, f"Max_Acceleration_Negative_at_t_{t}"

#### Terminal conditions
problem += x[T] == XT, "Final_Position"
problem += v[T] == VT, "Final_Velocity"

#### Solve the problem
problem.solve()

#### Extracting the results
x_values = [x[t].varValue for t in range(T + 1)]
v_values = [v[t].varValue for t in range(T + 1)]
a_values = [a[t].varValue for t in range(T)]

#### Assuming fuel spend is the sum of absolute accelerations
fuel_spend = sum(abs(at) for at in a_values)

#### Output
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spend
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

