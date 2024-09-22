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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function
profit = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += profit, "Total_Profit"

# Constraints
problem += (pulp.lpSum(sell[i] * current_price[i] * (1 - transaction_rate) -
                       ((sell[i] * current_price[i] - sell[i] * buy_price[i]) * (tax_rate / 100))
                       for i in range(N)) >= K), "Minimum_Value_Constraint"

# Upper bound constraints
for i in range(N):
    problem += (sell[i] <= bought[i], f"Upper_Bound_Sell_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')