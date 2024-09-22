import pulp
import json

# Given data in JSON format
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

# Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Defining the problem
K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Defining decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints for each shop
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s]), f"Shop_Capacity_{s}"

# Solve the problem
problem.solve()

# Output the results
quantities = [x[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{"quantity": {quantities}}}')