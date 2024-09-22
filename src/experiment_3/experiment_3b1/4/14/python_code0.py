import pulp
import json

# Data from the provided JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 
        'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 
        'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Create the problem variable
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['P']), lowBound=0)  # Production quantities
u = pulp.LpVariable("u", 0, 1, pulp.LpBinary)  # Upgrade decision

# Objective function
problem += pulp.lpSum(
    ((data['Price'][i] - data['Cost'][i]) * x[i] 
    - data['InvestPercentage'][i] * data['Price'][i] * x[i]) 
    for i in range(data['P'])
) - data['UpgradeCost'] * u, "Total_Net_Income"

# Constraints
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * u, "Machine_Capacity"
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'], "Cash_Availability"

# Solve the problem
problem.solve()

# Output the results
net_income = pulp.value(problem.objective)
production = [pulp.value(x[i]) for i in range(data['P'])]
upgrade = pulp.value(u)

print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production Quantities: {production}')
print(f'Upgrade Machine Capacity: {bool(upgrade)}')