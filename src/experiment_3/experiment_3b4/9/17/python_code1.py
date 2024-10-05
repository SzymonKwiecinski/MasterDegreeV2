import pulp

# Data from the problem
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function
objective = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += objective

# Constraint: Net amount of money raised must be at least K
net_money_raised = pulp.lpSum(
    sell[i] * current_price[i] * (1 - transaction_rate) - 
    (sell[i] * current_price[i] - sell[i] * buy_price[i]) * tax_rate for i in range(N)
)
problem += net_money_raised >= K

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')