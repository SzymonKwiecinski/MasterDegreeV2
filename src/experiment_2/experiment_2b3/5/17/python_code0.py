import pulp

# Parse the data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Future_Portfolio_Value", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective: maximize expected future value of the portfolio
future_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += future_value

# Constraint: raise at least K amount after costs and taxes
# Net proceeds from selling stock i = sell_i * currentPrice_i * (1 - transactionRate)
# Net capital gains from selling stock i = max(0, (currentPrice_i - buyPrice_i) * sell_i)
net_proceeds = pulp.lpSum(sell[i] * current_price[i] * (1 - transaction_rate) for i in range(N))
capital_gains = pulp.lpSum(pulp.lpSum((current_price[i] - buy_price[i]) * sell[i] for i in range(N) if current_price[i] > buy_price[i]))
net_capital_gains = capital_gains * (1 - tax_rate)

# Required to raise at least K amount
problem += (net_proceeds - net_capital_gains) >= K

# Solve the problem
problem.solve()

# Prepare the output
sell_shares = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_shares
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')