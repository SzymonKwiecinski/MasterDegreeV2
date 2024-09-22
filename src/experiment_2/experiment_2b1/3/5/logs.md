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

#### Extracting the data from the input
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flow_reqs = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost_Flow", pulp.LpMinimize)

#### Create variables for flow on each link
flow_vars = pulp.LpVariable.dicts("Flow", [(start, end) for (start, end, _, _) in links], lowBound=0)

#### Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for (start, end, capacity, cost) in links)

#### Constraints: Capacity for each link
for (start, end, capacity, _) in links:
    problem += flow_vars[(start, end)] <= capacity

#### Flow conservation constraints for sources and sinks
for (source, destination, rate) in flow_reqs:
    #### Flow into the destination node should equal data rate
    problem += pulp.lpSum(flow_vars.get((i, destination), 0) for i in range(1, 5) if (i, destination) in flow_vars) \
               - pulp.lpSum(flow_vars.get((destination, j), 0) for j in range(1, 5) if (destination, j) in flow_vars) == 0
    
    #### Flow out of the source node should equal the data rate
    problem += pulp.lpSum(flow_vars.get((source, j), 0) for j in range(1, 5) if (source, j) in flow_vars) == rate

#### Solve the problem
problem.solve()

#### Prepare output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

#### Collecting the flows and corresponding costs
for (source, dest, capacity, cost) in links:
    if (source, dest) in flow_vars:
        path_flow = flow_vars[(source, dest)].varValue
        if path_flow > 0:
            path_cost = path_flow * cost
            optimized_paths['paths'].append({
                "source": source,
                "destination": dest,
                "route": [source, dest],  #### Simplified route for direct links
                "path_flow": path_flow,
                "path_cost": path_cost
            })

#### Output result
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

