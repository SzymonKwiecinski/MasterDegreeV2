import pulp

# Data from JSON
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

# Create the problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0) for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Objective Function
net_income = pulp.lpSum([(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * production[i] for i in range(data['P'])])
problem += net_income, "Total_Net_Income"

# Constraints
# Machine Hours Constraint
problem += (pulp.lpSum(data['Hour'][i] * production[i] for i in range(data['P'])) <= data['AvailableHours'] + upgrade * data['UpgradeHours'], "Machine_Hours_Constraint")

# Cash Availability Constraint
problem += (pulp.lpSum((data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * production[i] for i in range(data['P'])) <= data['Cash'] + upgrade * data['UpgradeCost'], "Cash_Availability_Constraint")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')