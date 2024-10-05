import pulp

# Data input
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

# Unpacking data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define LP problem
problem = pulp.LpProblem("Investor_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat=pulp.LpContinuous) for i in range(N)]

# Objective function: Maximize expected future value of the portfolio
future_value = pulp.lpSum((bought[i] - sell[i]) * futurePrice[i] for i in range(N))
problem += future_value

# Constraints: Raise required net amount K
money_raised = pulp.lpSum(sell[i] * currentPrice[i] for i in range(N))
transaction_costs = pulp.lpSum(sell[i] * currentPrice[i] * transactionRate for i in range(N))
capital_gains = pulp.lpSum(sell[i] * (currentPrice[i] - buyPrice[i]) for i in range(N))
taxes_on_gains = taxRate * capital_gains

problem += (money_raised - transaction_costs - taxes_on_gains >= K), "NetAmountRequirement"

# Solve the problem
problem.solve()

# Output results
sell_values = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')