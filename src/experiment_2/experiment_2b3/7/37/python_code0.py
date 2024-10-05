import pulp

# Input Data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

time = data['time']
profit = data['profit']
capacity = data['capacity']

K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define the decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints: Capacity of each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Output the results
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')