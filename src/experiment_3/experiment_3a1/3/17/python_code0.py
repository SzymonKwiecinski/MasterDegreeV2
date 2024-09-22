import pulp

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

# Problem definition
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("Sell", range(data['N']), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N'])), "Total_Expected_Value"

# Constraints
problem += pulp.lpSum((1 - data['TransactionRate'] / 100) * data['CurrentPrice'][i] * sell[i] - 
                      (data['TaxRate'] / 100) * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i] 
                      for i in range(data['N'])) >= data['K'], "Capital_Gains_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')