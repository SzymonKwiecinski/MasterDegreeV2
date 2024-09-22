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
import pulp

#### Data
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

#### Parse the JSON data
links = list(zip(data['StartNode'], data['EndNode'], data['Capacity'], data['Cost']))
flow_reqs = list(zip(data['Source'], data['Destination'], data['DataRate']))

#### Create a linear programming problem
problem = pulp.LpProblem("NetworkOptimization", pulp.LpMinimize)

#### Variables
flow_vars = {}
for (i, j, U, C) in links:
    for (k, l, rate) in flow_reqs:
        flow_vars[(k, l, i, j)] = pulp.LpVariable(f"flow_{k}_{l}_{i}_{j}", lowBound=0)

#### Objective Function: Minimize the total cost
problem += pulp.lpSum(C * flow_vars[(k, l, i, j)] for (i, j, U, C) in links for (k, l, rate) in flow_reqs)

#### Constraints
#### Capacity constraints on each link
for (i, j, U, C) in links:
    problem += pulp.lpSum(flow_vars[(k, l, i, j)] for (k, l, rate) in flow_reqs) <= U

#### Flow conservation for each flow request
for (k, l, rate) in flow_reqs:
    #### Outflow from source node
    problem += pulp.lpSum(flow_vars[(k, l, k, j)] for (start, j, U, C) in links if start == k) - \
               pulp.lpSum(flow_vars[(k, l, i, k)] for (i, end, U, C) in links if end == k) == rate
    #### Inflow to destination node
    problem += pulp.lpSum(flow_vars[(k, l, i, l)] for (i, end, U, C) in links if end == l) - \
               pulp.lpSum(flow_vars[(k, l, l, j)] for (start, j, U, C) in links if start == l) == rate
    #### Conservation of flow for other nodes
    for node in set(data['StartNode'] + data['EndNode']):
        if node != k and node != l:
            problem += pulp.lpSum(flow_vars[(k, l, i, node)] for (i, end, U, C) in links if end == node) == \
                       pulp.lpSum(flow_vars[(k, l, node, j)] for (start, j, U, C) in links if start == node)

#### Solve the problem
problem.solve()

#### Results
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

#### Construct the result outputs
for (k, l, rate) in flow_reqs:
    paths_for_request = []
    for (i, j, U, C) in links:
        flow_value = pulp.value(flow_vars[(k, l, i, j)])
        if flow_value > 1e-5:  #### Consider only non-zero flows
            paths_for_request.append({
                "source": k,
                "destination": l,
                "route": [i, j],
                "path_flow": flow_value,
                "path_cost": flow_value * C,
            })
    optimized_paths["paths"].extend(paths_for_request)

optimized_paths["total_cost"] = total_cost

#### Output
import json
output = {
    "optimized_paths": optimized_paths
}
print(json.dumps(output, indent=4))
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

