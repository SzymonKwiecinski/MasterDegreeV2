import pulp

# Data based on the json input
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,  # as percentage
    'TaxRate': 15.0,  # as percentage
    'K': 5000
}

# Parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Stock_Selling_Decision", pulp.LpMaximize)

# Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum(future_price[i] * (bought[i] - sell_vars[i]) for i in range(N)), "Maximize_Future_Portfolio_Value"

# Constraints
# Constraint 1: The net amount raised by selling the shares must be at least K
problem += pulp.lpSum(
    current_price[i] * sell_vars[i] * (1 - transaction_rate / 100) - 
    (sell_vars[i] * buy_price[i] * tax_rate / 100)
    for i in range(N)
) >= K, "Net_Amount_Raised"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')