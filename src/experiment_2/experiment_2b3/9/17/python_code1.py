import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Maximize_Future_Portfolio_Value", pulp.LpMaximize)

# Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective Function: Maximize expected future portfolio value
future_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += future_value

# Constraints
net_gain_constraint = pulp.lpSum(
    (sell[i] * current_price[i]) * (1 - transaction_rate) - 
    (pulp.lpSum(sell[i] * (current_price[i] - buy_price[i]) for i in range(N)) * tax_rate) 
    for i in range(N)
) >= K

problem += net_gain_constraint

# Solve
problem.solve()

# Results
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')