import pulp

# Data from the JSON
data = {'alloy_quant': 1000, 'target': [300, 700], 
        'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
        'price': [5, 4, 3, 2, 1.5]}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of materials
M = len(target)  # Number of components in alloy

# Create a LP problem instance
problem = pulp.LpProblem("Alloy_Mix_Optimization", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints

# Total alloy quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant, "Total_Alloy_Quantity"

# Composition constraints for each component 'm'
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == target[m], f"Composition_Target_{m}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')