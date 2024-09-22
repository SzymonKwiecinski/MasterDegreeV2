import pulp

# Data from provided JSON
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

# Create the LP problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

# Objective function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N'])), "Objective"

# Constraints
problem += (pulp.lpSum((data['CurrentPrice'][i] * sell[i]) * (1 - data['TransactionRate'] / 100) - 
                       (data['BuyPrice'][i] * sell[i]) * (data['TaxRate'] / 100) 
                       for i in range(data['N'])) >= data['K'], "Net_Amount_Constraint")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')