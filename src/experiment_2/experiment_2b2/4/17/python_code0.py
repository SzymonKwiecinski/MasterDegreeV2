import pulp

# Data from JSON
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

# Extract data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create a LP problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function: Maximize future portfolio value
problem += pulp.lpSum((bought[i] - sell[i]) * futurePrice[i] for i in range(N))

# Constraint: Ensure the net cash raised is at least K
net_cash_raised = pulp.lpSum(
    sell[i] * currentPrice[i] * (1 - transactionRate) 
    - (sell[i] * (currentPrice[i] - buyPrice[i])) * taxRate
    for i in range(N)
)
problem += net_cash_raised >= K

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "sell": [pulp.value(sell[i]) for i in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')