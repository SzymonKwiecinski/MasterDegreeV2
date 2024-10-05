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

# Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Initializing the problem
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function
problem += pulp.lpSum((future_price[i] * bought[i] - x[i] * future_price[i]) for i in range(N))

# Constraints
problem += pulp.lpSum(
    [x[i] * current_price[i] * (1 - transaction_rate / 100) - 
     x[i] * buy_price[i] * (tax_rate / 100) for i in range(N)]
) >= K

# Solve the problem
problem.solve()

# Output the solution
sell = [x[i].varValue for i in range(N)]
print(f'sell = {sell}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')