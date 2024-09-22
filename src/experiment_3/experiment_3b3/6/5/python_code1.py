import pulp
import json

# Data provided
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

# Sets and Parameters
N = list(set(data['StartNode'] + data['EndNode']))
A = list(zip(data['StartNode'], data['EndNode']))
U = {(i, j): cap for i, j, cap in zip(data['StartNode'], data['EndNode'], data['Capacity'])}
C = {(i, j): cost for i, j, cost in zip(data['StartNode'], data['EndNode'], data['Cost'])}
B = {(k, l): rate for k, l, rate in zip(data['Source'], data['Destination'], data['DataRate'])}

# Problem Definition
problem = pulp.LpProblem("Communication_Network_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Flow", A, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([C[i, j] * x[i, j] for i, j in A])

# Constraints
# Capacity constraints
for i, j in A:
    problem += x[i, j] <= U[i, j], f"Capacity_constraint_{i}_{j}"

# Flow conservation constraints
for node in N:
    for k, l in zip(data['Source'], data['Destination']):
        flow_balance = (pulp.lpSum([x[i, j] for i, j in A if i == node]) -
                        pulp.lpSum([x[j, i] for j, i in A if j == node]))
        
        if node == k:
            problem += flow_balance == B[k, l], f"Flow_conservation_source_{node}_{l}"
        elif node == l:
            problem += flow_balance == -B[k, l], f"Flow_conservation_dest_{node}_{k}"
        else:
            problem += flow_balance == 0, f"Flow_conservation_{node}"

# Solve the problem
problem.solve()

# Extract results
optimized_paths = {
    "optimized_paths": {
        "paths": [],
        "total_cost": pulp.value(problem.objective)
    }
}

# Calculate path costs and flows
for k, l in zip(data['Source'], data['Destination']):
    path = [k]
    path_flow = float('inf')
    current_node = k
    path_cost = 0

    for _ in range(len(N)):  # Limit the number of iterations to avoid infinite loop
        found_next_node = False
        for i, j in A:
            if i == current_node and x[i, j].varValue > 0:
                path.append(j)
                path_flow = min(path_flow, x[i, j].varValue)
                path_cost += C[i, j] * x[i, j].varValue
                current_node = j
                found_next_node = True
                break
        if not found_next_node:
            break

    optimized_paths["optimized_paths"]["paths"].append({
        "source": k,
        "destination": l,
        "route": path,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the paths
print(json.dumps(optimized_paths, indent=4))