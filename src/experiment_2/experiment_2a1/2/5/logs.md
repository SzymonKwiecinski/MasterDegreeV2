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

#### Load data from the provided JSON format
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 
        'DataRate': [40, 30]}

#### Define problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

#### Create decision variables for flows on each link
link_vars = {}
for i in range(data['NumLinks']):
    link = (data['StartNode'][i], data['EndNode'][i])
    link_vars[link] = pulp.LpVariable(f'flow_{link}', lowBound=0, upBound=data['Capacity'][i])

#### Objective Function: Minimize total cost
total_cost = pulp.lpSum(link_vars[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i]
                         for i in range(data['NumLinks']))
problem += total_cost

#### Constraints to ensure all data rates are met
for flow_req in range(data['NumFlowReqs']):
    source = data['Source'][flow_req]
    destination = data['Destination'][flow_req]
    rate = data['DataRate'][flow_req]
    
    #### Flow conservation constraints
    problem += (pulp.lpSum(link_vars.get((source, j), 0) for j in data['EndNode']) -
                 pulp.lpSum(link_vars.get((j, destination), 0) for j in data['StartNode'])) == rate

#### Solve the problem
problem.solve()

#### Prepare output
optimized_paths = {"paths": []}
total_cost_value = pulp.value(problem.objective)

for flow_req in range(data['NumFlowReqs']):
    source = data['Source'][flow_req]
    destination = data['Destination'][flow_req]
    path_flow = None
    path_cost = None
    route = []
    
    for link in link_vars:
        if link_vars[link].varValue > 0 and link[0] == source:
            route.append(link[0])  #### Start with the source
            path_flow = link_vars[link].varValue
            path_cost = data['Cost'][data['StartNode'].index(link[0])]
            route.append(link[1])  #### Append the end node
    
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

#### Adding total cost to the output
optimized_paths["total_cost"] = total_cost_value

#### Print the output in required format
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
```

