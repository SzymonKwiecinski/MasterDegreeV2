import pulp

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("Container_Management_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
cranes = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')
containers = pulp.LpVariable.dicts("containers", range(0, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] + data['HoldingCost'] * containers[t] + data['CraneCost'] * cranes[t]
                      for t in range(1, data['T'] + 1))

# Initial Condition
containers[0] = data['InitContainer']

# Constraints
for t in range(1, data['T'] + 1):
    # Container Balance
    problem += containers[t] == containers[t - 1] + amount[t] - data['Demands'][t - 1], f"Container_Balance_{t}"

    # Final Condition
    if t == data['T']:
        problem += containers[t] == 0, "Final_Condition"

    # Unloading Constraints
    problem += amount[t] <= data['UnloadCapacity'][t - 1], f"Unload_Capacity_{t}"

    # Storage Constraints
    problem += containers[t] <= data['MaxContainer'], f"Max_Container_{t}"

    # Crane Constraints
    problem += cranes[t] * data['CraneCapacity'] >= data['Demands'][t - 1], f"Crane_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')