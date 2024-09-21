import pulp

# Data
alloy_quant = 1000
target = [300, 700]
ratio = [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]]
price = [5, 4, 3, 2, 1.5]

# Number of alloys and components
K = len(price)  # Number of alloys
M = len(target) # Number of components

# Create the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of each alloy

# Objective function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints
# Total quantity of alloys produced
problem += pulp.lpSum([x[k] for k in range(K)]) == alloy_quant, "Total_Alloy_Quantity"

# Constraints for each target component
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * x[k] for k in range(K)]) >= target[m], f"Component_{m+1}_Requirement"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')