import pulp

# Data from JSON
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

# Sets
N = set(data['StartNode']).union(set(data['EndNode']))
A = list(zip(data['StartNode'], data['EndNode']))

# Parameters
U = {(i, j): cap for i, j, cap in zip(data['StartNode'], data['EndNode'], data['Capacity'])}
C = {(i, j): cost for i, j, cost in zip(data['StartNode'], data['EndNode'], data['Cost'])}
B = {(k, l): rate for k, l, rate in zip(data['Source'], data['Destination'], data['DataRate'])}

# Initialize the problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(C[i, j] * x[i, j] for i, j in A), "Total_Cost"

# Constraints

# Flow conservation constraints
for k in N:
    for l in N:
        if k != l:
            problem += pulp.lpSum(x[k, j] for j in N if (k, j) in A) - pulp.lpSum(x[i, k] for i in N if (i, k) in A) == (
                B.get((k, l), 0) - B.get((l, k), 0)
            ), f"Flow_Conservation_Node_{k}_to_{l}"

# Capacity constraints
for i, j in A:
    problem += x[i, j] <= U[i, j], f"Capacity_Constraint_for_Link_({i},{j})"

# Solve the problem
problem.solve()

# Output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for k, l in B.keys():
    path_flow = pulp.value(B[k, l])
    path_cost = pulp.lpSum(C[i, j] * x[i, j].varValue for i, j in A if x[i, j].varValue is not None)
    route = [k]  # This is a placeholder, the route determination would require additional logic
    optimized_paths["paths"].append({
        "source": k,
        "destination": l,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')