import pulp
import json

# Given data in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Define parameters
K = len(data["inputone"])  # Number of industries
T = 2  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("Build_Capa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("Stock_Hold", (range(K), range(T)), lowBound=0)

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T)), "Total_Production"

# Constraints
# Year0: Stock inventory
for k in range(K):
    problem += stockhold[k][0] == data["stock"][k] + produce[k][0] - pulp.lpSum(data["inputone"][k][j] * produce[j][0] for j in range(K)), f"Stock_Year0_{k}"
    
# Year1: Stock inventory and inputs
for k in range(K):
    problem += stockhold[k][1] == stockhold[k][0] + produce[k][1] - pulp.lpSum(data["inputone"][k][j] * produce[j][1] for j in range(K)), f"Stock_Year1_{k}"

# Year1 & Year2: Capacity building constraints
for k in range(K):
    problem += pulp.lpSum(data["inputtwo"][k][j] * buildcapa[j][0] for j in range(K)) + data["stock"][k] >= produce[k][0] + buildcapa[k][0], f"Capacity_Building_Year1_{k}"
    problem += pulp.lpSum(data["inputtwo"][k][j] * buildcapa[j][1] for j in range(K)) + stockhold[k][1] >= produce[k][1] + buildcapa[k][1], f"Capacity_Building_Year2_{k}"

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data["manpowerone"][k] * produce[k][t] + data["manpowertwo"][k] * buildcapa[k][t] for k in range(K)) <= data["manpower_limit"], f"Manpower_Limit_Year{t}"

# Solve the problem
problem.solve()

# Print the results
produce_result = [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]

# Output results
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')