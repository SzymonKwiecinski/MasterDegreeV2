import pulp
import json

# Input data in JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

# Extracting data from the input
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and number of shops
K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints for each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Shop_Capacity_{s+1}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')