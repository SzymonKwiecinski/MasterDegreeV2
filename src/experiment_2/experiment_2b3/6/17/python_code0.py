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

# Parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100.0
tax_rate = data['TaxRate'] / 100.0
K = data['K']

# Define the linear programming problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f"sell_{i}", 0, bought[i]) for i in range(N)]

# Objective function: Maximize future portfolio value
problem += pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N)), "Maximize_Future_Value"

# Constraint: Raise at least K after transaction costs and taxes
problem += pulp.lpSum(
    (current_price[i] * sell[i] - 
     tax_rate * (current_price[i] - buy_price[i]) * sell[i] - 
     transaction_rate * current_price[i] * sell[i]) for i in range(N)
) >= K, "Raise_Amount_K"

# Solve the problem
problem.solve()

# Extract the results
sell_values = [pulp.value(sell[i]) for i in range(N)]

# Output format
output = {
    "sell": sell_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')