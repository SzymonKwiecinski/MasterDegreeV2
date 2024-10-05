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
<DATA>
{'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we will use the PuLP library to set up and solve a linear programming problem. We need to minimize the total fuel consumption, which is the sum of the magnitudes of accelerations over time, while ensuring the rocket achieves the specified final position and velocity.

```python
import pulp

#### Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

#### Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

#### Create a linear programming problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat='Continuous')
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(abs_a[t] for t in range(T))

#### Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

#### Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

#### State update constraints
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]
    
    #### Absolute value constraints
    problem += abs_a[t] >= a[t]
    problem += abs_a[t] >= -a[t]

#### Solve the problem
problem.solve()

#### Prepare the solution
output = {
    "x": [pulp.value(x[i]) for i in range(T+1)],
    "v": [pulp.value(v[i]) for i in range(T+1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": pulp.value(problem.objective),
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This Python script uses the PuLP library to define and solve a linear programming problem. The objective is to minimize fuel usage, subject to position and velocity constraints at each time step. We use two variables \(a_t\) and \(|a_t|\) to handle the absolute value condition and ensure the solution conforms to the problem's requirements.

