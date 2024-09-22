import pulp
import json

data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')
switch_increase = pulp.LpVariable.dicts("Switch_Increase", range(T-1), lowBound=0, cat='Continuous')
switch_decrease = pulp.LpVariable.dicts("Switch_Decrease", range(T-1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
            pulp.lpSum(switch_cost * (switch_increase[i] + switch_decrease[i]) for i in range(T-1)), "Total_Cost"

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] == deliver[i], f"Demand_Constraint_{i}"
    else:
        problem += x[i] + inventory[i] == deliver[i] + inventory[i-1], f"Demand_Constraint_{i}"

        # Switching costs constraints
        problem += x[i] - x[i-1] == switch_increase[i-1] - switch_decrease[i-1], f"Switch_Constraint_{i-1}_1"
        problem += switch_increase[i-1] >= 0, f"Switch_Increase_Nonneg_{i-1}"
        problem += switch_decrease[i-1] >= 0, f"Switch_Decrease_Nonneg_{i-1}"
        
        problem += switch_increase[i-1] >= x[i] - x[i-1], f"Switch_Increase_Positive_{i-1}"
        problem += switch_decrease[i-1] >= x[i-1] - x[i], f"Switch_Decrease_Negative_{i-1}"

# Solve the problem
problem.solve()

# Collect results
results = {
    "x": [x[i].varValue for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(json.dumps(results))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')