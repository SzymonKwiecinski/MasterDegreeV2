import pulp

# Define the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Load data
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
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Define the objective function
problem += pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))

# Define the constraints
# Net money raised after selling
for i in range(N):
    # Money received from selling shares of stock i
    amount_received = sell[i] * current_price[i]
    # Capital gain for stock i
    capital_gain = sell[i] * (current_price[i] - buy_price[i])
    # Transaction cost for stock i
    transaction_cost = amount_received * transaction_rate
    # Tax cost for stock i
    tax_cost = capital_gain * tax_rate
    # Net money after selling
    net_money = amount_received - transaction_cost - tax_cost
    # Add constraint for each stock
    if i == 0:
        net_money_constraint = net_money
    else:
        net_money_constraint += net_money

# Final constraint to ensure the total net money raised is at least K
problem += net_money_constraint >= K

# Solve the problem
problem.solve()

# Gather results
sell_values = [pulp.value(sell[i]) for i in range(N)]

# Output format
output = {
    "sell": sell_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')