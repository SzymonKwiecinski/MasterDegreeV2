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

#### Data in JSON format
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

#### Extract data for the problem
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flows = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

#### Create a LP problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

#### Decision variables for flow on each link
flow_vars = pulp.LpVariable.dicts("Flow", [(start, end) for start, end, _, _ in links], 0)

#### Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, _, cost in links)

#### Constraints for flow capacity
for start, end, capacity, _ in links:
    problem += flow_vars[(start, end)] <= capacity

#### Flow conservation constraints for each source and destination
for source, destination, rate in flows:
    #### Outflow from source
    problem += pulp.lpSum(flow_vars[(source, end)] for start, end in links if start == source) == rate

    #### Inflow to destination
    problem += pulp.lpSum(flow_vars[(start, destination)] for start, end in links if end == destination) == rate

#### Solve the problem
problem.solve()

#### Collect optimized paths and costs
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for source, destination, rate in flows:
    path_flow = 0
    path_cost = 0
    route = []
    
    for start, end in flow_vars.keys():
        if start == source and flow_vars[(start, end)].varValue > 0:
            flow_value = flow_vars[(start, end)].varValue
            path_flow += flow_value
            path_cost += flow_value * next(cost for s, e, _, cost in links if s == start and e == end)
            route.append(end)
            
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": [source] + route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

#### Output the results
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

