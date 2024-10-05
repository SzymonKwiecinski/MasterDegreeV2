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

#### Define the problem
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

#### Extract data from JSON format
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

#### Defining variables
flow_vars = {}
for i in range(data['NumLinks']):
    for req in range(data['NumFlowReqs']):
        flow_vars[(data['StartNode'][i], data['EndNode'][i], req)] = pulp.LpVariable(
            f"flow_{data['StartNode'][i]}_{data['EndNode'][i]}_req_{req}",
            lowBound=0,
            upBound=data['Capacity'][i],
            cat=pulp.LpContinuous
        )

#### Objective: Minimize the total cost of flow
problem += pulp.lpSum(
    flow_vars[(data['StartNode'][i], data['EndNode'][i], req)] * data['Cost'][i]
    for i in range(data['NumLinks'])
    for req in range(data['NumFlowReqs'])
)

#### Flow conservation constraints
nodes = set(data['StartNode'] + data['EndNode'])
for node in nodes:
    for req in range(data['NumFlowReqs']):
        inflow = pulp.lpSum(
            flow_vars[(i, node, req)]
            for i in data['StartNode'] if (i, node, req) in flow_vars
        )
        outflow = pulp.lpSum(
            flow_vars[(node, j, req)]
            for j in data['EndNode'] if (node, j, req) in flow_vars
        )

        if node == data['Source'][req]:
            problem += (outflow - inflow == data['DataRate'][req])
        elif node == data['Destination'][req]:
            problem += (outflow - inflow == -data['DataRate'][req])
        else:
            problem += (outflow == inflow)

#### Solve the problem
problem.solve()

#### Retrieve results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}
for req in range(data['NumFlowReqs']):
    path = {
        "source": data['Source'][req],
        "destination": data['Destination'][req],
        "route": [],
        "path_flow": 0,
        "path_cost": 0
    }
    total_cost = 0
    for i in range(data['NumLinks']):
        flow = pulp.value(flow_vars[(data['StartNode'][i], data['EndNode'][i], req)])
        if flow > 0:
            path["route"].append(data['StartNode'][i])
            path["path_flow"] += flow
            path["path_cost"] += flow * data['Cost'][i]
    path["route"].append(data['Destination'][req])
    optimized_paths["paths"].append(path)
    total_cost += path["path_cost"]
    
print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

