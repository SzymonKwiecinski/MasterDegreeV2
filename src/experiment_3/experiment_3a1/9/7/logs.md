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

\section*{Rocket Motion Linear Programming Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We assume that the acceleration \( a_t \) is controlled by the rocket thrust, and its magnitude \( |a_t| \) is proportional to the rate of fuel consumption at time \( t \). Given the initial conditions:

\[
x_0, \quad v_0
\]

we aim to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). Our objective is to minimize the maximum thrust required:

\[
\text{Objective:} \quad \min \max_{t} |a_t|
\]

The constraints for the problem can be formulated as follows:

1. State update equations for position and velocity:
   \[
   x_{t+1} - x_t - v_t = 0 \quad \text{for } t = 0, 1, \dots, T-1
   \]
   \[
   v_{t+1} - v_t - a_t = 0 \quad \text{for } t = 0, 1, \dots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = x_0, \quad v_0 = v_0
   \]

3. Target conditions:
   \[
   x_T = x_T, \quad v_T = v_T
   \]

4. Thrust limitation:
   \[
   -M \leq a_t \leq M \quad \text{for } t = 0, 1, \dots, T-1
   \]
   where \( M \) is the maximum allowable thrust.

The output format consists of lists for positions, velocities, accelerations, and total fuel spent:

\[
\text{Output:}
\]

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

\section*{Rocket Motion Linear Programming Model}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. The discrete-time model is defined as follows:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We assume that the acceleration \( a_t \) is controlled by the rocket thrust, and its magnitude \( |a_t| \) is proportional to the rate of fuel consumption at time \( t \). Given the initial conditions:

\[
x_0, \quad v_0
\]

we aim to reach a target position \( x_T \) with a target velocity \( v_T \) at time \( T \). Our objective is to minimize the maximum thrust required:

\[
\text{Objective:} \quad \min \max_{t} |a_t|
\]

The constraints for the problem can be formulated as follows:

1. State update equations for position and velocity:
   \[
   x_{t+1} - x_t - v_t = 0 \quad \text{for } t = 0, 1, \dots, T-1
   \]
   \[
   v_{t+1} - v_t - a_t = 0 \quad \text{for } t = 0, 1, \dots, T-1
   \]

2. Initial conditions:
   \[
   x_0 = x_0, \quad v_0 = v_0
   \]

3. Target conditions:
   \[
   x_T = x_T, \quad v_T = v_T
   \]

4. Thrust limitation:
   \[
   -M \leq a_t \leq M \quad \text{for } t = 0, 1, \dots, T-1
   \]
   where \( M \) is the maximum allowable thrust.

The output format consists of lists for positions, velocities, accelerations, and total fuel spent:

\[
\text{Output:}
\]

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

#### Extracting data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Defining variables
T = data['T']
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
M = 10  #### Assuming a maximum allowable thrust

#### Create a linear programming problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

#### Defining the variables for positions, velocities, and accelerations
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=-M, upBound=M) for t in range(T)]

#### Setting the initial conditions
problem += (x[0] == x0), "InitialPosition"
problem += (v[0] == v0), "InitialVelocity"

#### Adding the state update equations as constraints
for t in range(T):
    problem += (x[t + 1] - x[t] - v[t] == 0), f"PositionUpdate_{t}"
    problem += (v[t + 1] - v[t] - a[t] == 0), f"VelocityUpdate_{t}"

#### Adding the target conditions
problem += (x[T] == xT), "FinalPosition"
problem += (v[T] == vT), "FinalVelocity"

#### Objective function: minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable('max_thrust', lowBound=0)
for t in range(T):
    problem += (a[t] <= max_thrust), f"MaxThrustUpper_{t}"
    problem += (-a[t] <= max_thrust), f"MaxThrustLower_{t}"
problem += pulp.lpSum(a[t] for t in range(T))  #### Assuming thrust relates to fuel spent

#### Solve the problem
problem.solve()

#### Extracting the results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]

#### Assuming total fuel spent relates to the sum of the absolute values of accelerations
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

#### Output the results
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

