# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- US soybean suppliers ship soybeans to different destinations using various routes.
- Consider a transportation network consisting of \var{n} cities.
- Soybeans are sent from a terminal city \var{k} to a port city \var{p}.
- Subsequently, Soybeans are transported from a port city \var{p} to a destination city \var{l}
- Let \var{A} be the set of all routes. 
- There is a positive transport cost \var{C_{i,j}} per metric ton along that route.
- Each source terminal \var{k} has a soybean supply of \var{supply_{k}}. 
- Each destination \var{l} has a demand for soybeans of \var{demand_{l}}.

INPUT FORMAT: 

{
    "routes": [
       {
        "start": i,
        "end": j,
        "C": C_{i,j},
       }
    ],
    "demand": [
        {
            "destination": l,
            "D": demand_{l}
        }
    ],
    "supply": [
        {
            "terminal": k,
            "S": supply_{k}
        }
    ]
}

OBJECTIVE: What quantity of soybeans should they from source to destination to minimize transportation costs?

OUTPUT INFO:

- the amount of soybeans shipped from \var{i} to \var{j} is \var{amount_{i,j}}.
- \var{total_cost} represents the total transportation cost.

OUTPUT FORMAT:

{
    "distribution": [
        {"from": i,
         "to": j,
         "amount": amount_{i,j}
        }
        for id in 1, ..., m
    ],
    "total_cost": total_cost
}


</DESCRIPTION>
<DATA>
{'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

#### Extracting data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost_matrix = data['Cost']
demand = data['Demand']
supply = data['Supply']

#### Define the problem
problem = pulp.LpProblem("Soybean Transportation Problem", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(cost_matrix[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations))

#### Constraints
#### Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i][j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

#### Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i][j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Prepare the output
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        if pulp.value(amount[i][j]) > 0:  #### Only include non-zero shipments
            distribution.append({
                "from": i,
                "to": j,
                "amount": pulp.value(amount[i][j])
            })

#### Total cost
total_cost = pulp.value(problem.objective)

#### Output the results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

#### Print the output in JSON format
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

