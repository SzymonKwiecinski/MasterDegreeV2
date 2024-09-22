import pulp
import json

data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Extracting data from JSON
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)  # number of alloys
M = len(target)  # number of metals

# Create the LP problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Decision variables: amount of each alloy
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints to ensure the alloy composition is correct
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_{m+1}_Constraint"

# Constraint for total alloy quantity
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Alloy_Quantity_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
amount_solution = [amount[k].varValue for k in range(K)]
output = {
    "amount": amount_solution
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')