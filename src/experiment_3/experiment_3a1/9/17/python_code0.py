import pulp

# Data extracted from JSON format
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

# Problem definition
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) - sell[i] * data['CurrentPrice'][i] for i in range(data['N'])])
problem += profit

# Constraints
net_amount = pulp.lpSum([
    (sell[i] * data['CurrentPrice'][i] -
     data['TransactionRate'] * (sell[i] * data['CurrentPrice'][i]) -
     data['TaxRate'] / 100 * ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i]))
    for i in range(data['N'])
])

problem += net_amount >= data['K'], "NetAmountConstraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')