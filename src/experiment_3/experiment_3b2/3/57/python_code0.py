import pulp

# Data from the provided JSON format
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

# Define the problem
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, cat='Integer')
yard = pulp.LpVariable.dicts("yard", range(data['T'] + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] +
                       data['HoldingCost'] * yard[t] +
                       data['CraneCost'] * crane[t] 
                       for t in range(data['T'])), "Total Cost"

# Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unload_Capacity_Constraint_{t+1}"
    if t > 0:
        problem += yard[t-1] + amount[t] - data['Demands'][t] == yard[t], f"Balance_Equation_{t+1}"
    else:
        problem += yard[0] == data['InitContainer'], "Initial_Containers"

    problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t], f"Cranes_Capacity_Constraint_{t+1}"
    problem += yard[t] <= data['MaxContainer'], f"Max_Container_Constraint_{t+1}"
    problem += crane[t] <= data['NumCranes'], f"Crane_Limit_Constraint_{t+1}"

# Final constraint for yard at the last month
problem += yard[data['T']] == 0, "Final_Yard_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')