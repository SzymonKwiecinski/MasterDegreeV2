import pulp
import json

# Input data
data = {'alloy_quant': 1000, 
        'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Extracting data from the input
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the LP problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables for the amount of each alloy
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: minimize the total cost
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Constraints
# Total amount of alloys used must equal alloy_quant
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Amount"

# Constraints for each metal
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) == target[m], f"Metal_Constraint_{m}"

# Solve the problem
problem.solve()

# Prepare the output
output = {"amount": [amount[k].varValue for k in range(K)]}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')