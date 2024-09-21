import pulp

# Data provided
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

# Define the Linear Program
problem = pulp.LpProblem("Investor's_Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
problem += sum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Constraints
# Non-negativity and cannot sell more than bought constraints
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i]

# Amount raised constraint
raised_amount = sum(
    x[i] * data['CurrentPrice'][i] - 
    x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100 - 
    x[i] * data['CurrentPrice'][i] * data['TransactionRate'] / 100 
    for i in range(data['N'])
)
problem += raised_amount >= data['K']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')