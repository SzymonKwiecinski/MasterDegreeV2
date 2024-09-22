import pulp
import json

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

N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables: number of shares to sell for each stock
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

# Objective function: maximize the expected future value of the portfolio
expected_future_value = sum(
    (FuturePrice[i] * (Bought[i] - sell[i])) for i in range(N)
)
problem += expected_future_value

# Constraints
# The amount raised from selling shares minus costs and taxes should be at least K
total_amount_raised = sum(
    (CurrentPrice[i] * sell[i] * (1 - transactionRate) * (1 - taxRate)) -
    (BuyPrice[i] * sell[i] * (1 - taxRate)) for i in range(N)
)

problem += total_amount_raised >= K, "AmountRaisedConstraint"

# Upper limit constraints (cannot sell more than owned)
for i in range(N):
    problem += sell[i] <= Bought[i], f"MaxSellConstraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
sell_amounts = [sell[i].varValue for i in range(N)]
output = {
    "sell": sell_amounts
}

# Output the result
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')