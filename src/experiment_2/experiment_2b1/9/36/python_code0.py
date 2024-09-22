import json
import pulp

# Load data
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Problem definition
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Variables
K = len(data['price'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(data['price'][k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(amount[k] for k in range(K)) == data['alloy_quant'], "Total_Alloy_Quantity"

M = len(data['target'])
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * amount[k] for k in range(K)) == data['target'][m], f"Metal_{m+1}_Constraint"

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "amount": [amount[k].varValue for k in range(K)]
}

# Output the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')