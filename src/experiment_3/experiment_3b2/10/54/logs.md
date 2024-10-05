# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create a mathematical model for this problem, we'll define variables, objective function, and constraints based on the given information.

######### Decision Variables:
Let \( x_p \) be the number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).

######### Objective Function:
We want to maximize the total profit, which is the difference between revenue and total machine and labor costs. The profit function can be expressed as:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) - \text{Labor Cost for Machine 1}
\]

The labor cost for Machine 1 involves both standard and overtime costs:
- If the total hours required for Machine 1 are less than or equal to \(\text{overtime_hour}\), the labor cost is \(\text{standard_cost} \times \text{hours used}\).
- If the total hours exceed \(\text{overtime_hour}\), the cost is \(\text{standard_cost} \times \text{overtime_hour} + \text{overtime_cost} \times (\text{hours used} - \text{overtime_hour})\).

Let \( T_1 = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \) be the total hours required on Machine 1.

######### Constraints:
1. **Minimum production requirement for each part:**
   \[
   x_p \geq \text{min_batches}_{p} \quad \forall \, p = 1, \ldots, P
   \]

2. **Machine availability (except Machine 1):**
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m \quad \forall \, m = 2, \ldots, M
   \]

3. **Non-negativity constraint:**
   \[
   x_p \geq 0 \quad \forall \, p = 1, \ldots, P
   \]

Here's the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced per month, for \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the profit given by:
\[
Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) - \text{Labor Cost for Machine 1}
\]

Where the labor cost for Machine 1 is calculated as:
\[
\text{Labor Cost for Machine 1} = 
\begin{cases} 
\text{standard_cost} \times T_1, & \text{if } T_1 \leq \text{overtime_hour} \\
\text{standard_cost} \times \text{overtime_hour} + \text{overtime_cost} \times (T_1 - \text{overtime_hour}), & \text{if } T_1 > \text{overtime_hour}
\end{cases}
\]
Here, \( T_1 = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \).

\subsection*{Constraints}
1. Minimum production requirement for each part:
   \[
   x_p \geq \text{min_batches}_{p} \quad \forall \, p = 1, \ldots, P
   \]

2. Machine availability (except Machine 1):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m \quad \forall \, m = 2, \ldots, M
   \]

3. Non-negativity constraint:
   \[
   x_p \geq 0 \quad \forall \, p = 1, \ldots, P
   \]

\end{document}
```

This model enables the manufacturer to determine the optimal number of batches for each part to produce each month to maximize profit, taking into account machine costs, labor costs, availability constraints, and minimum production requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced per month, for \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the profit given by:
\[
Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) - \text{Labor Cost for Machine 1}
\]

Where the labor cost for Machine 1 is calculated as:
\[
\text{Labor Cost for Machine 1} = 
\begin{cases} 
\text{standard_cost} \times T_1, & \text{if } T_1 \leq \text{overtime_hour} \\
\text{standard_cost} \times \text{overtime_hour} + \text{overtime_cost} \times (T_1 - \text{overtime_hour}), & \text{if } T_1 > \text{overtime_hour}
\end{cases}
\]
Here, \( T_1 = \sum_{p=1}^{P} \text{time}_{1,p} \cdot x_p \).

\subsection*{Constraints}
1. Minimum production requirement for each part:
   \[
   x_p \geq \text{min_batches}_{p} \quad \forall \, p = 1, \ldots, P
   \]

2. Machine availability (except Machine 1):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m \quad \forall \, m = 2, \ldots, M
   \]

3. Non-negativity constraint:
   \[
   x_p \geq 0 \quad \forall \, p = 1, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0)

#### Calculate T1
T1 = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))

#### Labor cost for Machine 1
labor_cost_m1 = pulp.LpVariable("labor_cost_m1")

#### Labor cost expression
labor_cost_expr = pulp.lpSum([
    data['StandardCost'] * T1 if T1 <= data['OvertimeHour'][0] else 
    data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'][0] * (T1 - data['OvertimeHour'][0])
])

#### Objective function
profit = pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts'])) - \
         pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])) - \
         labor_cost_expr

problem += profit

#### Constraints

#### Minimum production requirement for each part
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"MinBatch_Constraint_{p}"

#### Machine availability constraints (except Machine 1)
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"MachineAvailability_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

