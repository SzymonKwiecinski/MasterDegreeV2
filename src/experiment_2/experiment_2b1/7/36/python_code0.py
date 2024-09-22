import pulp
import json

# Data input
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], 
                  [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

# Problem parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of alloys and metals
K = len(price)
M = len(target)

# Create the linear programming problem
problem = pulp.LpProblem("Alloy_Mixture_Problem", pulp.LpMinimize)

# Decision variables for the amount of each alloy
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum([amount[k] * price[k] for k in range(K)])

# Constraints
# Total weight of alloys must equal to the total alloy quantity
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant, "Total_Weight"

# Constraints for each metal target
for m in range(M):
    problem += pulp.lpSum([amount[k] * ratio[k][m] for k in range(K)]) == target[m], f"Metal_{m+1}_Target"

# Solve the problem
problem.solve()

# Output the results
amounts = [pulp.value(amount[k]) for k in range(K)]
output = {"amount": amounts}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')