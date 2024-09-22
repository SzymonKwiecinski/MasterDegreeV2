import pulp
import json

# Data
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, upBound=data['NumCranes'], cat='Integer')
held = pulp.LpVariable.dicts("held", range(data['T'] + 1), lowBound=0)

# Objective Function
total_cost = pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * held[t + 1] + data['CraneCost'] * crane[t] for t in range(data['T']))
problem += total_cost

# Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unload_Capacity_Constraint_{t}"
    if t > 0:
        problem += held[t] == held[t - 1] + amount[t] - data['Demands'][t], f"Demand_Balance_Constraint_{t}"
    else:
        problem += held[0] == data['InitContainer'], f"Initial_Container_Constraint"

for t in range(data['T']):
    problem += held[t + 1] <= data['MaxContainer'], f"Max_Container_Constraint_{t}"
    problem += held[t + 1] >= 0, f"Non_Negative_Held_Constraint_{t}"
    if t > 0:
        problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t] - held[t], f"Crane_Capacity_Constraint_{t}"
        
# Final constraint
problem += held[data['T']] == 0, "Final_Held_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')