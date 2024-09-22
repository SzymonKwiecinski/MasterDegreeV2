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

# Create the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')

# Objective Function
total_cost = pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] for t in range(1, data['T'] + 1)) + \
              pulp.lpSum(data['HoldingCost'] * (data['InitContainer'] + 
              pulp.lpSum(amount[i] - data['Demands'][i-1] for i in range(1, t + 1)) for t in range(1, data['T'] + 1))) + \
              pulp.lpSum(data['CraneCost'] * crane[t] for t in range(1, data['T'] + 1))

problem += total_cost

# Constraints
# 1. Demand Satisfaction
problem += (pulp.lpSum(amount[t] for t in range(1, data['T'] + 1)) - 
             pulp.lpSum(data['Demands'][t-1] for t in range(1, data['T'] + 1)) == -data['InitContainer'], "Demand_Satisfaction")

# 2. Unloading Capacity
for t in range(1, data['T'] + 1):
    problem += (amount[t] <= data['UnloadCapacity'][t-1], f"Unload_Capacity_{t}")

# 3. Maximum Storage
for t in range(1, data['T'] + 1):
    problem += (data['InitContainer'] + 
                 pulp.lpSum(amount[i] - data['Demands'][i-1] for i in range(1, t + 1)) <= data['MaxContainer'], 
                 f"Max_Storage_{t}")

# 4. Crane Limitation
for t in range(1, data['T'] + 1):
    problem += (crane[t] * data['CraneCapacity'] >= 
                 pulp.lpSum(data['Demands'][i-1] for i in range(1, t + 1)), f"Crane_Limitation_{t}")

# 6. Non-Negativity (already covered by lower bound)

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, data['T'] + 1)]
cranes_rented = [crane[t].varValue for t in range(1, data['T'] + 1)]
total_cost_value = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: {total_cost_value}')
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')