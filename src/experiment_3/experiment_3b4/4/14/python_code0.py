import pulp

# Data
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum((data['Price'][i] * production[i] - 
                         (data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * production[i]) 
                         for i in range(data['P'])) - data['UpgradeCost'] * upgrade
problem += net_income

# Constraints

# Cash constraint
cash_constraint = pulp.lpSum(production[i] * data['Cost'][i] for i in range(data['P'])) <= (
    data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * production[i] for i in range(data['P'])))
problem += cash_constraint

# Machine capacity constraint
machine_capacity_constraint = pulp.lpSum(production[i] * data['Hour'][i] for i in range(data['P'])) <= (
    data['AvailableHours'] + data['UpgradeHours'] * upgrade)
problem += machine_capacity_constraint

# Non-negativity constraints are automatically handled by `lowBound=0` in `LpVariable`.

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')