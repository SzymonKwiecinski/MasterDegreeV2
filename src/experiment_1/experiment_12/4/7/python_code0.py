import pulp

# Extracting data
data = {
    'N': 3, 
    'Bought': [100, 150, 80], 
    'BuyPrice': [50, 40, 30], 
    'CurrentPrice': [60, 35, 32], 
    'FuturePrice': [65, 44, 34], 
    'TransactionRate': 1.0, 
    'TaxRate': 15.0, 
    'K': 5000
}

# Define the problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=data['Bought'][i], cat='Continuous') for i in range(data['N'])]

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Constraints
# Non-negativity and can’t sell more than bought constraints are covered by the variable bounds

# Amount raised constraint
problem += pulp.lpSum(
    x[i] * data['CurrentPrice'][i] - 
    x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100 - 
    x[i] * data['CurrentPrice'][i] * data['TransactionRate'] / 100
    for i in range(data['N'])
) >= data['K']

# Solve the problem
problem.solve()

# Print the results
print(f"Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>")
for i in range(data['N']):
    print(f"Shares sold for stock {i+1}: {x[i].varValue}")