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
To model this problem, we need to formulate an optimization problem that minimizes the maximum thrust (or acceleration) required at any time step \( t \) while ensuring that the rocket reaches the target position \( x_T \) with velocity \( v_T \) at time \( T \). The constraints include the equations of motion and the initial conditions.

Below is the mathematical formulation of the problem, along with the constraints and objective function:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} 

Minimize the maximum thrust required, which is \(\max_t |a_t|\). 

\textbf{Constraints:}
\begin{align*}
& x_{t+1} = x_t + v_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& x_0 \text{ given}, \\
& v_0 \text{ given}, \\
& x_T \text{ target position}, \\
& v_T \text{ target velocity}.
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
& a_t \text{ for } t = 0, 1, 2, \ldots, T-1, \\
& x_t \text{ for } t = 0, 1, 2, \ldots, T, \\
& v_t \text{ for } t = 0, 1, 2, \ldots, T.
\end{align*}

\textbf{Optimization Problem:}
\begin{align*}
\text{Minimize} \quad & \max_{t=0, 1, \ldots, T-1} |a_t| \\
\text{subject to:} \quad & x_{t+1} = x_t + v_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& x_0 \text{ is given}, \\
& v_0 \text{ is given}, \\
& x_T \text{ is the target position}, \\
& v_T \text{ is the target velocity}.
\end{align*}

\textbf{Fuel Consumption:}
The total fuel spent can be assumed to be proportional to the sum of absolute accelerations, i.e.,
\[
\text{fuel\_spend} = \sum_{t=0}^{T-1} |a_t|
\]

\end{document}
```

This linear programming formulation seeks to minimize the maximum of the absolute values of the accelerations \( a_t \), which correspond to minimizing the peak thrust required. The total fuel spent is given by the sum of the absolute values of the accelerations over all time steps. The constraints ensure that the rocket's position and velocity follow the discrete-time equations of motion, starting from given initial conditions and reaching the specified target conditions at time \( T \).

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

Minimize the maximum thrust required, which is \(\max_t |a_t|\). 

\textbf{Constraints:}
\begin{align*}
& x_{t+1} = x_t + v_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& x_0 \text{ given}, \\
& v_0 \text{ given}, \\
& x_T \text{ target position}, \\
& v_T \text{ target velocity}.
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
& a_t \text{ for } t = 0, 1, 2, \ldots, T-1, \\
& x_t \text{ for } t = 0, 1, 2, \ldots, T, \\
& v_t \text{ for } t = 0, 1, 2, \ldots, T.
\end{align*}

\textbf{Optimization Problem:}
\begin{align*}
\text{Minimize} \quad & \max_{t=0, 1, \ldots, T-1} |a_t| \\
\text{subject to:} \quad & x_{t+1} = x_t + v_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& v_{t+1} = v_t + a_t, \quad t = 0, 1, 2, \ldots, T-1, \\
& x_0 \text{ is given}, \\
& v_0 \text{ is given}, \\
& x_T \text{ is the target position}, \\
& v_T \text{ is the target velocity}.
\end{align*}

\textbf{Fuel Consumption:}
The total fuel spent can be assumed to be proportional to the sum of absolute accelerations, i.e.,
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

#### Given data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Max_Thrust", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  #### acceleration variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  #### position variables
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  #### velocity variables

#### Objective Function: Minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

#### Constraints
problem += (x[0] == X0, "Initial_Position_Constraint")
problem += (v[0] == V0, "Initial_Velocity_Constraint")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (a[t] <= max_thrust, f"Max_Thrust_Upper_{t}")  #### a_t <= max_thrust
    problem += (a[t] >= -max_thrust, f"Max_Thrust_Lower_{t}")  #### a_t >= -max_thrust

#### Last position and velocity constraints
problem += (x[T] == XT, "Target_Position_Constraint")
problem += (v[T] == VT, "Target_Velocity_Constraint")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

