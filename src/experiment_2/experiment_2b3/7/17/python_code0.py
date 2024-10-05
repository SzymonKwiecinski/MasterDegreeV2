import pulp

# Input data
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
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective: Maximize the expected value of the portfolio next year
expected_value_next_year = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += expected_value_next_year

# Constraints
net_amounts = [(sell[i] * current_price[i] * (1 - transaction_rate)) - 
               ((sell[i] * current_price[i] - sell[i] * buy_price[i]) * tax_rate) for i in range(N)]
problem += pulp.lpSum(net_amounts) >= K

# Solve the problem
problem.solve()

# Gather the results
sell_result = [sell[i].varValue for i in range(N)]

output = {
    "sell": sell_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')