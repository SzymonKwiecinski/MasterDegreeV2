import pulp

# Data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100.0
tax_rate = data['TaxRate'] / 100.0
K = data['K']

# Problem
problem = pulp.LpProblem("Investor_Portfolio", pulp.LpMaximize)

# Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective: Maximize expected future value of portfolio
expected_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += expected_value

# Constraints: Raise at least K amount of money
net_sale_revenue = [
    (sell[i] * current_price[i]) * (1 - transaction_rate) - (sell[i] * (current_price[i] - buy_price[i])) * tax_rate
    for i in range(N)
]
problem += pulp.lpSum(net_sale_revenue) >= K

# Solve
problem.solve()

# Output
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')