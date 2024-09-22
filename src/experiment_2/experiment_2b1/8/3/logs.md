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
import json

#### Input Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_added = pulp.LpVariable.dicts("CoalAdded", range(T), lowBound=0, cat='Continuous')
nuke_added = pulp.LpVariable.dicts("NukeAdded", range(T), lowBound=0, cat='Continuous')

#### Objective Function: Minimize total cost
problem += pulp.lpSum(coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T))

#### Constraints
for t in range(T):
    total_capacity = oil_cap[t]
    #### Add capacities from previous years considering their lifetime
    for c in range(1, coal_life + 1):
        if t - c >= 0:
            total_capacity += coal_added[t - c]
    for n in range(1, nuke_life + 1):
        if t - n >= 0:
            total_capacity += nuke_added[t - n]
    
    #### Demand constraints
    problem += (total_capacity >= demand[t], f"Demand_Constraint_{t}")
    
    #### Max nuclear capacity constraint
    problem += (nuke_added[t] <= max_nuke * total_capacity, f"Max_Nuclear_Capacity_Constraint_{t}")

#### Solve the problem
problem.solve()

#### Prepare the output
coal_cap_added = [pulp.value(coal_added[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

#### Output result
result = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

