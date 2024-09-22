import pulp
import json

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
        'profit': [30, 20, 40, 25, 10], 
        'capacity': [700, 1000]}

# Parameters
K = len(data['profit'])  # number of parts
S = len(data['time'][0])  # number of shops

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("Quantity", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Shop_{s+1}"

# Solve the problem
problem.solve()

# Output the results
result = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')