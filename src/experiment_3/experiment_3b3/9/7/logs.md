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

\section*{Rocket Motion Optimization Problem}

We are tasked with modeling the motion of a rocket along a straight path using a linear programming approach. We define:

\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time model is given by the following equations:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

We control the acceleration \( a_t \), which is related to the thrust and, in turn, to the fuel consumption. Our objective is to minimize the maximum thrust required, defined as:

\[
\text{Minimize } \max_{t} |a_t|
\]

######### Inputs

The inputs are defined as follows:

\begin{align*}
    x_0 & : \text{initial position} \\
    v_0 & : \text{initial velocity} \\
    x_T & : \text{target position} \\
    v_T & : \text{target velocity} \\
    T & : \text{total time}
\end{align*}

######### Constraints

We have the following constraints based on the motion equations:

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

Additionally, we assume that the acceleration is bounded:

\[
|a_t| \leq M \quad \forall t = 0, 1, \ldots, T-1
\]

where \( M \) is a constant that represents the maximum thrust.

######### Outputs

The required outputs are:

\begin{itemize}
    \item \( x \): a list of positions of the rocket at each time step from 0 to \( T \)
    \item \( v \): a list of velocities of the rocket at each time step from 0 to \( T \)
    \item \( a \): a list of accelerations of the rocket at each time step from 0 to \( T \)
    \item \( \text{fuel\_spend} \): total fuel spent by the rocket
\end{itemize}

The output format is specified as follows:

\[
\text{Output} = \{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel\_spend": \text{fuel\_spent}
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

\section*{Rocket Motion Optimization Problem}

We are tasked with modeling the motion of a rocket along a straight path using a linear programming approach. We define:

\begin{itemize}
    \item \( x_t \): position of the rocket at time \( t \)
    \item \( v_t \): velocity of the rocket at time \( t \)
    \item \( a_t \): acceleration of the rocket at time \( t \)
\end{itemize}

The discrete-time model is given by the following equations:

\begin{align}
    x_{t+1} &= x_t + v_t \\
    v_{t+1} &= v_t + a_t
\end{align}

We control the acceleration \( a_t \), which is related to the thrust and, in turn, to the fuel consumption. Our objective is to minimize the maximum thrust required, defined as:

\[
\text{Minimize } \max_{t} |a_t|
\]

######### Inputs

The inputs are defined as follows:

\begin{align*}
    x_0 & : \text{initial position} \\
    v_0 & : \text{initial velocity} \\
    x_T & : \text{target position} \\
    v_T & : \text{target velocity} \\
    T & : \text{total time}
\end{align*}

######### Constraints

We have the following constraints based on the motion equations:

\begin{align}
    x_T &= x_0 + \sum_{t=0}^{T-1} v_t \\
    v_T &= v_0 + \sum_{t=0}^{T-1} a_t
\end{align}

Additionally, we assume that the acceleration is bounded:

\[
|a_t| \leq M \quad \forall t = 0, 1, \ldots, T-1
\]

where \( M \) is a constant that represents the maximum thrust.

######### Outputs

The required outputs are:

\begin{itemize}
    \item \( x \): a list of positions of the rocket at each time step from 0 to \( T \)
    \item \( v \): a list of velocities of the rocket at each time step from 0 to \( T \)
    \item \( a \): a list of accelerations of the rocket at each time step from 0 to \( T \)
    \item \( \text{fuel\_spend} \): total fuel spent by the rocket
\end{itemize}

The output format is specified as follows:

\[
\text{Output} = \{
    "x": [x_i \text{ for } i = 0, \ldots, T],
    "v": [v_i \text{ for } i = 0, \ldots, T],
    "a": [a_i \text{ for } i = 0, \ldots, T],
    "fuel\_spend": \text{fuel\_spent}
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Initialize the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(data['T'] + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(data['T'] + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(data['T']), cat='Continuous')
max_thrust = pulp.LpVariable("Max_Thrust", lowBound=0, cat='Continuous')

#### Objective function
problem += max_thrust, "Minimize_Max_Thrust"

#### Add constraints
problem += (x[0] == data['X0'], "Initial_Position")
problem += (v[0] == data['V0'], "Initial_Velocity")

#### Equation constraints
for t in range(data['T']):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (-max_thrust <= a[t], f"Negative_Acceleration_Bound_{t}")
    problem += (a[t] <= max_thrust, f"Positive_Acceleration_Bound_{t}")

#### Final position and velocity constraints
problem += (x[data['T']] == data['XT'], "Final_Position")
problem += (v[data['T']] == data['VT'], "Final_Velocity")

#### Solve the problem
problem.solve()

#### Prepare the output
x_result = [x[i].varValue for i in range(data['T'] + 1)]
v_result = [v[i].varValue for i in range(data['T'] + 1)]
a_result = [a[i].varValue for i in range(data['T'])]
fuel_spend = sum(abs(a[i].varValue) for i in range(data['T']))

output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spend
}

#### Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

