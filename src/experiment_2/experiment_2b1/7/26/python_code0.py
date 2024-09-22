import pulp
import json

data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'demand': [60000000.0, 60000000.0, 30000000.0]}

K = len(data['stock'])
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    for k in range(K):
        # Stock balance
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t], f"Stock_Initial_{k}_{t}"
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t], f"Stock_Balance_{k}_{t}"

        # Demand satisfaction
        if t > 0:
            problem += stockhold[k][t] >= data['demand'][k], f"Demand_Satisfaction_{k}_{t}"

        # Producing according to input requirements
        problem += produce[k][t] <= data['capacity'][k], f"Capacity_Limit_{k}_{t}"

for t in range(T-1):
    for k in range(K):
        # Input uses for future production
        for j in range(K):
            problem += (produce[k][t] * data['inputone'][k][j] <= stockhold[j][t], f"Input_Use_{k}_{j}_{t}")

for t in range(T):
    for k in range(K):
        # Build capacity requires manpower and inputs
        problem += (buildcapa[k][t] * data['manpowertwo'][k] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j][t] for j in range(K)), 
                     f"Build_Capa_Use_{k}_{t}")

# Solve the problem
problem.solve()

# Output result
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')