import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100  # converting percentage to decimal
taxRate = data['TaxRate'] / 100  # converting percentage to decimal
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None)

# Objective function: Maximize the future value of the portfolio after selling the shares
objective = pulp.lpSum((FuturePrice[i] * (Bought[i] - sell[i])) for i in range(N))
problem += objective

# Constraints
# Net money raised after selling shares must be at least K
net_money = pulp.lpSum((CurrentPrice[i] * sell[i] * (1 - transactionRate) - 
                         (CurrentPrice[i] * sell[i] - BuyPrice[i] * sell[i]) * taxRate) 
                        for i in range(N))
problem += net_money >= K

# Limit the amount of shares sold to the amount bought
for i in range(N):
    problem += sell[i] <= Bought[i]

# Solve the problem
problem.solve()

# Prepare the output
sell_output = [sell[i].varValue for i in range(N)]
output = {"sell": sell_output}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')