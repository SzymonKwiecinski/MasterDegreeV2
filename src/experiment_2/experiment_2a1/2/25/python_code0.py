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

# Constants
K = len(data['inputone'])  # Number of industries
T = 2  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Constraints for each industry and each year
for k in range(K):
    for t in range(T):
        # Stocks from previous year and current production
        if t == 0:
            stock_previous = data['stock'][k]
        else:
            stock_previous = stockhold[k][t-1]
        
        # Manpower constraints
        manpower_used = data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t]
        problem += manpower_used <= data['manpower_limit'], f"Manpower_limit_{k}_{t}"
        
        # Input constraints
        total_input = stock_previous + sum(produce[j][t-1] * data['inputone'][j][k] for j in range(K) if t > 0)
        problem += total_input >= produce[k][t] + sum(buildcapa[j][t-1] * data['inputtwo'][j][k] for j in range(K) if t > 0), f"Input_constraints_{k}_{t}"

        # Stocks for the next year
        if t < T - 1:
            problem += stockhold[k][t] == stock_previous + produce[k][t] - produce[k][t], f"Stock_hold_{k}_{t}"

# Objective function: Maximize total production in the last two years
objective = pulp.lpSum(produce[k][t] for k in range(K) for t in range(T))
problem += objective, "Total_Production"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')