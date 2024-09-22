import pulp

# Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

# Unpack data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
C_c = data['CoalCost']
C_n = data['NukeCost']
M_n = data['MaxNuke']
L_c = data['CoalLife']
L_n = data['NukeLife']

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Variables
x_c = pulp.LpVariable.dicts("Coal_Added", range(T), lowBound=0, cat='Continuous')
x_n = pulp.LpVariable.dicts("Nuke_Added", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C_c * x_c[t] + C_n * x_n[t] for t in range(T)), "Total_Cost"

# Constraints
for t in range(T):
    # Capacity availability constraint
    problem += (oil_cap[t] + pulp.lpSum(x_c[j] for j in range(max(0, t-L_c+1), t+1)) + 
                pulp.lpSum(x_n[j] for j in range(max(0, t-L_n+1), t+1))) >= demand[t]

    # Maximum nuclear capacity constraint
    problem += pulp.lpSum(x_n[j] for j in range(t+1)) <= (
            M_n / 100.0 * (oil_cap[t] + pulp.lpSum(x_c[j] for j in range(t+1)) + 
            pulp.lpSum(x_n[j] for j in range(t+1))))

# Solve the problem
problem.solve()

# Collect results
coal_cap_added = [pulp.value(x_c[t]) for t in range(T)]
nuke_cap_added = [pulp.value(x_n[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output results
print("Coal Capacity Added:", coal_cap_added)
print("Nuclear Capacity Added:", nuke_cap_added)
print("Total Cost:", total_cost)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')