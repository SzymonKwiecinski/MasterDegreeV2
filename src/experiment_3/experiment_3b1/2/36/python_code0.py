import pulp

# Data from the JSON
data = {
    'alloy_quant': 1000, 
    'target': [300, 700], 
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
# Total weight of the alloys must equal the desired alloy quantity
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Weight"

# For each metal, the total amount must meet the target
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Target_{m+1}"

# Solve the problem
problem.solve()

# Output the results
for k in range(K):
    print(f"Amount of alloy {k + 1}: {amount[k].varValue}")

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')