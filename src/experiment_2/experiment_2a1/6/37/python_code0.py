import pulp
import json

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

# Number of parts and shops
K = len(data['profit'])
S = len(data['capacity'])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: quantity of each spare part
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints: Each shop's capacity
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_Shop_{s+1}"

# Solve the problem
problem.solve()

# Output the quantities
result = {"quantity": [quantity[k].varValue for k in range(K)]}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')