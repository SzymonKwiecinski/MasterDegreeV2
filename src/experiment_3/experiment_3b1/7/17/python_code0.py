import pulp

# Data from JSON format
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

# Problem Definition
problem = pulp.LpProblem("Investor_Stock_Selling_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

# Objective Function
profit_from_future = pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N']))
cost_of_selling = pulp.lpSum(data['CurrentPrice'][i] * sell[i] * (1 + data['TransactionRate'] / 100) for i in range(data['N']))
tax_cost = pulp.lpSum(((data['CurrentPrice'][i] - data['BuyPrice'][i]) / data['CurrentPrice'][i]) * data['TaxRate'] / 100 * sell[i] for i in range(data['N']))

problem += profit_from_future - cost_of_selling - tax_cost, "Total_Profit"

# Constraints
net_proceeds = pulp.lpSum((data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100)) - 
                          ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100) * sell[i] 
                          for i in range(data['N']))

problem += net_proceeds >= data['K'], "Net_Proceeds_Constraint"

# Constraints to limit sells to the amount bought
for i in range(data['N']):
    problem += sell[i] <= data['Bought'][i], f"Limit_Sell_{i}"
    
# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')