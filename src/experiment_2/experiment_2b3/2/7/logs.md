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
To solve this problem, we must model the rocket's motion and minimize the maximum thrust required (i.e., the maximum acceleration). We'll use the PuLP library to set up and solve this linear programming problem.

Here is the Python code to achieve that:

```python
import pulp

#### Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

#### Create a LP minimization problem
problem = pulp.LpProblem("Minimum_Thrust_Rocket", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=-1, upBound=1, cat='Continuous') for t in range(T)]  #### Assuming |a_t| <= 1

#### Objective Function: Minimize the maximum absolute thrust (acceleration)
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')
problem += M

#### Initial conditions
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

#### Dynamics constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    #### Limit the maximum thrust
    problem += (a[t] <= M, f"Max_Thrust_Upper_{t}")
    problem += (-a[t] <= M, f"Max_Thrust_Lower_{t}")

#### Final conditions
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

#### Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=False))

#### Collect the results
x_result = [pulp.value(x[t]) for t in range(T+1)]
v_result = [pulp.value(v[t]) for t in range(T+1)]
a_result = [pulp.value(a[t]) for t in range(T)]

#### Calculate total fuel spent (sum of absolute accelerations)
fuel_spent = sum(abs(a_t) for a_t in a_result)

output = {
    "x": x_result[1:],
    "v": v_result[1:],
    "a": a_result,
    "fuel_spend": fuel_spent,
}

print(output)
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

This code constructs the LP problem where:

- We minimize the variable `M`, representing the maximum magnitude of acceleration used by the rocket.
- We ensure that the rocket follows the given dynamic model and satisfies the initial and final conditions.
- We calculate the total fuel spent as the sum of absolute values of the accelerations used over the time period.

