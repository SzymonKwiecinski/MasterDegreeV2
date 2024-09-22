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
To solve this problem using Linear Programming, we need to formulate the objective and constraints in a mathematical model. The aim is to minimize the maximum thrust required, which is represented by minimizing the maximum absolute value of the acceleration \(|a_t|\) across all time steps.

Here's the linear programming formulation:

######### Decision Variables:
- \( x_t \): position of the rocket at time \( t \)
- \( v_t \): velocity of the rocket at time \( t \)
- \( a_t \): acceleration of the rocket at time \( t \)
- \( M \): maximum absolute acceleration, \( M = \max_t |a_t| \)

######### Parameters:
- \( x_0 \): initial position
- \( v_0 \): initial velocity
- \( x_T \): target position at time \( T \)
- \( v_T \): target velocity at time \( T \)
- \( T \): time steps

######### Objective:
Minimize the maximum thrust required:
\[ 
\min M 
\]

######### Constraints:
1. Dynamics of the rocket:
   \[
   x_{t+1} = x_t + v_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   \[
   v_{t+1} = v_t + a_t \quad \text{for } t = 0, 1, \ldots, T-1
   \]

2. Absolute value constraint on acceleration:
   \[
   |a_t| \leq M \quad \text{for } t = 0, 1, \ldots, T-1
   \]
   This can be linearized as:
   \[
   a_t \leq M \quad \text{and} \quad -a_t \leq M \quad \text{for } t = 0, 1, \ldots, T-1
   \]

3. Initial conditions:
   \[
   x_0 = \text{given initial position}
   \]
   \[
   v_0 = \text{given initial velocity}
   \]

4. Final conditions:
   \[
   x_T = \text{given target position}
   \]
   \[
   v_T = \text{given target velocity}
   \]

5. Total fuel consumption is proportional to the sum of absolute accelerations:
   \[
   \text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
   \]

Let's create this linear programming formulation in \(\LaTeX\):

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Formulation for Rocket Trajectory Optimization}

\subsection*{Objective}
Minimize the maximum absolute acceleration:
\[
\min M
\]

\subsection*{Subject to Constraints}

\begin{align}
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
& a_t \leq M, \quad t = 0, 1, \ldots, T-1, \\
& -a_t \leq M, \quad t = 0, 1, \ldots, T-1, \\
& x_0 = \text{given }, \\
& v_0 = \text{given }, \\
& x_T = \text{given }, \\
& v_T = \text{given }.
\end{align}

\subsection*{Fuel Consumption}
The total fuel spent is calculated as:
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

This \(\LaTeX\) code describes the linear programming model for optimizing the rocket's trajectory to minimize the maximum thrust required. You can implement this model using a linear programming solver to find the optimal trajectory and fuel consumption.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Formulation for Rocket Trajectory Optimization}

\subsection*{Objective}
Minimize the maximum absolute acceleration:
\[
\min M
\]

\subsection*{Subject to Constraints}

\begin{align}
& x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1, \\
& a_t \leq M, \quad t = 0, 1, \ldots, T-1, \\
& -a_t \leq M, \quad t = 0, 1, \ldots, T-1, \\
& x_0 = \text{given }, \\
& v_0 = \text{given }, \\
& x_T = \text{given }, \\
& v_T = \text{given }.
\end{align}

\subsection*{Fuel Consumption}
The total fuel spent is calculated as:
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data from JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create a linear programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Define decision variables
M = pulp.LpVariable("M", lowBound=0)  #### Maximum absolute acceleration
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### Acceleration at each time step
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### Position at each time step
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### Velocity at each time step

#### Objective function: minimize M
problem += M, "Minimize_Max_Acceleration"

#### Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

#### Constraints for position and velocity
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

    #### Constraints on acceleration
    problem += (a[t] <= M, f"Max_Acceleration_{t}")
    problem += (-a[t] <= M, f"Min_Acceleration_{t}")

#### Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

