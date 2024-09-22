# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Consider a communication network consisting of \var{n} nodes.
- Nodes are con­nected by communication links.
- A link allowing one-way transmission from node \var{i} to node \var{j} is described by an ordered pair (\var{i},\var{j}). 
- Let \var{A} be the set of all links. 
- We assume that each link (\var{i},\var{j}) \in \var{A} can carry up to \var{U_{i,j}} bits per second. 
- There is a positive cost \var{C_{i,j}} per bit transmitted along that link. 
- Each node \var{k} generates data, at the rate of \var{B_{k,l}} bits per second, that have to be transmitted to node \var{l}, either through a direct link (\var{k}, \var{l}) or by tracing a sequence of links. 
- We allow the data with the same origin and destination to be split and be transmitted along different paths.

INPUT FORMAT:

{
    "links": [
       {
        "start": i,
        "end": j,
        "U": U_{i,j},
        "C": C_{i,j},
       }
    ],
    "data": [
        {
            "source": k,
            "destination": l,
            "rate": B_{k,l}
        }
    ]
}


OBJECTIVE: Find paths along which all data reach their intended destinations, while minimizing the total cost. 



OUTPUT INFO:
- \var{total_cost} represents the total cost of all the paths
- \var{path_cost} represents the cost of the corresponding path
- \var{path_flow} represents the flow going through the corresponding path

OUTPUT FORMAT:

{
    "optimized_paths": {
        "paths": [
            {
                "source": k,
                "destination": l,
                "route": [k, i_1, i_2, ..., l],
                "path_flow": path_flow
                "path_cost": path_cost
            },
            for id in 1, ..., m 
        ],
    "total_cost": "total_cost"
}
</DESCRIPTION>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import json
import pulp

#### Input data
data = {
    'NumLinks': 4,
    'StartNode': [1, 2, 2, 3],
    'EndNode': [2, 3, 4, 4],
    'Capacity': [50, 40, 60, 50],
    'Cost': [2, 3, 1, 1],
    'NumFlowReqs': 2,
    'Source': [1, 2],
    'Destination': [4, 3],
    'DataRate': [40, 30]
}

#### Extract data from the input
links = [
    (data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i])
    for i in range(data['NumLinks'])
]
flows = [
    (data['Source'][i], data['Destination'][i], data['DataRate'][i])
    for i in range(data['NumFlowReqs'])
]

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Create decision variables
flow_vars = pulp.LpVariable.dicts("flow", ((i, j) for i, j, _, _ in links), lowBound=0)

#### Objective function: minimize total cost
problem += pulp.lpSum(flow_vars[i, j] * cost for (i, j, _, cost) in links)

#### Constraints
for (source, destination, rate) in flows:
    problem += pulp.lpSum(flow_vars[i, j] for (i, j, _, _) in links if i == source) == rate

for (i, j, capacity, _) in links:
    problem += flow_vars[i, j] <= capacity

#### Solve the problem
problem.solve()

#### Prepare the output
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for (source, destination, rate) in flows:
    path_flow = 0
    route = [source]
    
    while True:
        for (i, j, _, _) in links:
            if i == source and flow_vars[i, j].value() > 0:
                route.append(j)
                path_flow = flow_vars[i, j].value()
                source = j
                break
        else:
            break
    
    path_cost = sum(flow_vars[i, j].value() * cost for (i, j, _, cost) in links if (i, j) in flow_vars and flow_vars[i, j].value() > 0)
    
    optimized_paths["paths"].append({
        "source": route[0],
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

#### Print the optimized paths and total cost
print(json.dumps(optimized_paths))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

