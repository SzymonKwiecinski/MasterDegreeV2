import pulp
import json

data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['stock'])
T = 5

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Constraints for stocks and capacities
for k in range(K):
    for t in range(T):
        if t == 0:
            stock_current = data['stock'][k]
        else:
            stock_current = stockhold[k][t-1] + produce[k][t-1] - data['demand'][k]

        # Initial stock constraint for year 0
        if t == 0:
            problem += stockhold[k][t] == stock_current, f"Stock_Initial_Industry_{k}_Year_{t}"

        # Stocks for subsequent years
        problem += stockhold[k][t] == stock_current, f"Stock_Industry_{k}_Year_{t}"

        # Capacity constraint
        if t < T - 1:
            problem += produce[k][t] + buildcapa[k][t] <= data['capacity'][k] + \
                       pulp.lpSum(buildcapa[j][t-1] for j in range(K)) * data['inputone'][k][j], \
                       f"Capacity_Industry_{k}_Year_{t}"
        
    # Demand constraint
    for t in range(1, T):
        problem += produce[k][t] >= data['demand'][k], f"Demand_Industry_{k}_Year_{t}"

# Objective function: Maximize the total manpower requirement over five years
total_manpower = pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                             for k in range(K) for t in range(T))
problem += total_manpower, "Total_Manpower"

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