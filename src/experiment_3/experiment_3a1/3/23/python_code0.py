import pulp
import json

# Load the data from the provided JSON format
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

# Extract parameters
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * (data['lessonewaste'][k] * recruit[k][i] for k in range(K) for i in range(I)) +
    data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I) +
    data['costshort'][k] * short[k][i] for k in range(K) for i in range(I)
), "Total_Cost"

# Constraints
for k in range(K):
    problem += (data['strength'][k] + pulp.lpSum(recruit[k][i] for i in range(I)) -
                 pulp.lpSum(short[k][i] for i in range(I)) -
                 pulp.lpSum(overmanning[k][i] for i in range(I)) ==
                 pulp.lpSum(data['requirement'][k][i] for i in range(I)),
                 f"Workforce_Balance_Constraint_{k}")

    problem += (pulp.lpSum(recruit[k][i] for i in range(I)) <= data['recruit'][k],
                 f"Recruit_Constraint_{k}")

    problem += (pulp.lpSum(overmanning[k][i] for i in range(I)) <= data['num_overman'],
                 f"Overman_Constraint_{k}")

    problem += (pulp.lpSum(short[k][i] for i in range(I)) <= data['num_shortwork'],
                 f"Short_Work_Constraint_{k}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')