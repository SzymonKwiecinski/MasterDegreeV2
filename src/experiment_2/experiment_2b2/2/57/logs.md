# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A seaport unloads shipping containers off of rail cars, holds them in its yard on a transport system, and then loads them onto ships.
- The demand \var{demand_{t}} for containers by ships varies every month, and this demand must be fulfilled.
- The unloading cost \var{unload_cost_{t}} per container indicates how much it costs to unload a single container from the rail car.
- The unloading capacity \var{unload_capacity_{t}} specifies the maximum number of containers that can be unloaded in a month.
- For each container kept in the yard until the subsequent month, there is a holding cost of $\var{holding_cost}.
- Due to space limitations, the yard can store a maximum of \var{max_container} containers at the end of any month.
- Initially, at the start of the first month, the yard has \var{init_container} containers.
- The yard should not contain any containers after the end of the last month.
- Additionally, loading containers onto ships necessitates the rental of cranes.
- A maximum of \var{num_cranes} cranes can be rented each month, each having a capacity to load \var{crane_capacity} containers.
- It costs \var{crane_cost} for each crane.

INPUT FORMAT: 

{
    "demands": [demand_{t} for t in 1, ..., T],
    "unload_costs": [unload_cost_{t} for t in 1, ..., T],
    "unload_capacity": [unload_capacity_{t} for t in 1, ..., T],
    "holding_cost": holding_cost,
    "max_container": max_container,
    "init_container": init_container,
    "num_cranes": num_cranes,
    "crane_capacity": crane_capacity,
    "crane_cost": crane_cost,
}

OBJECTIVE: Determine a strategy to minimize costs from unloading, storage, and crane rentals over the period.

OUTPUT INFO:

- \var{amount_{t}} indicates the number of containers unloaded for each month.
- \var{crane_{t}} specifies the number of cranes rented for each month.
- \var{total_cost} shows the total cost of the company over the period.

OUTPUT FORMAT:

{
    "containers_unloaded": [amount_{t} for t in 1, ..., T],
    "cranes_rented": [crane_{t} for t in 1, ..., T],
    "total_cost": total_cost
}

</DESCRIPTION>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

#### Initialize problem
problem = pulp.LpProblem("Seaport_Container_Optimization", pulp.LpMinimize)

#### Define Variables
amount = pulp.LpVariable.dicts("Amount", range(data['T']), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("Cranes", range(data['T']), lowBound=0, cat='Integer')
cont_in_yard = pulp.LpVariable.dicts("ContainersInYard", range(data['T'] + 1), lowBound=0, cat='Integer')

#### Initial condition
cont_in_yard[0] = data['InitContainer']

#### Objective Function
problem += pulp.lpSum([amount[t] * data['UnloadCosts'][t] + cranes[t] * data['CraneCost'] +
                       cont_in_yard[t+1] * data['HoldingCost'] for t in range(data['T'])])

#### Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"UnloadCapacity_{t}"

    problem += cranes[t] <= data['NumCranes'], f"MaxCranes_{t}"

    problem += cranes[t] * data['CraneCapacity'] >= data['Demands'][t], f"DemandFulfillment_{t}"

    problem += cont_in_yard[t] + amount[t] - data['Demands'][t] == cont_in_yard[t+1], f"FlowBalance_{t}"

    problem += cont_in_yard[t+1] <= data['MaxContainer'], f"MaxYardCapacity_{t+1}"

#### Final condition
problem += cont_in_yard[data['T']] == 0, "EndPeriodCondition"

#### Solve the problem
problem.solve()

#### Construct output
output = {
    "containers_unloaded": [amount[t].varValue for t in range(data['T'])],
    "cranes_rented": [cranes[t].varValue for t in range(data['T'])],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

