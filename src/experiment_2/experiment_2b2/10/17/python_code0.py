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

# Extract data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Variables
sell = [pulp.LpVariable(f'sell_{i}', 0, bought[i]) for i in range(N)]

# Objective Function: Maximize expected future portfolio value
problem += pulp.lpSum([(bought[i] - sell[i]) * future_price[i] for i in range(N)])

# Constraint: Ensure the net amount raised meets the target K
problem += pulp.lpSum([
    (sell[i] * current_price[i]) * (1 - transaction_rate / 100) - 
    ((sell[i] * current_price[i] - sell[i] * buy_price[i]) * (tax_rate / 100))
    for i in range(N)
]) >= K

# Solve the problem
problem.solve()

# Output results
sell_result = [pulp.value(sell[i]) for i in range(N)]

output = {"sell": sell_result}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')