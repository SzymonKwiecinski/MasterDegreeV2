import pulp
import json

# Data input
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
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function: maximize expected future portfolio value
expected_future_value = pulp.lpSum(
    (FuturePrice[i] * (Bought[i] - sell[i]) for i in range(N))
)

# Add the objective to the problem
problem += expected_future_value

# Constraint: the amount raised must be at least K net of costs
amount_raised = pulp.lpSum(
    (CurrentPrice[i] * sell[i] * (1 - transaction_rate) - 
     (CurrentPrice[i] * sell[i] - BuyPrice[i] * sell[i]) * tax_rate 
     for i in range(N))
)

problem += amount_raised >= K

# Constraint: cannot sell more than bought
for i in range(N):
    problem += sell[i] <= Bought[i]

# Solve the problem
problem.solve()

# Prepare output
sell_shares = [sell[i].varValue for i in range(N)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the number of shares to sell
output = {"sell": sell_shares}
print(output)