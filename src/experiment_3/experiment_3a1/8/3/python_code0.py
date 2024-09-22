import pulp
import json

# Data from JSON format
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Problem Definition
problem = pulp.LpProblem("ElectricityCapacityExpansion", pulp.LpMinimize)

# Variables
coal = pulp.LpVariable.dicts("coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(1, data['T'] + 1)), "Total Cost"

# Constraints
for t in range(1, data['T'] + 1):
    # Demand constraint
    problem += (data['OilCap'][t-1] + 
                 pulp.lpSum(coal[t - i] for i in range(1, min(t, data['CoalLife']) + 1)) + 
                 pulp.lpSum(nuke[t - i] for i in range(1, min(t, data['NukeLife']) + 1)) >= 
                 data['Demand'][t-1]), f"Demand_Constraint_{t}"
    
    # Nuclear Capacity Constraint
    problem += (pulp.lpSum(coal[t - i] for i in range(1, min(t, data['CoalLife']) + 1)) + 
                 pulp.lpSum(nuke[t - i] for i in range(1, min(t, data['NukeLife']) + 1)) >= 
                 (data['MaxNuke'] / 100) * 
                 (data['OilCap'][t-1] + 
                  pulp.lpSum(coal[t - i] for i in range(1, min(t, data['CoalLife']) + 1)) + 
                  pulp.lpSum(nuke[t - i] for i in range(1, min(t, data['NukeLife']) + 1))),
                 f"Nuclear_Capacity_Constraint_{t}")

# Solve the problem
problem.solve()

# Extract results
coal_cap_added = [coal[t].varValue for t in range(1, data['T'] + 1)]
nuke_cap_added = [nuke[t].varValue for t in range(1, data['T'] + 1)]
total_cost = pulp.value(problem.objective)

# Output
print(f'Coal Capacity Added Each Year: {coal_cap_added}')
print(f'Nuclear Capacity Added Each Year: {nuke_cap_added}')
print(f'Total Cost incurred: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')