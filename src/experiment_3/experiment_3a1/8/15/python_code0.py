import pulp
import json

# Given data in JSON format
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

# Problem definition
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
o = pulp.LpVariable("o", lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) \
         - (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) + data['OvertimeAssemblyCost'] * o)

problem += profit

# Constraints
# 1. Assembly labor constraint
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint")

# 2. Testing labor constraint
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) 
            <= data['MaxTesting'], "Testing_Labor_Constraint")

# 4. Material cost constraint for discount
C = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discounted_C = C * (1 - data['MaterialDiscount'] / 100)

# Add the material cost constraint if the discount threshold is crossed
problem += (C <= data['DiscountThreshold'] + 1e-5) | (discounted_C <= C)

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')