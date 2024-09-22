import pulp
import json

# Input Data
data_json = '''{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}'''
data = json.loads(data_json.replace("'", "\""))

# Parameters
T = data['T']  # Number of days
period = data['Period']  # Number of consecutive days for night shift
demand = data['Demand']  # Demand for nurses for each day

# Create the linear programming problem
problem = pulp.LpProblem("NursingShiftScheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(start[j] for j in range(1, T + 1)), "TotalNursesHired"

# Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[max(1, j - k)] for k in range(0, min(period, j))) >= demand[j - 1],
        f"Demand_Satisfaction_Day_{j}"
    )

# Solve the problem
problem.solve()

# Output the results
for j in range(1, T + 1):
    print(f'Start_{j}: {start[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')