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
import json

#### Load the data
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

#### Unpack the data
links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

#### Initialize the problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

#### Variables
flow_vars = {}
for f in range(flow_reqs):
    for l in range(links):
        flow_vars[(f, l)] = pulp.LpVariable(f"Flow_{f}_{l}", 0, capacities[l])

#### Objective Function: Minimize the total cost
problem += pulp.lpSum(flow_vars[(f, l)] * costs[l] for f in range(flow_reqs) for l in range(links))

#### Constraints: 
#### 1. Flow conservation: Ensure data flows from sources to destinations
for f in range(flow_reqs):
    for node in set(start_nodes + end_nodes):
        inflow = pulp.lpSum(flow_vars[(f, l)] for l in range(links) if end_nodes[l] == node)
        outflow = pulp.lpSum(flow_vars[(f, l)] for l in range(links) if start_nodes[l] == node)

        if node == sources[f]:
            problem += outflow - inflow == data_rates[f]
        elif node == destinations[f]:
            problem += inflow - outflow == data_rates[f]
        else:
            problem += inflow - outflow == 0

#### Capacity constraints
for l in range(links):
    problem += pulp.lpSum(flow_vars[(f, l)] for f in range(flow_reqs)) <= capacities[l]

#### Solve the problem
problem.solve()

#### Collect the results
result = {
    "optimized_paths": {
        "paths": [],
        "total_cost": pulp.value(problem.objective)
    }
}

for f in range(flow_reqs):
    path_flow = []
    path_cost = 0
    route = [sources[f]]
    current_node = sources[f]
    while current_node != destinations[f]:
        for l in range(links):
            if start_nodes[l] == current_node and pulp.value(flow_vars[(f, l)]) > 0:
                route.append(end_nodes[l])
                path_flow.append(pulp.value(flow_vars[(f, l)]))
                path_cost += pulp.value(flow_vars[(f, l)]) * costs[l]
                current_node = end_nodes[l]
                break
    
    result["optimized_paths"]["paths"].append({
        "source": sources[f],
        "destination": destinations[f],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

#### Output the result
output_json = json.dumps(result, indent=4)
print(output_json)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

