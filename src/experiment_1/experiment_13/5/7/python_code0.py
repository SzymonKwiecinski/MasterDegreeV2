import pulp

# Data extracted from the given JSON format
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

# Create the problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])), "Objective"

# Constraints
# Non-negativity constraint and cannot sell more than bought is handled by variable definition

# Amount raised constraint
problem += (pulp.lpSum(
    x[i] * data['CurrentPrice'][i] - 
    x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * (data['TaxRate'] / 100) - 
    x[i] * data['CurrentPrice'][i] * (data['TransactionRate'] / 100) 
    for i in range(data['N'])
) >= data['K']), "Amount_Raised_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')