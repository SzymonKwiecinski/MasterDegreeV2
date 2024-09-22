import pulp

# Data extracted from the given JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]
standard_cost = 20
overtime_cost = 30
overtime_hour = 400
min_profit = 5000

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Compute labor cost
y1 = sum(time_required[0][p] * x[p] for p in range(P))
labor_cost_1 = pulp.LpVariable("Labor_Cost_1", lowBound=0, cat='Continuous')

# Add constraints for labor cost determination
problem += labor_cost_1 == standard_cost * y1 + pulp.lpSum([(y1 - overtime_hour) * overtime_cost if y1 > overtime_hour else 0]), "Labor_Cost_Calculation"

# Objective function
profit = sum(prices[p] * x[p] for p in range(P))
machine_costs_total = sum(machine_costs[m] * sum(time_required[m][p] * x[p] for p in range(P)) for m in range(1, M))
problem += profit - machine_costs_total - labor_cost_1

# Constraints
# Minimum production constraint
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Batches_Constraint_{p}"

# Machine time constraint
for m in range(1, M):
    problem += sum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Machine_Time_Constraint_{m}"

# Profit constraint
problem += profit - machine_costs_total - labor_cost_1 >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')