import pulp

# Parse the data
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

# Initialize problem
problem = pulp.LpProblem("Seaport_Container_Optimization", pulp.LpMinimize)

# Define Variables
amount = pulp.LpVariable.dicts("Amount", range(data['T']), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("Cranes", range(data['T']), lowBound=0, cat='Integer')
cont_in_yard = pulp.LpVariable.dicts("ContainersInYard", range(data['T'] + 1), lowBound=0, cat='Integer')

# Initial condition
cont_in_yard[0] = data['InitContainer']

# Objective Function
problem += pulp.lpSum([amount[t] * data['UnloadCosts'][t] + cranes[t] * data['CraneCost'] +
                       cont_in_yard[t+1] * data['HoldingCost'] for t in range(data['T'])])

# Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"UnloadCapacity_{t}"

    problem += cranes[t] <= data['NumCranes'], f"MaxCranes_{t}"

    problem += cranes[t] * data['CraneCapacity'] >= data['Demands'][t], f"DemandFulfillment_{t}"

    problem += cont_in_yard[t] + amount[t] - data['Demands'][t] == cont_in_yard[t+1], f"FlowBalance_{t}"

    problem += cont_in_yard[t+1] <= data['MaxContainer'], f"MaxYardCapacity_{t+1}"

# Final condition
problem += cont_in_yard[data['T']] == 0, "EndPeriodCondition"

# Solve the problem
problem.solve()

# Construct output
output = {
    "containers_unloaded": [amount[t].varValue for t in range(data['T'])],
    "cranes_rented": [cranes[t].varValue for t in range(data['T'])],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')