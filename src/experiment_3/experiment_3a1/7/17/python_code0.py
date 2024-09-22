import pulp
import json

# Data from the provided JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum(future_price[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

# Constraints
# Total amount raised must be >= K after costs and taxes
problem += (pulp.lpSum((current_price[i] * sell[i]) * (1 - transaction_rate / 100) for i in range(N)) 
                     - pulp.lpSum(((current_price[i] - buy_price[i]) * sell[i]) * (tax_rate / 100) for i in range(N)) >= K, 
                     "Capital_Gains_Constraint")

# Solve the problem
problem.solve()

# Output the results
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')