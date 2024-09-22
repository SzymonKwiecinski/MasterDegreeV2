import pulp
import json

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts (K) and shops (S)
K = len(profit)
S = len(capacity)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for quantities of each spare part
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

# Constraints for each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output results
quantity_values = [quantity[k].varValue for k in range(K)]
output = {"quantity": quantity_values}
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')