import pulp

# Data from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extracting the parameters
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
K = len(profit)  # Number of spare parts
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Production quantities

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints for each shop
S = len(capacity)  # Number of shops
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Shop_Capacity_{s+1}"

# Solve the problem
problem.solve()

# Output the quantities produced and the objective value
quantities = [x[k].varValue for k in range(K)]
print(f'quantities = {quantities}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')