import pulp

# Data from the provided JSON input
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

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
amounts = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)  # number of containers unloaded
cranes = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')  # number of cranes rented
holds = pulp.LpVariable.dicts("hold", range(1, data['T'] + 1), lowBound=0)  # number of containers held over

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t - 1] * amounts[t] + 
                       data['HoldingCost'] * holds[t] + 
                       data['CraneCost'] * cranes[t] for t in range(1, data['T'] + 1))

# Initial condition
holds[1] = data['InitContainer']  # Initial containers in the yard

# Constraints
for t in range(1, data['T'] + 1):
    # Demand fulfillment
    if t > 1:
        holds[t] = holds[t - 1] + amounts[t] - data['Demands'][t - 1]
    else:
        holds[t] = holds[t - 1] + amounts[t] - data['Demands'][t - 1]  # for t=1, hold[0] is managed by initial condition

    # Yard capacity constraint
    problem += holds[t] <= data['MaxContainer'], f"Yard_Capacity_Constraint_{t}"

    # Unloading capacity constraint
    problem += amounts[t] <= data['UnloadCapacity'][t - 1], f"Unload_Capacity_Constraint_{t}"

    # Crane capacity constraint
    problem += cranes[t] * data['CraneCapacity'] >= amounts[t], f"Crane_Capacity_Constraint_{t}"

# Maximum cranes rental constraint
for t in range(1, data['T'] + 1):
    problem += cranes[t] <= data['NumCranes'], f"Max_Cranes_Constraint_{t}"

# Yard empty condition after last month
problem += holds[data['T']] == 0, "Final_Yard_Empty_Condition"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')