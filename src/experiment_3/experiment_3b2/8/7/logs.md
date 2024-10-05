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
To model this problem as a linear programming problem, we need to define the decision variables, constraints, and objective function in a formal way.

######### Decision Variables

- \( x_t \): Position of the rocket at time \( t \).
- \( v_t \): Velocity of the rocket at time \( t \).
- \( a_t \): Acceleration of the rocket at time \( t \).
- Introduce a new variable \( M \) to represent the maximum thrust required, i.e., \( M = \max_t |a_t| \).

######### Objective

Minimize the maximum thrust required, \( M \).

######### Constraints

1. Position Update: \( x_{t+1} = x_t + v_t \) for \( t = 0, 1, \ldots, T-1 \).
2. Velocity Update: \( v_{t+1} = v_t + a_t \) for \( t = 0, 1, \ldots, T-1 \).
3. Initial Conditions: \( x_0 = \text{given initial position} \), \( v_0 = \text{given initial velocity} \).
4. Terminal Conditions: \( x_T = \text{given target position} \), \( v_T = \text{given target velocity} \).
5. Maximum Thrust: \( -M \leq a_t \leq M \) for \( t = 0, 1, \ldots, T-1 \).

######### Linear Programming Formulation in LaTeX

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\min M
\]

\textbf{Subject to:}

\[
x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1
\]

\[
v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1
\]

\[
x_0 = x_0^{\text{given}}
\]

\[
v_0 = v_0^{\text{given}}
\]

\[
x_T = x_T^{\text{given}}
\]

\[
v_T = v_T^{\text{given}}
\]

\[
-M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\]

The total fuel spent can be calculated as:
\[
\text{fuel\_spend} = \sum_{t = 0}^{T-1} |a_t|
\]

\end{document}
```

This LP model minimizes the maximum thrust \( M \) required while satisfying the given dynamic constraints and boundary conditions. The total fuel spent, which is not directly minimized in the LP but can be calculated after obtaining the optimal accelerations \( a_t \), is the sum of the absolute values of the accelerations over the time period.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\min M
\]

\textbf{Subject to:}

\[
x_{t+1} = x_t + v_t, \quad t = 0, 1, \ldots, T-1
\]

\[
v_{t+1} = v_t + a_t, \quad t = 0, 1, \ldots, T-1
\]

\[
x_0 = x_0^{\text{given}}
\]

\[
v_0 = v_0^{\text{given}}
\]

\[
x_T = x_T^{\text{given}}
\]

\[
v_T = v_T^{\text{given}}
\]

\[
-M \leq a_t \leq M, \quad t = 0, 1, \ldots, T-1
\]

The total fuel spent can be calculated as:
\[
\text{fuel\_spend} = \sum_{t = 0}^{T-1} |a_t|
\]

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']
M = 10  #### Define a large finite value for M

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Fuel_Spend", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=-M, upBound=M)

#### Objective Function
problem += pulp.lpSum(a[t] for t in range(T)), "Total_Fuel_Spend"

#### Initial Conditions
problem += x[0] == X0, "Initial_Position"
problem += v[0] == V0, "Initial_Velocity"
problem += x[T] == XT, "Final_Position"
problem += v[T] == VT, "Final_Velocity"

#### Dynamics Constraints
for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t], f"Position_Update_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

