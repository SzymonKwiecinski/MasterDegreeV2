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

# Create the Linear Programming problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("UnloadedContainers", range(data['T']), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("CranesRented", range(data['T']), lowBound=0, upBound=data['NumCranes'], cat='Integer')
z = pulp.LpVariable.dicts("ContainersInStorage", range(data['T'] + 1), lowBound=0, upBound=data['MaxContainer'], cat='Integer')

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * x[t] + data['HoldingCost'] * z[t] + data['CraneCost'] * y[t] for t in range(data['T'])), "Total_Cost"

# Constraints

# Initial Condition
problem += (z[0] == data['InitContainer'], "Initial_Containers")

# Demand Fulfillment Constraints
for t in range(1, data['T']):  # Start from 1 to avoid index -1
    problem += (data['Demands'][t] == x[t] + z[t-1] - z[t], f"Demand_Fulfillment_{t}")

# Unloading Capacity Constraints
for t in range(data['T']):
    problem += (x[t] <= data['UnloadCapacity'][t], f"Unloading_Capacity_{t}")

# Storage Capacity Constraints
for t in range(data['T']):
    problem += (z[t] <= data['MaxContainer'], f"Storage_Capacity_{t}")

# End Condition
problem += (z[data['T']] == 0, "End_Condition")

# Crane Usage Constraints
for t in range(data['T']):
    problem += (data['Demands'][t] <= y[t] * data['CraneCapacity'], f"Crane_Usage_{t}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')