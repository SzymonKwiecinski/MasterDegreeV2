import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Indices
P = range(len(data['prices']))
M = range(len(data['machine_costs']))

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision Variables
batches = {p: pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in P}
h1_reg = pulp.LpVariable('h1_reg', lowBound=0, cat='Continuous')
h1_over = pulp.LpVariable('h1_over', lowBound=0, cat='Continuous')

# Objective Function
problem += (
    pulp.lpSum(data['prices'][p] * batches[p] for p in P) 
    - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] for m in M[1:] for p in P)
    - (data['standard_cost'] * h1_reg + data['overtime_cost'] * h1_over)
), "Total_Profit"

# Constraints

# Machine constraints for machines other than Machine 1
for m in M[1:]:
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m]
    ), f"Machine_{m}_Availability"

# Machine 1 working constraints
problem += (
    h1_reg + h1_over >= pulp.lpSum(data['time_required'][0][p] * batches[p] for p in P)
), "Machine_1_Working_Hours"

problem += (
    h1_reg <= data['overtime_hour']
), "Machine_1_Regular_Hours_Limit"

# Contractual obligations
for p in P:
    problem += (
        batches[p] >= data['min_batches'][p]
    ), f"Min_Batches_{p}"

# Profit constraint
problem += (
    pulp.lpSum(data['prices'][p] * batches[p] for p in P) 
    - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] for m in M[1:] for p in P)
    - (data['standard_cost'] * h1_reg + data['overtime_cost'] * h1_over) >= data['min_profit']
), "Profit_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')