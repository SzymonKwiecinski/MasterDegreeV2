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
To formulate the given problem as a linear programming model, we will define a mathematical model in LaTeX format that captures the dynamics of the rocket and the objective to minimize the thrust. Here's how the model can be structured:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\subsection*{Objective}
Minimize the maximum thrust required, which is given by:

\[
\text{minimize} \quad M = \max_{t} |a_t|
\]

\subsection*{Constraints}

1. **Position and Velocity Constraints**:
   \begin{align*}
   x_{t+1} &= x_t + v_t & \forall t = 0, \ldots, T-1 \\
   v_{t+1} &= v_t + a_t & \forall t = 0, \ldots, T-1
   \end{align*}

2. **Initial Conditions**:
   \begin{align*}
   x_0 &= \text{given initial position (input)} \\
   v_0 &= \text{given initial velocity (input)}
   \end{align*}

3. **Target Conditions**:
   \begin{align*}
   x_T &= \text{target position (input)} \\
   v_T &= \text{target velocity (input)}
   \end{align*}

4. **Thrust (Acceleration) Constraints**:
   The magnitude of each acceleration must be bounded by the maximum thrust:
   \[
   -M \leq a_t \leq M \quad \forall t = 0, \ldots, T-1
   \]

5. **Fuel Usage**:
   Total fuel spend can be represented as the sum of absolute values of accelerations:
   \[
   \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
   \]

\subsection*{Decision Variables}

- \(x_t\): Position of the rocket at time \(t\).
- \(v_t\): Velocity of the rocket at time \(t\).
- \(a_t\): Acceleration of the rocket at time \(t\).
- \(M\): Maximum absolute acceleration, to be minimized.

\subsection*{Model Formulation}

To solve the above problem, we'll use linear programming techniques. The main objective is to minimize \(M\), subject to the position, velocity, and boundary constraints. 

The optimization problem can be implemented and solved using any LP solver by defining it with the given sets of constraints and conditions.

\end{document}
```

In this formulation, our goal is to find the values of \( a_t \), \( x_t \), and \( v_t \) for \( t = 0, \ldots, T \) that minimize the maximum absolute acceleration \( M \), while satisfying the position, velocity updates, and reaching the target conditions. The fuel spend is a secondary outcome, computed as the total absolute acceleration used over the time period.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\subsection*{Objective}
Minimize the maximum thrust required, which is given by:

\[
\text{minimize} \quad M = \max_{t} |a_t|
\]

\subsection*{Constraints}

1. **Position and Velocity Constraints**:
   \begin{align*}
   x_{t+1} &= x_t + v_t & \forall t = 0, \ldots, T-1 \\
   v_{t+1} &= v_t + a_t & \forall t = 0, \ldots, T-1
   \end{align*}

2. **Initial Conditions**:
   \begin{align*}
   x_0 &= \text{given initial position (input)} \\
   v_0 &= \text{given initial velocity (input)}
   \end{align*}

3. **Target Conditions**:
   \begin{align*}
   x_T &= \text{target position (input)} \\
   v_T &= \text{target velocity (input)}
   \end{align*}

4. **Thrust (Acceleration) Constraints**:
   The magnitude of each acceleration must be bounded by the maximum thrust:
   \[
   -M \leq a_t \leq M \quad \forall t = 0, \ldots, T-1
   \]

5. **Fuel Usage**:
   Total fuel spend can be represented as the sum of absolute values of accelerations:
   \[
   \text{Fuel Spend} = \sum_{t=0}^{T-1} |a_t|
   \]

\subsection*{Decision Variables}

- \(x_t\): Position of the rocket at time \(t\).
- \(v_t\): Velocity of the rocket at time \(t\).
- \(a_t\): Acceleration of the rocket at time \(t\).
- \(M\): Maximum absolute acceleration, to be minimized.

\subsection*{Model Formulation}

To solve the above problem, we'll use linear programming techniques. The main objective is to minimize \(M\), subject to the position, velocity, and boundary constraints. 

The optimization problem can be implemented and solved using any LP solver by defining it with the given sets of constraints and conditions.

\end{document}</MATH_MODEL>
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create a LP problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')

#### Objective
problem += M, "Minimize_Maximum_Thrust"

#### Constraints

#### Initial Conditions
problem += (x[0] == X0), "Initial_Position"
problem += (v[0] == V0), "Initial_Velocity"

#### Target Conditions
problem += (x[T] == XT), "Target_Position"
problem += (v[T] == VT), "Target_Velocity"

#### Position and Velocity Constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Constraint_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Constraint_{t}"

#### Thrust Constraints
for t in range(T):
    problem += (-M <= a[t]), f"Thrust_Lower_Bound_{t}"
    problem += (a[t] <= M), f"Thrust_Upper_Bound_{t}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

