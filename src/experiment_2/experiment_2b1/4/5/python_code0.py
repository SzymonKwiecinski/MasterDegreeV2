import json
import pulp

# Input data in dict format
data = {
    "NumLinks": 4,
    "StartNode": [1, 2, 2, 3],
    "EndNode": [2, 3, 4, 4],
    "Capacity": [50, 40, 60, 50],
    "Cost": [2, 3, 1, 1],
    "NumFlowReqs": 2,
    "Source": [1, 2],
    "Destination": [4, 3],
    "DataRate": [40, 30]
}

# Extracting data for the problem formulation
links = [
    {
        "start": data["StartNode"][i],
        "end": data["EndNode"][i],
        "U": data["Capacity"][i],
        "C": data["Cost"][i],
    }
    for i in range(data["NumLinks"])
]

flows = [
    {
        "source": data["Source"][i],
        "destination": data["Destination"][i],
        "rate": data["DataRate"][i]
    }
    for i in range(data["NumFlowReqs"])
]

# Initialize LP problem
problem = pulp.LpProblem("Minimize_Transport_Cost", pulp.LpMinimize)

# Create flow variables for each link
flow_vars = pulp.LpVariable.dicts("Flow", 
                                   ((link["start"], link["end"]) for link in links), 
                                   lowBound=0,
                                   upBound=link["U"],
                                   cat='Continuous')

# Objective function: Minimize cost
problem += pulp.lpSum(flow_vars[(link["start"], link["end"])] * link["C"]
                       for link in links), "Total_Cost"

# Supply constraints (flow conservation)
for flow in flows:
    flow_rate = flow["rate"]
    src, dest = flow["source"], flow["destination"]
    
    # Outflow from source
    problem += (pulp.lpSum(flow_vars[(src, link["end"])] for link in links if link["start"] == src) == flow_rate)

    # Inflow to destination
    problem += (pulp.lpSum(flow_vars[(link["start"], dest)] for link in links if link["end"] == dest) == flow_rate)

# Capacity constraints
for link in links:
    problem += (flow_vars[(link["start"], link["end"])] <= link["U"], 
                f"Capacity_Constraint_{link['start']}_to_{link['end']}")

# Solve the problem
problem.solve()

# Prepare results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for flow in flows:
    src, dest = flow["source"], flow["destination"]
    path_flow = 0
    if flow_vars[(src, dest)].varValue is not None:
        path_flow = flow_vars[(src, dest)].varValue
        path_cost = path_flow * next(link["C"] for link in links if link["start"] == src and link["end"] == dest)
        optimized_paths["paths"].append({
            "source": src,
            "destination": dest,
            "route": [src, dest],
            "path_flow": path_flow,
            "path_cost": path_cost
        })

# Output the total cost
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(optimized_paths, indent=4))