import pulp

# Load data
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
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0) for t in range(data['T'])]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, cat=pulp.LpInteger) for t in range(data['T'])]
hold = [pulp.LpVariable(f'hold_{t}', lowBound=0) for t in range(data['T'] + 1)]

# Objective function
total_cost = pulp.lpSum(
    [data['UnloadCosts'][t] * amount[t] +
     data['HoldingCost'] * hold[t + 1] +
     data['CraneCost'] * crane[t] for t in range(data['T'])]
)
problem += total_cost

# Constraints
problem += hold[0] == data['InitContainer'], "Initial_Condition"
problem += hold[data['T']] == 0, "Final_Condition"

for t in range(data['T']):
    # Unloading Capacity
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unloading_Capacity_{t}"
    
    # Yard Capacity
    problem += hold[t + 1] <= data['MaxContainer'], f"Yard_Capacity_{t}"
    
    # Inventory Balance
    problem += hold[t + 1] == hold[t] + amount[t] - data['Demands'][t], f"Inventory_Balance_{t}"
    
    # Loading Capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t], f"Loading_Capacity_{t}"
    
    # Cranes Limit
    problem += crane[t] <= data['NumCranes'], f"Cranes_Limit_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')