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

# Variables
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective Function
objective = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += objective

# Constraints
constraint = pulp.lpSum(
    sell[i] * current_price[i] * (1 - transaction_rate / 100) - 
    (sell[i] * (current_price[i] - buy_price[i]) * tax_rate / 100)
    for i in range(N)
) >= K

problem += constraint

# Solve the problem
problem.solve()

# Print the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for i in range(N):
    print(f"Sell Amount of Asset {i+1}: {pulp.value(sell[i])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')