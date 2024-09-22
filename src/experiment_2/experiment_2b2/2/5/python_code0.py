import pulp

# Load data
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

# Initialize the LP problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

# Extract data
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
capacities = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
costs = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}
flow_reqs = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Create decision variables
flow_vars = pulp.LpVariable.dicts("flow", (range(data['NumFlowReqs']), links), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[f][(i, j)] * costs[(i, j)] for f in range(data['NumFlowReqs']) for (i, j) in links)

# Constraints: Capacity constraints
for (i, j) in links:
    problem += pulp.lpSum(flow_vars[f][(i, j)] for f in range(data['NumFlowReqs'])) <= capacities[(i, j)], f"Cap_Constraint_{i}_{j}"

# Flow conservation constraints
for f, (source, destination, rate) in enumerate(flow_reqs):
    nodes = set(data['StartNode'] + data['EndNode'])
    for node in nodes:
        if node == source:
            problem += pulp.lpSum(flow_vars[f][(node, j)] for j in nodes if (node, j) in links) - \
                       pulp.lpSum(flow_vars[f][(i, node)] for i in nodes if (i, node) in links) == rate, f"FlowCons_Src_{f}_{node}"
        elif node == destination:
            problem += pulp.lpSum(flow_vars[f][(node, j)] for j in nodes if (node, j) in links) - \
                       pulp.lpSum(flow_vars[f][(i, node)] for i in nodes if (i, node) in links) == -rate, f"FlowCons_Dest_{f}_{node}"
        else:
            problem += pulp.lpSum(flow_vars[f][(node, j)] for j in nodes if (node, j) in links) - \
                       pulp.lpSum(flow_vars[f][(i, node)] for i in nodes if (i, node) in links) == 0, f"FlowCons_Node_{f}_{node}"

# Solve problem
problem.solve()

# Extract results
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for f, (source, destination, rate) in enumerate(flow_reqs):
    path_flow = {}
    path_cost = 0
    for (i, j) in links:
        flow_value = flow_vars[f][(i, j)].varValue
        if flow_value is not None and flow_value > 0:
            path_flow[(i, j)] = flow_value
            path_cost += flow_value * costs[(i, j)]
            
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": list(path_flow.keys()),
        "path_flow": path_flow,
        "path_cost": path_cost
    })

optimized_paths["total_cost"] = total_cost

import json
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')