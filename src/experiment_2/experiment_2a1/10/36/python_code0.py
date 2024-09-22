import pulp
import json

# Input data
data = json.loads("{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}")

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of alloys
M = len(target)  # Number of metals

# Problem definition
problem = pulp.LpProblem("Alloy_Combination_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Alloy_Weight"
for m in range(M):
    problem += pulp.lpSum(amount[k] * ratios[k][m] for k in range(K)) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Output results
amount_solution = [amount[k].varValue for k in range(K)]
print(json.dumps({"amount": amount_solution}))

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')