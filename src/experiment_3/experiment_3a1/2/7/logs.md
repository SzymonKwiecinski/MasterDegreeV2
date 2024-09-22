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

\section*{Mathematical Model for Rocket Trajectory Control}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. We have the following relationships:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We assume that the acceleration \( a_t \) is controlled through the rocket thrust. To minimize fuel consumption, we will also minimize the maximum required thrust, denoted as \( \max_t |a_t| \).

######### Input Parameters

\begin{itemize}
    \item Initial position: \( x_0 \)
    \item Initial velocity: \( v_0 \)
    \item Target position: \( x_T \)
    \item Target velocity: \( v_T \)
    \item Time duration: \( T \)
\end{itemize}

######### Objective Function

We wish to minimize the maximum thrust used during the flight:

\[
\text{Minimize } Z = \max_{t=0,1,\ldots,T} |a_t|
\]

######### Constraints

The constraints for the model are derived from the position and velocity equations:

1. For \( t = 0, 1, \ldots, T-1 \):
   \[
   x_{t+1} = x_t + v_t
   \]
   \[
   v_{t+1} = v_t + a_t
   \]

2. Initial conditions:
   \[
   x_0, \quad v_0
   \]

3. Final conditions (at time \( T \)):
   \[
   x_T = x_T, \quad v_T = v_T
   \]

4. Control limits for acceleration:
   \[
   -M \leq a_t \leq M \quad \forall t = 0, 1, \ldots, T
   \]
   where \( M \) is a defined maximum thrust limit.

######### Output Variables

Define the output variables:

\begin{itemize}
    \item \( x = [x_0, x_1, \ldots, x_T] \) - positions at each time step
    \item \( v = [v_0, v_1, \ldots, v_T] \) - velocities at each time step
    \item \( a = [a_0, a_1, \ldots, a_{T-1}] \) - accelerations at each time step
    \item \( \text{fuel\_spend} \) - total fuel spent by the rocket
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

\section*{Mathematical Model for Rocket Trajectory Control}

Let \( x_t \), \( v_t \), and \( a_t \) represent the position, velocity, and acceleration of the rocket at time \( t \), respectively. We have the following relationships:

\[
x_{t+1} = x_t + v_t
\]

\[
v_{t+1} = v_t + a_t
\]

We assume that the acceleration \( a_t \) is controlled through the rocket thrust. To minimize fuel consumption, we will also minimize the maximum required thrust, denoted as \( \max_t |a_t| \).

######### Input Parameters

\begin{itemize}
    \item Initial position: \( x_0 \)
    \item Initial velocity: \( v_0 \)
    \item Target position: \( x_T \)
    \item Target velocity: \( v_T \)
    \item Time duration: \( T \)
\end{itemize}

######### Objective Function

We wish to minimize the maximum thrust used during the flight:

\[
\text{Minimize } Z = \max_{t=0,1,\ldots,T} |a_t|
\]

######### Constraints

The constraints for the model are derived from the position and velocity equations:

1. For \( t = 0, 1, \ldots, T-1 \):
   \[
   x_{t+1} = x_t + v_t
   \]
   \[
   v_{t+1} = v_t + a_t
   \]

2. Initial conditions:
   \[
   x_0, \quad v_0
   \]

3. Final conditions (at time \( T \)):
   \[
   x_T = x_T, \quad v_T = v_T
   \]

4. Control limits for acceleration:
   \[
   -M \leq a_t \leq M \quad \forall t = 0, 1, \ldots, T
   \]
   where \( M \) is a defined maximum thrust limit.

######### Output Variables

Define the output variables:

\begin{itemize}
    \item \( x = [x_0, x_1, \ldots, x_T] \) - positions at each time step
    \item \( v = [v_0, v_1, \ldots, v_T] \) - velocities at each time step
    \item \( a = [a_0, a_1, \ldots, a_{T-1}] \) - accelerations at each time step
    \item \( \text{fuel\_spend} \) - total fuel spent by the rocket
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']
M = 10  #### Define a maximum thrust limit

#### Define the problem
problem = pulp.LpProblem("Rocket_Trajectory_Control", pulp.LpMinimize)

#### Define decision variables
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-M, upBound=M) for t in range(T)]

#### Objective function: Minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

#### Constraints
problem += x[0] == x0  #### Initial position
problem += v[0] == v0  #### Initial velocity

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]  #### Position constraint
    problem += v[t + 1] == v[t] + a[t]  #### Velocity constraint

problem += x[T] == xT  #### Final position constraint
problem += v[T] == vT  #### Final velocity constraint

#### Maximum thrust constraints
for t in range(T):
    problem += max_thrust >= a[t]  #### Ensures max_thrust is at least a[t]
    problem += max_thrust >= -a[t]  #### Ensures max_thrust is at least -a[t]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

