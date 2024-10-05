# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A state wants to plan its electricity capacity for the next \var{T} years. 
- The state has a forecast of \var{demand_t} megawatts, presumed accurate, of the demand for electricity during year \var{t}.
- The existing capacity, which is in oil-fired plants, that will not be retired and will be available during year \var{t}, is \var{oil_t}.
- There are two alternatives for expanding electric capacity: coal­ fired or nuclear power plants.
- There is a capital cost of \var{coal_cost} per megawatt of coal-fired capacity that becomes operational at the beginning of year \var{t}.
- There is a capital cost of \var{nuke_cost} per megawatt of nuclear power capacity that becomes operational at the beginning of year \var{t}.
- For various political and safety reasons, it has been decided that no more than \var{max_nuke}% of the total capacity should ever be nuclear (\var{max_nuke} is a number between 0 and 100).
- Coal plants last for \var{coal_life} years, while nuclear plants last for \var{nuke_life} years.

INPUT FORMAT: 

{
    "demand": [demand_t for t in 1, ..., T],
    "oil_cap": [oil_t for t in 1, ..., T],
    "coal_cost": coal_cost,
    "nuke_cost": nuke_cost,
    "max_nuke": max_nuke,
    "coal_life": coal_life,
    "nuke_life": nuke_life,
}


OBJECTIVE: What is the capacity expansion plan that results in the minimum cost?


OUTPUT INFO:

- the output should represent how much coal and nuclear capacity should be added in each year, and how much the total cost is.
- the output should be a dictionary with three keys: "coal_cap_added", "nuke_cap_added", and "total_cost".
- the value of "coal_cap_added" should be a list of the coal capacity added in each year.
- the value of "nuke_cap_added" should be a list of the nuclear capacity added in each year.
- the value of "total_cost" should be a single floating point number showing the total cost of the system.


OUTPUT FORMAT:

{
    "coal_cap_added": [coal_t for t in 1, ..., T],
    "nuke_cap_added": [nuke_t for t in 1, ..., T],
    "total_cost": total_cost,
}


</DESCRIPTION>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data from JSON
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

#### Define problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

#### Decision variables
coal_cap_added = [pulp.LpVariable(f'CoalCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]
nuke_cap_added = [pulp.LpVariable(f'NukeCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]

#### Objective function: Minimize total cost
total_cost = pulp.lpSum([data['CoalCost'] * coal_cap_added[t] + data['NukeCost'] * nuke_cap_added[t] for t in range(data['T'])])
problem += total_cost

#### Constraints

#### Capacity constraints: Coal plants last for `coal_life` years and nuclear plants for `nuke_life` years
for t in range(data['T']):
    total_coal_cap = pulp.lpSum([coal_cap_added[i] for i in range(max(0, t - data['CoalLife'] + 1), t + 1)])
    total_nuke_cap = pulp.lpSum([nuke_cap_added[i] for i in range(max(0, t - data['NukeLife'] + 1), t + 1)])
    
    problem += total_coal_cap + total_nuke_cap + data['OilCap'][t] >= data['Demand'][t]

    #### Constraint on maximum nuclear capacity
    problem += total_nuke_cap <= data['MaxNuke'] / 100.0 * (data['OilCap'][t] + total_coal_cap + total_nuke_cap)

#### Solve the problem
problem.solve()

#### Prepare results
result = {
    "coal_cap_added": [pulp.value(coal_cap_added[t]) for t in range(data['T'])],
    "nuke_cap_added": [pulp.value(nuke_cap_added[t]) for t in range(data['T'])],
    "total_cost": pulp.value(problem.objective)
}

#### Print result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

