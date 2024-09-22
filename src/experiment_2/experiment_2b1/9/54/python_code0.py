import pulp
import json

# Input data as JSON
data = '{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}'
input_data = json.loads(data)

# Extracting data from the input
NumMachines = input_data['NumMachines']
NumParts = input_data['NumParts']
TimeRequired = input_data['TimeRequired']
MachineCosts = input_data['MachineCosts']
Availability = input_data['Availability']
Prices = input_data['Prices']
MinBatches = input_data['MinBatches']
StandardCost = input_data['StandardCost']
OvertimeCost = input_data['OvertimeCost']
OvertimeHour = input_data['OvertimeHour']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(NumParts), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum((Prices[p] * batches[p] - 
                     pulp.lpSum([(TimeRequired[m][p] * batches[p] / 100) * MachineCosts[m] for m in range(NumMachines)])) 
                     for p in range(NumParts))
problem += profit

# Constraints
# Minimum batches constraint
for p in range(NumParts):
    problem += batches[p] >= MinBatches[p], f"MinBatches_{p}"

# Machine hour constraints
for m in range(NumMachines):
    problem += (pulp.lpSum(TimeRequired[m][p] * batches[p] for p in range(NumParts)) <= Availability[m]), f"MachineAvailability_{m}"

# Solve the problem
problem.solve()

# Retrieve results
batches_solution = [batches[p].varValue for p in range(NumParts)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_solution,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')