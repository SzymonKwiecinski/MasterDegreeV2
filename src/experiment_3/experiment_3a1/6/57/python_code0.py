import pulp
import json

# Data input in JSON format
data = json.loads("""
{
    "T": 4,
    "Demands": [450, 700, 500, 750],
    "UnloadCosts": [75, 100, 105, 130],
    "UnloadCapacity": [800, 500, 450, 700],
    "HoldingCost": 20,
    "MaxContainer": 500,
    "InitContainer": 200,
    "NumCranes": 4,
    "CraneCapacity": 200,
    "CraneCost": 1000
}
""")

# Model
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')
hold = pulp.LpVariable.dicts("hold", range(1, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t - 1] * amount[t] + 
                       data['HoldingCost'] * hold[t] + 
                       data['CraneCost'] * crane[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Hold container equation
    if t == 1:
        problem += hold[t] == data['InitContainer'] + amount[t] - data['Demands'][t - 1]
    else:
        problem += hold[t] == hold[t - 1] + amount[t] - data['Demands'][t - 1]

    # Maximum container constraint
    problem += hold[t] <= data['MaxContainer']
    
    # Unload capacity constraint
    problem += amount[t] <= data['UnloadCapacity'][t - 1]
    
    # Capacity of previous holding plus unload capacity
    if t > 1:
        problem += amount[t] <= hold[t - 1] + data['UnloadCapacity'][t - 1]

    # Crane capacity must meet demand
    problem += pulp.lpSum(crane[t] * data['CraneCapacity'] for t in range(1, data['T'] + 1)) >= data['Demands'][t - 1]
    
    # Crane rental limit
    problem += crane[t] <= data['NumCranes']

# Final holding constraint
problem += hold[data['T']] == 0

# Solve the problem
problem.solve()

# Prepare output
containers_unloaded = [amount[t].varValue for t in range(1, data['T'] + 1)]
cranes_rented = [crane[t].varValue for t in range(1, data['T'] + 1)]
total_cost = pulp.value(problem.objective)

# Output
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')