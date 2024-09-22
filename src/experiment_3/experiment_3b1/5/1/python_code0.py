import pulp

# Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], 
                     [0, 5, 2, 1, 0], 
                     [1, 0, 0, 5, 3], 
                     [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Production_Revenue", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(data['M']), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M'])), "Total_Revenue"

# Constraints
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][i][j] * x[j] for j in range(data['M'])) <= data['Available'][i]), f"Raw_Material_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the results
produced_amounts = [x[j].varValue for j in range(data['M'])]
print(f'{{"amount": {produced_amounts}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')