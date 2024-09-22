import pulp

# Data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0, # Transaction costs in percentage
    'TaxRate': 15.0, # Tax rate in percentage
    'K': 5000
}

# Set parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100.0 # Convert to decimal
tax_rate = data['TaxRate'] / 100.0 # Convert to decimal
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum(future_price[i] * (bought[i] - sell[i]) for i in range(N)), "Maximize_Expected_Portfolio_Value"

# Constraints
# Constraint 1: Amount raised from selling shares
problem += pulp.lpSum((current_price[i] * sell[i] - transaction_rate * current_price[i] * sell[i] - tax_rate * (current_price[i] - buy_price[i]) * sell[i]) for i in range(N)) >= K, "Raise_Required_Amount"

# Solve the problem
problem.solve()

# Output results
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')