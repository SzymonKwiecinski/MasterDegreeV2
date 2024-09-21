import pulp

# Data
data = {
    'N': 3,
    'M': 2,
    'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    'DesiredIlluminations': [14, 3, 12]
}

# Problem Definition
problem = pulp.LpProblem("Minimize_Illumination_Error", pulp.LpMinimize)

# Decision Variables
P = pulp.LpVariable.dicts("LampPower", range(data['M']), lowBound=0)  # Lamp powers
E = pulp.LpVariable.dicts("AbsoluteError", range(data['N']), lowBound=0)  # Absolute errors

# Objective Function
problem += pulp.lpSum(E[i] for i in range(data['N'])), "Total_Absolute_Error"

# Constraints
for i in range(data['N']):
    # Constraint for upper bound of error
    problem += (pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) - data['DesiredIlluminations'][i] <= E[i]), f"UpperBoundError_{i}"
    # Constraint for lower bound of error
    problem += (data['DesiredIlluminations'][i] - pulp.lpSum(data['Coefficients'][i][j] * P[j] for j in range(data['M'])) <= E[i]), f"LowerBoundError_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')