import pulp
import json

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

# Extracting data from the input
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')