import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['stock'])  # Number of industries
T = 2  # Number of years to consider for production

# Create the LP problem
problem = pulp.LpProblem("Industry_Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T)), "Total_Production"

# Constraints
# Year 0 stocks and production limitations
for k in range(K):
    problem += stockhold[k][0] + produce[k][0] <= data['stock'][k] + data['capacity'][k], f"Stock_Capacity_Year_0_{k}"

# Yearly manpower limits
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Limit_Year_{t}"

# Stock and production relationship
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k][t - 1] + produce[k][t] == stockhold[k][t] + data['capacity'][k], f"Stock_Hold_Year_{t}_{k}"

# Input constraints for production and capacity building
for k in range(K):
    for t in range(1, T):  # Production inputs can only be for t = 1 (second year)
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t - 1] for j in range(K)) + data['stock'][k] >= produce[k][t], f"Input_Production_Year_{t}_{k}"
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in range(K)) >= buildcapa[k][t], f"Input_Build_Capa_Year_{t}_{k}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')