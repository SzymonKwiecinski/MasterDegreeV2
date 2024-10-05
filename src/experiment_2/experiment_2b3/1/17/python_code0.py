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

# Unpack Data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Investor_Problem", pulp.LpMaximize)

# Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Constraints
transaction_costs = [sell[i] * current_price[i] * transaction_rate for i in range(N)]
capital_gains = [sell[i] * (current_price[i] - buy_price[i]) for i in range(N)]
taxes = [capital_gains[i] * tax_rate for i in range(N)]

net_proceeds = [sell[i] * current_price[i] - transaction_costs[i] - taxes[i] for i in range(N)]

# Adding constraint to ensure at least K is raised
problem += pulp.lpSum(net_proceeds) >= K, "Net_Proceeds"

# Objective: Maximize expected value of portfolio next year
future_value = [bought[i] * future_price[i] - sell[i] * future_price[i] for i in range(N)]
problem += pulp.lpSum(future_value), "Maximize_Future_Value"

# Solve the problem
problem.solve()

# Result
result_sell = [sell[i].varValue for i in range(N)]
result = {"sell": result_sell}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')