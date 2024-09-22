import pulp

# Define the data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000,
}

# Extract data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("InvestorPortfolio", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum([futurePrice[i] * (bought[i] - sell[i]) for i in range(N)])

# Constraint 1: Net amount raised from selling shares
problem += pulp.lpSum([
    (currentPrice[i] * sell[i]) * (1 - transactionRate / 100) - ((currentPrice[i] - buyPrice[i]) * sell[i]) * (taxRate / 100)
    for i in range(N)
]) >= K

# Solve the problem
problem.solve()

# Output the solution
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')