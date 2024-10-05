import pulp

# Load the data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    'strength': [2000, 1500, 1000], 
    'lessonewaste': [0.25, 0.2, 0.1], 
    'moreonewaste': [0.1, 0.05, 0.05], 
    'recruit': [500, 800, 500], 
    'costredundancy': [200, 500, 500], 
    'num_overman': 150, 
    'costoverman': [1500, 2000, 3000], 
    'num_shortwork': 50, 
    'costshort': [500, 400, 400]
}

K = len(data["strength"])  # Number of manpower categories
I = len(data["requirement"][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
recruit_vars = [[pulp.LpVariable(f"recruit_{k}_{i}", 0, data["recruit"][k], cat='Integer') for i in range(I)] for k in range(K)]
overman_vars = [[pulp.LpVariable(f"overman_{k}_{i}", 0, data["num_overman"], cat='Integer') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f"short_{k}_{i}", 0, data["num_shortwork"], cat='Integer') for i in range(I)] for k in range(K)]
redundancy_vars = [[pulp.LpVariable(f"redundancy_{k}_{i}", 0) for i in range(I)] for k in range(K)]

# Objective function
costs = []
for k in range(K):
    for i in range(I):
        costs.append(
            data["costredundancy"][k] * redundancy_vars[k][i] +
            data["costoverman"][k] * overman_vars[k][i] +
            data["costshort"][k] * short_vars[k][i]
        )
problem += pulp.lpSum(costs)

# Constraints
for k in range(K):
    manpower_prev = data["strength"][k]
    for i in range(I):
        wastage_lessone = data["lessonewaste"][k] * recruit_vars[k][i]
        wastage_moreone = data["moreonewaste"][k] * manpower_prev

        problem += (
            recruit_vars[k][i] 
            + manpower_prev 
            - wastage_lessone 
            - wastage_moreone 
            - redundancy_vars[k][i] 
            + overman_vars[k][i] 
            + 0.5 * short_vars[k][i]
            >= data["requirement"][k][i]
        )

        manpower_prev = (
            manpower_prev 
            + recruit_vars[k][i] 
            - wastage_lessone 
            - wastage_moreone 
            - redundancy_vars[k][i]
        )

# Solve the problem
problem.solve()

# Prepare the output format
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overman_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')