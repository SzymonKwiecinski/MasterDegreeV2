import pulp
import json

# Data from JSON format
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

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, cat='Integer')
containers_in_yard = pulp.LpVariable.dicts("containers_in_yard", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] + 
                       data['HoldingCost'] * containers_in_yard[t] + 
                       data['CraneCost'] * crane[t] 
                       for t in range(1, data['T'] + 1))

# Constraints

# 1. Demand Fulfillment
problem += (pulp.lpSum(amount[t] for t in range(1, data['T'] + 1)) >= 
            pulp.lpSum(data['Demands'][t-1] for t in range(1, data['T'] + 1))), "Demand_Fulfillment"

# 2. Unloading Capacity
for t in range(1, data['T'] + 1):
    problem += (amount[t] <= data['UnloadCapacity'][t-1]), f"Unloading_Capacity_{t}"

# 3. Crane Capacity
for t in range(1, data['T'] + 1):
    problem += (crane[t] * data['CraneCapacity'] >= data['Demands'][t-1]), f"Crane_Capacity_{t}"

# 4. Crane Rental Limit
for t in range(1, data['T'] + 1):
    problem += (crane[t] <= data['NumCranes']), f"Crane_Rental_Limit_{t}"

# 5. Yard Capacity
for t in range(1, data['T'] + 1):
    problem += (containers_in_yard[t] <= data['MaxContainer']), f"Yard_Capacity_{t}"

# 6. Yard Dynamics
for t in range(2, data['T'] + 1):
    problem += (containers_in_yard[t] == containers_in_yard[t-1] + amount[t] - data['Demands'][t-1]), f"Yard_Dynamics_{t}"

# 7. Initial Condition
problem += (containers_in_yard[1] == data['InitContainer']), "Initial_Condition"

# 8. End Condition
problem += (containers_in_yard[data['T']] == 0), "End_Condition"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')