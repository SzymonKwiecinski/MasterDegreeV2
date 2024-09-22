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

\section*{Rocket Thrust Optimization Problem}

We define the discrete-time model of the rocket's motion as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

where:
\begin{itemize}
    \item \(x_t\) is the position of the rocket at time \(t\),
    \item \(v_t\) is the velocity of the rocket at time \(t\),
    \item \(a_t\) is the acceleration of the rocket at time \(t\).
\end{itemize}

We are given the following initial conditions and target values:
\begin{itemize}
    \item Initial position: \(x_0\)
    \item Initial velocity: \(v_0\)
    \item Target position: \(x_T\)
    \item Target velocity: \(v_T\)
    \item Time horizon: \(T\)
\end{itemize}

Our objective is to minimize the maximum thrust required, defined as:
\[
\text{minimize } \max_{t} |a_t|
\]

Subject to the constraints:
\begin{align}
    x_0 &= x_0 \\
    v_0 &= v_0 \\
    x_T &= x_T \\
    v_T &= v_T
\end{align}

The state equations are iteratively defined as:
\begin{align}
    x_{t+1} &= x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
\end{align}

We define:
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

The output format should be structured as follows:

\begin{verbatim}
{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel_spend": \text{fuel\_spent},
}
\end{verbatim}

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

\section*{Rocket Thrust Optimization Problem}

We define the discrete-time model of the rocket's motion as follows:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

where:
\begin{itemize}
    \item \(x_t\) is the position of the rocket at time \(t\),
    \item \(v_t\) is the velocity of the rocket at time \(t\),
    \item \(a_t\) is the acceleration of the rocket at time \(t\).
\end{itemize}

We are given the following initial conditions and target values:
\begin{itemize}
    \item Initial position: \(x_0\)
    \item Initial velocity: \(v_0\)
    \item Target position: \(x_T\)
    \item Target velocity: \(v_T\)
    \item Time horizon: \(T\)
\end{itemize}

Our objective is to minimize the maximum thrust required, defined as:
\[
\text{minimize } \max_{t} |a_t|
\]

Subject to the constraints:
\begin{align}
    x_0 &= x_0 \\
    v_0 &= v_0 \\
    x_T &= x_T \\
    v_T &= v_T
\end{align}

The state equations are iteratively defined as:
\begin{align}
    x_{t+1} &= x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
\end{align}

We define:
\[
\text{fuel\_spent} = \sum_{t=0}^{T-1} |a_t|
\]

The output format should be structured as follows:

\begin{verbatim}
{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel_spend": \text{fuel\_spent},
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Extracting data
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("RocketThrustOptimization", pulp.LpMinimize)

#### Decision variables for acceleration
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Decision variables for position and velocity
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)

#### Objective: Minimize the maximum absolute thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

#### Constraints for position and velocity state equations
problem += x[0] == x0
problem += v[0] == v0

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
  
#### Constraints for the final position and final velocity
problem += x[T] == xT
problem += v[T] == vT

#### Constraints for thrust limits
for t in range(T):
    problem += a[t] <= max_thrust
    problem += a[t] >= -max_thrust

#### Solve the problem
problem.solve()

#### Collecting results
x_values = [x[i].varValue for i in range(T + 1)]
v_values = [v[i].varValue for i in range(T + 1)]
a_values = [a[i].varValue for i in range(T)]
fuel_spent = sum(abs(a[i].varValue) for i in range(T))

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Output format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spent": fuel_spent,
}

#### To view the output
print(output)
```

