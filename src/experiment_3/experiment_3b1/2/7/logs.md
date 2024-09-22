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

\section*{Mathematical Model for Rocket Motion}

Let:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
    \item \( T \): Total time for the journey
    \item \( x_0 \): Initial position
    \item \( v_0 \): Initial velocity
    \item \( x_T \): Target position
    \item \( v_T \): Target velocity
\end{itemize}

The discrete-time model is defined by the following equations:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We need to find the acceleration \( a_t \) for \( t = 0, 1, \ldots, T-1 \), under the constraints given below, while minimizing the maximum thrust required.

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which is expressed as:
\[
\text{Minimize } \max_{t} |a_t|
\]

\subsection*{Constraints}
The constraints based on initial conditions and final targets are:
\[
x_0 = x_0 \quad \text{(initial position)}
\]
\[
v_0 = v_0 \quad \text{(initial velocity)}
\]
\[
x_T = x_T \quad \text{(target position)}
\]
\[
v_T = v_T \quad \text{(target velocity)}
\]

The evolution of the states gives us these implicit constraints:
\[
x_{t+1} - x_t - v_t = 0, \quad \forall t \in \{0, 1, \ldots, T-1\}
\]
\[
v_{t+1} - v_t - a_t = 0, \quad \forall t \in \{0, 1, \ldots, T-1\}
\]

\subsection*{Fuel Consumption}
Assuming fuel consumption is proportional to the magnitude of acceleration:
\[
\text{Fuel spent} = \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Decision Variables}
The decision variables are:
\begin{itemize}
    \item \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
\end{itemize}

\subsection*{Summary of Output}
The output will consist of:
\begin{itemize}
    \item A list of positions \( x_i \) for \( i = 0, 1, \ldots, T \)
    \item A list of velocities \( v_i \) for \( i = 0, 1, \ldots, T \)
    \item A list of accelerations \( a_i \) for \( i = 0, 1, \ldots, T \)
    \item Total fuel spent
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

Let:
\begin{itemize}
    \item \( x_t \): Position of the rocket at time \( t \)
    \item \( v_t \): Velocity of the rocket at time \( t \)
    \item \( a_t \): Acceleration of the rocket at time \( t \)
    \item \( T \): Total time for the journey
    \item \( x_0 \): Initial position
    \item \( v_0 \): Initial velocity
    \item \( x_T \): Target position
    \item \( v_T \): Target velocity
\end{itemize}

The discrete-time model is defined by the following equations:
\[
x_{t+1} = x_t + v_t
\]
\[
v_{t+1} = v_t + a_t
\]

We need to find the acceleration \( a_t \) for \( t = 0, 1, \ldots, T-1 \), under the constraints given below, while minimizing the maximum thrust required.

\subsection*{Objective Function}
The objective is to minimize the maximum thrust required, which is expressed as:
\[
\text{Minimize } \max_{t} |a_t|
\]

\subsection*{Constraints}
The constraints based on initial conditions and final targets are:
\[
x_0 = x_0 \quad \text{(initial position)}
\]
\[
v_0 = v_0 \quad \text{(initial velocity)}
\]
\[
x_T = x_T \quad \text{(target position)}
\]
\[
v_T = v_T \quad \text{(target velocity)}
\]

The evolution of the states gives us these implicit constraints:
\[
x_{t+1} - x_t - v_t = 0, \quad \forall t \in \{0, 1, \ldots, T-1\}
\]
\[
v_{t+1} - v_t - a_t = 0, \quad \forall t \in \{0, 1, \ldots, T-1\}
\]

\subsection*{Fuel Consumption}
Assuming fuel consumption is proportional to the magnitude of acceleration:
\[
\text{Fuel spent} = \sum_{t=0}^{T-1} |a_t|
\]

\subsection*{Decision Variables}
The decision variables are:
\begin{itemize}
    \item \( a_t \) for \( t = 0, 1, \ldots, T-1 \)
\end{itemize}

\subsection*{Summary of Output}
The output will consist of:
\begin{itemize}
    \item A list of positions \( x_i \) for \( i = 0, 1, \ldots, T \)
    \item A list of velocities \( v_i \) for \( i = 0, 1, \ldots, T \)
    \item A list of accelerations \( a_i \) for \( i = 0, 1, \ldots, T \)
    \item Total fuel spent
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create the problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### Acceleration variables
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)   #### Max thrust variable

#### Objective function: Minimize the maximum thrust
problem += max_thrust, "MinimizeMaxThrust"

#### Constraints for the rocket motion model
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]

#### Initial conditions
problem += (x[0] == X0, "InitialPosition")
problem += (v[0] == V0, "InitialVelocity")

#### Evolution constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionEvolution_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityEvolution_{t}")

#### Final conditions
problem += (x[T] == XT, "TargetPosition")
problem += (v[T] == VT, "TargetVelocity")

#### Maximum thrust constraint
for t in range(T):
    problem += (a[t] <= max_thrust, f"MaxThrustConstraintPos_{t}")
    problem += (a[t] >= -max_thrust, f"MaxThrustConstraintNeg_{t}")

#### Solve the problem
problem.solve()

#### Output results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Positions:", positions)
print("Velocities:", velocities)
print("Accelerations:", accelerations)
print("Total Fuel Spent:", fuel_spent)
```

