import pulp

# Data
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

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("shares_to_sell", range(data['N']), lowBound=0)

# Objective Function
problem += pulp.lpSum([(data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])]), "Total_Expected_Future_Value"

# Constraints
# Constraint 1: Amount raised is at least K, net of transaction costs and taxes
problem += pulp.lpSum([(1 - data['TransactionRate'] / 100) * data['CurrentPrice'][i] * x[i] -
                        (data['TaxRate'] / 100) * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * x[i]
                        for i in range(data['N'])]) >= data['K'], "Minimum_Amount_Raised"

# Constraint 2: Do not sell more shares than owned
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i], f"Max_Shares_Sold_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')