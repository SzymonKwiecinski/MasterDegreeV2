import pulp

# Data from JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quantity = data['alloy_quant']
target_components = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # Number of alloys
M = len(target_components)  # Number of target components

# Create a linear programming problem
problem = pulp.LpProblem("Alloy_Production_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("AlloyAmount", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Total alloy quantity produced must equal AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Alloy_Quantity"

# Constraints for target components
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= target_components[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')