import pulp

# Data provided
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

# Define the problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision variables
P = len(data['prices'])  # Number of parts
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

# Objective function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * (
    pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
) for m in range(len(data['machine_costs'])))
total_hours = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))

# Labor Costs
labor_costs = pulp.lpIf(total_hours <= data['overtime_hour'],
                        data['standard_cost'] * total_hours,
                        data['standard_cost'] * data['overtime_hour'] + 
                        data['overtime_cost'] * (total_hours - data['overtime_hour']))

# Full objective function
profit_equation = total_profit - machine_costs - labor_costs
problem += profit_equation, "Total_Profit"

# Constraints
# Minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Machine availability constraints
for m in range(len(data['availability'])):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
        <= data['availability'][m], f"Availability_{m}"
    )

# Minimum profit constraint
problem += profit_equation >= data['min_profit'], "Min_Profit"

# Solve the problem
problem.solve()

# Output results
batches_output = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')