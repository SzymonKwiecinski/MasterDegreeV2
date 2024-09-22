import pulp

# Data
data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}

# Extract data
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_limits = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(requirement)  # number of manpower categories
I = len(requirement[0])  # number of years

# Create LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=recruit_limits[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Add objective function
total_cost = pulp.lpSum(
    costredundancy[k] * pulp.lpSum(recruit[k][i] for i in range(I)) +
    costoverman[k] * pulp.lpSum(overmanning[k][i] for i in range(I)) +
    costshort[k] * pulp.lpSum(short[k][i] for i in range(I))
    for k in range(K)
)
problem += total_cost

# Initial number calculation for first year
for k in range(K):
    existing_workers = strength[k] * (1 - moreonewaste[k])
    # Constraints for each year
    for i in range(I):
        if i == 0:
            current_workers = existing_workers
        else:
            current_workers = (
                remaining_from_last_year * (1 - moreonewaste[k]) +
                recruit[k][i] * (1 - lessonewaste[k])
            )
        
        # Total number of workers with short time and overmanning
        total_workers = current_workers + 0.5 * short[k][i] + overmanning[k][i]
        
        # Constraint to meet the requirement
        problem += total_workers >= requirement[k][i]
        
        # Prepare remaining workers for the next year
        remaining_from_last_year = total_workers - overmanning[k][i]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "recruit": [[int(recruit[k][i].varValue) for i in range(I)] for k in range(K)],
    "overmanning": [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)],
    "short": [[int(short[k][i].varValue) for i in range(I)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')