import pulp

# Data from the JSON format
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: amount of each good to produce
amounts = pulp.LpVariable.dicts("Amount", range(data['M']), lowBound=0)

# Objective function: Maximize total revenue
problem += pulp.lpSum(data['Prices'][j] * amounts[j] for j in range(data['M'])), "Total_Revenue"

# Constraints for each raw material
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][k][i] * amounts[k] for k in range(data['M'])) <= data['Available'][i]), f"RawMaterial_{i}_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')