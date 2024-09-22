import pulp
import json

# Given data
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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

# Objective function
net_income = pulp.lpSum([(data['Price'][i] * (1 - data['InvestPercentage'][i]) * x[i]) for i in range(data['P'])]) - (data['UpgradeCost'] * u)
problem += net_income

# Constraints
# Cash availability constraint
problem += (pulp.lpSum([data['Cost'][i] * x[i] for i in range(data['P'])]) + (data['UpgradeCost'] * u) <= data['Cash']), "Cash_Constraint")

# Machine hours constraint
problem += (pulp.lpSum([data['Hour'][i] * x[i] for i in range(data['P'])]) <= (data['AvailableHours'] + data['UpgradeHours'] * u)), "Machine_Hours_Constraint")

# Solve the problem
problem.solve()

# Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')