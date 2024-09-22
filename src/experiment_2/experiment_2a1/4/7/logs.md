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
import pulp
import json

#### Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

#### Variables
T = data['T']
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']

#### Create the LP problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-pulp.LpInfinity, upBound=pulp.LpInfinity) for t in range(T)]

#### Objective: Minimize max_t |a_t|
max_a = pulp.LpVariable('max_a', lowBound=0)
problem += max_a

#### Constraints
problem += x[0] == x0
problem += v[0] == v0

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a[t] <= max_a
    problem += a[t] >= -max_a

#### Final conditions
problem += x[T] == xT
problem += v[T] == vT

#### Solve the problem
problem.solve()

#### Extract results
x_results = [pulp.value(x[t]) for t in range(T + 1)]
v_results = [pulp.value(v[t]) for t in range(T + 1)]
a_results = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_a)

#### Prepare output
output = {
    "x": x_results,
    "v": v_results,
    "a": a_results,
    "fuel_spend": fuel_spent,
}

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

