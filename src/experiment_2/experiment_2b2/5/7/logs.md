# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

#### Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Parameters
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

#### Model
problem = LpProblem("Rocket_Trajectory_Optimization", LpMinimize)

#### Variables
x = [LpVariable(f'x_{t}', cat='Continuous') for t in range(T+1)]
v = [LpVariable(f'v_{t}', cat='Continuous') for t in range(T+1)]
a = [LpVariable(f'a_{t}', lowBound=None, cat='Continuous') for t in range(T)]

#### Auxiliary variable for max |a_t|
max_a = LpVariable('max_a', lowBound=0, cat='Continuous')

#### Objective
problem += max_a

#### Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Equation_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Equation_{t}")
    problem += (a[t] <= max_a, f"Max_Acc_Constraint_Pos_{t}")
    problem += (-a[t] <= max_a, f"Max_Acc_Constraint_Neg_{t}")

problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

#### Solve the problem
problem.solve()

#### Prepare the output
x_values = [value(x[t]) for t in range(1, T+1)]
v_values = [value(v[t]) for t in range(1, T+1)]
a_values = [value(a[t]) for t in range(T)]
fuel_spent = sum(abs(value(a[t])) for t in range(T))

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f'(Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
```

