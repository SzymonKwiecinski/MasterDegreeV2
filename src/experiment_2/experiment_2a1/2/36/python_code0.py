import pulp
import json

data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}

# Extracting data from the JSON format
alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and metals
K = len(prices)
M = len(targets)

# Create the LP problem
problem = pulp.LpProblem("Alloy_Optimization", pulp.LpMinimize)

# Define decision variables for the amounts of each alloy
amounts = pulp.LpVariable.dicts("Amount", range(K), lowBound=0)

# Objective function: minimize total cost of alloys
problem += pulp.lpSum(prices[k] * amounts[k] for k in range(K)), "Total_Cost"

# Constraints for the total amount of each metal
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amounts[k] for k in range(K)) == targets[m], f"Metal_{m}_Requirement"

# Constraint for total alloy weight
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total_Alloy_Weight"

# Solve the problem
problem.solve()

# Prepare the output
amounts_solution = [amounts[k].varValue for k in range(K)]

# Print the outputs
print(json.dumps({"amount": amounts_solution}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')