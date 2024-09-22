import pulp
import json

# Input data in JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extract data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables: the number of shares to sell for each stock
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function: maximize the expected future value of the portfolio
expected_future_value = pulp.lpSum((future_price[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_future_value

# Constraints: The amount raised after accounting for transaction costs and taxes must be at least K
total_revenue = pulp.lpSum((current_price[i] * sell[i]) for i in range(N))
total_transaction_cost = transaction_rate * total_revenue
total_capital_gains = pulp.lpSum(((current_price[i] - buy_price[i]) * sell[i]) for i in range(N))
total_tax = tax_rate * total_capital_gains

net_amount_raised = total_revenue - total_transaction_cost - total_tax
problem += (net_amount_raised >= K, "Minimum_Money_Raised")

# Solve the problem
problem.solve()

# Output results
sell_shares = [sell[i].varValue for i in range(N)]
output = {"sell": sell_shares}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')