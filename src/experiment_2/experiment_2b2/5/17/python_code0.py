import pulp

# Given data
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

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective function: Maximize expected future portfolio value
objective = pulp.lpSum([(bought[i] - sell_vars[i]) * future_price[i] for i in range(N)])
problem += objective

# Constraints
net_amount_raised = pulp.lpSum([
    sell_vars[i] * current_price[i] * (1 - transaction_rate) 
    - (sell_vars[i] * (current_price[i] - buy_price[i]) * tax_rate) 
    for i in range(N)
])

problem += (net_amount_raised >= K, "Money_Raised_Constraint")

# Solve the problem
problem.solve()

# Extract results
sell = [sell_vars[i].varValue for i in range(N)]

# Output result
result = {
    "sell": sell
}
print(result)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')