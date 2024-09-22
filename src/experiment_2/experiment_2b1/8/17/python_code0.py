import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Sell_Shares", pulp.LpMaximize)

# Decision variables: number of shares to sell for each stock
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None)

# Objective Function: Maximize the expected portfolio value for next year
expected_value = pulp.lpSum(((future_price[i] * (1 - transaction_rate) - 
                               buy_price[i]) * (1 - tax_rate)) * sell[i]
                              for i in range(N))
problem += expected_value, "Expected_Value"

# Constraints: The net amount after selling must meet or exceed K
net_amount = pulp.lpSum((current_price[i] * (1 - transaction_rate) - 
                          buy_price[i]) * (1 - tax_rate) * sell[i]
                         for i in range(N))
problem += net_amount >= K, "Net_Amount_Requirement"

# Solve the problem
problem.solve()

# Output the result
sell_shares = [sell[i].varValue for i in range(N)]
output = {"sell": sell_shares}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')