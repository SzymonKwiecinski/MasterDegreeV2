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

# Variables
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

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective Function
future_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += future_value

# Constraints
net_proceeds = pulp.lpSum(sell[i] * current_price[i] for i in range(N))
transaction_costs = pulp.lpSum(sell[i] * current_price[i] * transaction_rate for i in range(N))
capital_gains = pulp.lpSum(sell[i] * (current_price[i] - buy_price[i]) for i in range(N))
taxes = capital_gains * tax_rate

problem += (net_proceeds - transaction_costs - taxes >= K)

# Solve
problem.solve()

# Output Solution
sell_output = [sell[i].varValue for i in range(N)]

print({
    "sell": sell_output,
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')