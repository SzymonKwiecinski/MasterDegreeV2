import pulp
import json

# Data in JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(future_price[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

# Constraints
problem += (pulp.lpSum(((current_price[i] - (transaction_rate / 100) * current_price[i]) * sell[i] - 
                         (tax_rate / 100) * (current_price[i] - buy_price[i]) * sell[i]) 
                        for i in range(N)) >= K, "Net_Money_Raised")

# Constraints for selling shares
for i in range(N):
    problem += sell[i] <= bought[i], f"Max_Sell_Constraint_{i+1}"
    
# Solve the problem
problem.solve()

# Output results
sell_values = [sell[i].varValue for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')