import pulp

# Data from provided JSON format
data = {
    'alloy_quant': 1000, 
    'target': [300, 700], 
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 
    'price': [5, 4, 3, 2, 1.5]
}

# Constants
K = len(data['price'])  # number of alloys
M = len(data['target'])  # number of components
AlloyQuantity = data['alloy_quant']
Target = data['target']
Ratio = data['ratio']
Price = data['price']

# Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Total alloy quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) == AlloyQuantity, "Total_Alloy_Quantity"

# Target component constraints
for m in range(M):
    problem += pulp.lpSum(Ratio[k][m] * x[k] for k in range(K)) >= Target[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')