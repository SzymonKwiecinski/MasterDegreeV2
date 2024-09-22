import pulp
import json

# Input data
data = json.loads('{"alloy_quant": 1000, "target": [300, 700], "ratio": [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], "price": [5, 4, 3, 2, 1.5]}')

# Parameters
A = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

M = len(target)  # Number of metals
K = len(price)   # Number of available alloys

# Define the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint 1: Total weight of the alloys
problem += pulp.lpSum(x[k] for k in range(K)) == A, "Total_Weight"

# Constraints for each metal to meet the target
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) == target[m], f"Metal_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Output the amounts of each alloy to be purchased
amounts = [x[k].varValue for k in range(K)]

print(f'Amounts of each alloy to be purchased: {amounts}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')