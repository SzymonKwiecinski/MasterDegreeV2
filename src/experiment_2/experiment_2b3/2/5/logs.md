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

#### Load data from JSON
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

#### Problem definition
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

#### Variables
flows = {}
for idx in range(data['NumLinks']):
    for flow in range(data['NumFlowReqs']):
        flows[(flow, data['StartNode'][idx], data['EndNode'][idx])] = pulp.LpVariable(
            f"flow_{flow}_{data['StartNode'][idx]}_{data['EndNode'][idx]}",
            lowBound=0,
            cat='Continuous'
        )

#### Objective function
problem += pulp.lpSum([
    flows[(flow, data['StartNode'][idx], data['EndNode'][idx])] * data['Cost'][idx]
    for idx in range(data['NumLinks'])
    for flow in range(data['NumFlowReqs'])
])

#### Constraints
#### Capacity constraints
for idx in range(data['NumLinks']):
    problem += pulp.lpSum([
        flows[(flow, data['StartNode'][idx], data['EndNode'][idx])]
        for flow in range(data['NumFlowReqs'])
    ]) <= data['Capacity'][idx], f"Cap_{data['StartNode'][idx]}_{data['EndNode'][idx]}"

#### Flow conservation constraints
nodes = set(data['StartNode']) | set(data['EndNode'])
for flow in range(data['NumFlowReqs']):
    source = data['Source'][flow]
    destination = data['Destination'][flow]
    for node in nodes:
        if node == source:
            problem += (pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) -
                        pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) ==
                        data['DataRate'][flow]), f"FlowConservation_Source_{flow}_{node}"
        elif node == destination:
            problem += (pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) -
                        pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) ==
                        data['DataRate'][flow]), f"FlowConservation_Destination_{flow}_{node}"
        else:
            problem += (pulp.lpSum([flows[(flow, node, j)] for j in nodes if (flow, node, j) in flows]) -
                        pulp.lpSum([flows[(flow, i, node)] for i in nodes if (flow, i, node) in flows]) ==
                        0), f"FlowConservation_{flow}_{node}"

#### Solve the problem
problem.solve()

#### Collect results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for flow in range(data['NumFlowReqs']):
    path_details = {
        "source": data['Source'][flow],
        "destination": data['Destination'][flow],
        "route": [],
        "path_flow": 0,
        "path_cost": 0
    }

    for idx in range(data['NumLinks']):
        if pulp.value(flows[(flow, data['StartNode'][idx], data['EndNode'][idx])]) > 0:
            path_details["route"].append((data['StartNode'][idx], data['EndNode'][idx]))
            flow_value = pulp.value(flows[(flow, data['StartNode'][idx], data['EndNode'][idx])])
            path_details["path_flow"] += flow_value
            path_details["path_cost"] += flow_value * data['Cost'][idx]

    optimized_paths["paths"].append(path_details)

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

