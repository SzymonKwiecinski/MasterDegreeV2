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

\section*{Rocket Movement Problem}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_t \) be the position of the rocket at time \( t \).
    \item \( v_t \) be the velocity of the rocket at time \( t \).
    \item \( a_t \) be the acceleration of the rocket at time \( t \).
\end{itemize}

\subsection*{Model Formulation}
The discrete-time model of the rocket can be described by the following equations:

\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
\end{align}

The goal is to reach a target position \( x_T \) with velocity \( v_T \) at time \( T \) given the initial conditions \( x_0 \) and \( v_0 \).

\subsection*{Objective Function}
Our objective is to minimize the maximum thrust required, expressed mathematically as:

\[
\min \max_{t} |a_t|
\]

\subsection*{Constraints}
The constraints on our system based on the desired final state are:

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

Additionally, we have the following constraints regarding the accelerations:

\[
|a_t| \leq A \quad \forall t = 0, 1, \ldots, T-1
\]

where \( A \) is the permissible thrust limit.

\subsection*{Input Format}
The input parameters are given as follows:

\[
\text{Input} = \{ x_0, v_0, x_T, v_T, T \}
\]

\subsection*{Output Format}
The output of the optimization problem is structured as:

\[
\text{Output} = \{ 
    x = [x_i \text{ for } i = 0, \ldots, T], 
    v = [v_i \text{ for } i = 0, \ldots, T], 
    a = [a_i \text{ for } i = 0, \ldots, T], 
    \text{fuel\_spend} = \text{total fuel spent}
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

\section*{Rocket Movement Problem}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_t \) be the position of the rocket at time \( t \).
    \item \( v_t \) be the velocity of the rocket at time \( t \).
    \item \( a_t \) be the acceleration of the rocket at time \( t \).
\end{itemize}

\subsection*{Model Formulation}
The discrete-time model of the rocket can be described by the following equations:

\begin{align}
    x_{t+1} &= x_t + v_t \quad \forall t = 0, 1, \ldots, T-1 \\
    v_{t+1} &= v_t + a_t \quad \forall t = 0, 1, \ldots, T-1
\end{align}

The goal is to reach a target position \( x_T \) with velocity \( v_T \) at time \( T \) given the initial conditions \( x_0 \) and \( v_0 \).

\subsection*{Objective Function}
Our objective is to minimize the maximum thrust required, expressed mathematically as:

\[
\min \max_{t} |a_t|
\]

\subsection*{Constraints}
The constraints on our system based on the desired final state are:

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

Additionally, we have the following constraints regarding the accelerations:

\[
|a_t| \leq A \quad \forall t = 0, 1, \ldots, T-1
\]

where \( A \) is the permissible thrust limit.

\subsection*{Input Format}
The input parameters are given as follows:

\[
\text{Input} = \{ x_0, v_0, x_T, v_T, T \}
\]

\subsection*{Output Format}
The output of the optimization problem is structured as:

\[
\text{Output} = \{ 
    x = [x_i \text{ for } i = 0, \ldots, T], 
    v = [v_i \text{ for } i = 0, \ldots, T], 
    a = [a_i \text{ for } i = 0, \ldots, T], 
    \text{fuel\_spend} = \text{total fuel spent}
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = '{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}'
parameters = json.loads(data)

#### Assign parameters
x0 = parameters['X0']
v0 = parameters['V0']
xT = parameters['XT']
vT = parameters['VT']
T = parameters['T']

#### Define the problem
problem = pulp.LpProblem("Rocket_Movement_Problem", pulp.LpMinimize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

#### Initial conditions
problem += (x[0] == x0)
problem += (v[0] == v0)

#### Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

#### Final state constraints
problem += (x[T] == xT)
problem += (v[T] == vT)

#### Max thrust limit
A = pulp.LpVariable("A", lowBound=0)  #### Thrust limit
for t in range(T):
    problem += (a[t] <= A)
    problem += (a[t] >= -A)

#### Objective function: minimize the maximum thrust requirement
problem += (A)

#### Solve the problem
problem.solve()

#### Collect results
results = {
    "x": [pulp.value(x[i]) for i in range(T+1)],
    "v": [pulp.value(v[i]) for i in range(T+1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

