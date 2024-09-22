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

OBJECTIVE: The objective is to minimize the total fuel \sum_{t=0}^{\var{T}-1} |\var{a_t}| spent subject to the preceding constraints.

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
To model this problem as a linear programming problem, we need to define the decision variables, the objective function, and the constraints. 

######### Decision Variables
- \( a_t \): Acceleration at time \( t \), for \( t = 0, 1, \ldots, T-1 \).
- \( x_t \): Position at time \( t \), for \( t = 0, 1, \ldots, T \).
- \( v_t \): Velocity at time \( t \), for \( t = 0, 1, \ldots, T \).

######### Objective Function
The objective is to minimize the total absolute acceleration (fuel consumption):
\[
\min \sum_{t=0}^{T-1} |a_t|
\]

######### Constraints
1. **Initial Conditions:**
   - \( x_0 = \text{given initial position} \)
   - \( v_0 = \text{given initial velocity} \)

2. **Final Conditions:**
   - \( x_T = \text{desired final position} \)
   - \( v_T = \text{desired final velocity} \)

3. **System Dynamics:**
   - \( x_{t+1} = x_t + v_t \), for \( t = 0, 1, \ldots, T-1 \)
   - \( v_{t+1} = v_t + a_t \), for \( t = 0, 1, \ldots, T-1 \)

4. **Fuel Consumption (absolute value constraint):**
   - To handle the absolute values in a linear program, introduce auxiliary variables \( u_t \) such that:
     \[
     a_t \leq u_t \quad \text{and} \quad -a_t \leq u_t \quad \text{for } t = 0, 1, \ldots, T-1
     \]
   The objective now becomes:
   \[
   \min \sum_{t=0}^{T-1} u_t
   \]

Now, let's write the problem in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Rocket Trajectory Optimization}

\textbf{Decision Variables:}
\begin{align*}
a_t &: \text{Acceleration at time } t, \quad t = 0, 1, \ldots, T-1 \\
x_t &: \text{Position at time } t, \quad t = 0, 1, \ldots, T \\
v_t &: \text{Velocity at time } t, \quad t = 0, 1, \ldots, T \\
u_t &: \text{Auxiliary variable for fuel consumption at time } t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\textbf{Objective Function:}
\[
\min \sum_{t=0}^{T-1} u_t
\]

\textbf{Constraints:}

- \text{Initial Conditions:}
\[
x_0 = \text{given } x_0, \quad v_0 = \text{given } v_0
\]

- \text{Final Conditions:}
\[
x_T = \text{desired } x_T, \quad v_T = \text{desired } v_T
\]

- \text{System Dynamics:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

- \text{Fuel Consumption Constraints:}
\begin{align*}
a_t &\leq u_t, \quad t = 0, 1, \ldots, T-1 \\
-a_t &\leq u_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}
```

This model can be solved using any standard LP solver to obtain the optimal acceleration values \( a_t \), and subsequently, we can compute the positions \( x_t \) and velocities \( v_t \) using the provided constraints.

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

\textbf{Decision Variables:}
\begin{align*}
a_t &: \text{Acceleration at time } t, \quad t = 0, 1, \ldots, T-1 \\
x_t &: \text{Position at time } t, \quad t = 0, 1, \ldots, T \\
v_t &: \text{Velocity at time } t, \quad t = 0, 1, \ldots, T \\
u_t &: \text{Auxiliary variable for fuel consumption at time } t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\textbf{Objective Function:}
\[
\min \sum_{t=0}^{T-1} u_t
\]

\textbf{Constraints:}

- \text{Initial Conditions:}
\[
x_0 = \text{given } x_0, \quad v_0 = \text{given } v_0
\]

- \text{Final Conditions:}
\[
x_T = \text{desired } x_T, \quad v_T = \text{desired } v_T
\]

- \text{System Dynamics:}
\begin{align*}
x_{t+1} &= x_t + v_t, \quad t = 0, 1, \ldots, T-1 \\
v_{t+1} &= v_t + a_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

- \text{Fuel Consumption Constraints:}
\begin{align*}
a_t &\leq u_t, \quad t = 0, 1, \ldots, T-1 \\
-a_t &\leq u_t, \quad t = 0, 1, \ldots, T-1
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data from JSON
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Define the Linear Programming problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable.dicts("a", (range(T)), lowBound=None, cat='Continuous')
x = pulp.LpVariable.dicts("x", (range(T+1)), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", (range(T+1)), lowBound=None, cat='Continuous')
u = pulp.LpVariable.dicts("u", (range(T)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(u[t] for t in range(T)), "Minimize fuel consumption"

#### Constraints
#### Initial Conditions
problem += (x[0] == x_0), "Initial_Position"
problem += (v[0] == v_0), "Initial_Velocity"

#### Final Conditions
problem += (x[T] == x_T), "Final_Position"
problem += (v[T] == v_T), "Final_Velocity"

#### System Dynamics
for t in range(T):
    problem += (x[t+1] == x[t] + v[t]), f"Position_Equation_{t}"
    problem += (v[t+1] == v[t] + a[t]), f"Velocity_Equation_{t}"

#### Fuel Consumption Constraints
for t in range(T):
    problem += (a[t] <= u[t]), f"Positive_Acceleration_Constraint_{t}"
    problem += (-a[t] <= u[t]), f"Negative_Acceleration_Constraint_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

