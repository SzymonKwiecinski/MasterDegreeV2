import pulp
import json

data = {'N': 3, 'Bought': [100, 150, 80], 
        'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 
        'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 
        'TaxRate': 15.0, 
        'K': 5000}

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100.0  # converting percentage to decimal
taxRate = data['TaxRate'] / 100.0  # converting percentage to decimal
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

# Define the objective function
portfolio_value_next_year = sum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N))
problem += portfolio_value_next_year, "Maximize_Portfolio_Value_Next_Year"

# Define constraints for raising K net of capital gains and transaction costs
net_amount = sum((currentPrice[i] * sell[i] * (1 - transactionRate) - 
                  (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate) 
                  for i in range(N))

problem += net_amount >= K, "Raise_Required_Amount"

# Solve the problem
problem.solve()

# Collect the results
sell_shares = [sell[i].varValue for i in range(N)]
output = {"sell": sell_shares}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')