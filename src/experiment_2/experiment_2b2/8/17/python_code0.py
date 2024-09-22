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

# Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, bought[i]) for i in range(N)]

# Objective function
problem += pulp.lpSum([
    future_price[i] * (bought[i] - sell[i]) for i in range(N)
]), "Maximize Future Value"

# Constraint for net money raised
net_money_constraints = []
for i in range(N):
    sell_value = sell[i] * current_price[i]
    transaction_cost = sell_value * transaction_rate
    capital_gains = sell[i] * (current_price[i] - buy_price[i])
    tax_on_gains = capital_gains * tax_rate
    net_proceeds = sell_value - transaction_cost - tax_on_gains
    net_money_constraints.append(net_proceeds)

problem += pulp.lpSum(net_money_constraints) >= K, "Net Money Constraint"

# Solve the problem
problem.solve()

# Output the result
sell_result = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')