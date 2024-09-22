import pulp

# Provided data
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

# Extracting data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective Function: Maximize expected value of portfolio next year
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N))

# Constraints
# Net amount requirement
problem += pulp.lpSum(
    (currentPrice[i] * sell[i] * (1 - transactionRate / 100) -
    (currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100))
    for i in range(N)
) >= K

# Solve the problem
problem.solve()

# Extract the results
sell_values = [pulp.value(sell[i]) for i in range(N)]

# Output the results
print(f'sell: {sell_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')