import pulp

# Extract data from the JSON format
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

# Define sets and parameters
A = list(zip(data['StartNode'], data['EndNode']))
U = {(i, j): data['Capacity'][index] for index, (i, j) in enumerate(A)}
C = {(i, j): data['Cost'][index] for index, (i, j) in enumerate(A)}
K = data['Source']
L = data['Destination']
B = {(k, l): data['DataRate'][index] for index, (k, l) in enumerate(zip(K, L))}

# Initialize the LP problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("Flow", A, lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total Cost"

# Flow conservation constraints
all_nodes = set(data['StartNode']) | set(data['EndNode'])

for k in all_nodes:
    if k not in K and k not in L:
        problem += (pulp.lpSum(x[k, j] for (k, j) in A if k == k) -
                    pulp.lpSum(x[i, k] for (i, k) in A if k == k) == 0), f"Flow_Conservation_at_{k}"

# Supply constraints at source nodes
for k in K:
    l = L[K.index(k)]
    problem += (pulp.lpSum(x[k, j] for (k, j) in A if k == k) == B[k, l]), f"Supply_at_Source_{k}"

# Demand constraints at destination nodes
for l in L:
    k = K[L.index(l)]
    problem += (pulp.lpSum(x[i, l] for (i, l) in A if l == l) == B[k, l]), f"Demand_at_Destination_{l}"

# Capacity constraints
for i, j in A:
    problem += (x[i, j] <= U[i, j]), f"Capacity_{i}_{j}"

# Solve the problem
problem.solve()

# Print the results
optimized_paths = [(i, j, pulp.value(x[i, j]), C[i, j] * pulp.value(x[i, j])) for (i, j) in A if pulp.value(x[i, j]) > 0]
total_cost = pulp.value(problem.objective)

print(f"Optimized Paths and Flow:")
for path in optimized_paths:
    print(f"From Node {path[0]} to Node {path[1]}: Flow={path[2]} with Cost={path[3]}")
print(f"Total Cost: {total_cost}")

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')