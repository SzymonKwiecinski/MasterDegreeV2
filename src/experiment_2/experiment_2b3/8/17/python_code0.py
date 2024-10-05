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

# Extract data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Initialize problem
problem = pulp.LpProblem("Maximize_Future_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, bought[i], cat='Continuous') for i in range(N)]

# Objective function: maximize the future value of the remaining shares
future_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += future_value

# Constraint: Net money raised should be at least K
net_money_raised = pulp.lpSum(
    (sell[i] * current_price[i] * (1 - transaction_rate) - 
    pulp.lpSum(sell[i] * (current_price[i] - buy_price[i]) * tax_rate if current_price[i] > buy_price[i] else 0))
    for i in range(N)
)
problem += (net_money_raised >= K, "Net_Money_Raised_Constraint")

# Solve the problem
problem.solve()

# Prepare output
sell_shares = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_shares
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')