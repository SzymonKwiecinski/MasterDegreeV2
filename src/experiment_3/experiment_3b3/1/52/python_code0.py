import pulp

# Data from the JSON input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("PowerPlantDistribution", pulp.LpMinimize)

# Decision Variables: send[p][c] for each power plant p and city c
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), 
                             lowBound=0, cat='Continuous')

# Objective Function: Minimize the total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[(p, c)] 
                      for p in range(P) for c in range(C))

# Constraints

# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= data['supply'][p]

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= data['demand'][c]

# Solve the problem
problem.solve()

# Output the results
print("Electricity sent from each power plant to each city:")
for p in range(P):
    for c in range(C):
        print(f" Power Plant {p+1} to City {c+1}: {send[(p, c)].varValue} million kwh")

print(f"Total Transmission Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")