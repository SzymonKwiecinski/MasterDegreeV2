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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{enumerate}
    \item Let \( b_p \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).
\end{enumerate}

\textbf{Parameters:}
\begin{enumerate}
    \item \( time_{m,p} \): time required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \): cost per hour for using machine \( m \)
    \item \( available_m \): availability of machine \( m \) in hours per month
    \item \( price_p \): selling price per batch of part \( p \)
    \item \( min\_batches_p \): minimum batches of part \( p \) required to fulfill a contract
    \item \( standard\_cost \): standard labor cost per hour
    \item \( overtime\_cost \): overtime labor cost per hour
    \item \( overtime\_hour \): regular hours before overtime applies
\end{enumerate}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( (price_p - \sum_{m=1}^{M} cost_m \cdot \frac{time_{m,p}}{100}) \cdot b_p \right) - \text{Labor\_Cost}
\]
Where the \text{Labor\_Cost} is calculated based on the usage of machine 1.

\textbf{Labor Cost Calculation:}
\[
\text{Labor\_Cost} = 
\begin{cases}
standard\_cost \cdot \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} & \text{if } \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} - overtime\_hour \right) & \text{otherwise}
\end{cases}
\]

\textbf{Constraints:}
\begin{align*}
\text{1. Machine Availability:} & \quad \sum_{p=1}^{P} \frac{b_p \cdot time_{m,p}}{100} \leq available_m, \quad \forall m = 2, \ldots, M \\
\text{2. Minimum Production Requirements:} & \quad b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
\end{align*}

\textbf{Non-negativity:}
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{enumerate}
    \item Let \( b_p \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).
\end{enumerate}

\textbf{Parameters:}
\begin{enumerate}
    \item \( time_{m,p} \): time required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \): cost per hour for using machine \( m \)
    \item \( available_m \): availability of machine \( m \) in hours per month
    \item \( price_p \): selling price per batch of part \( p \)
    \item \( min\_batches_p \): minimum batches of part \( p \) required to fulfill a contract
    \item \( standard\_cost \): standard labor cost per hour
    \item \( overtime\_cost \): overtime labor cost per hour
    \item \( overtime\_hour \): regular hours before overtime applies
\end{enumerate}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( (price_p - \sum_{m=1}^{M} cost_m \cdot \frac{time_{m,p}}{100}) \cdot b_p \right) - \text{Labor\_Cost}
\]
Where the \text{Labor\_Cost} is calculated based on the usage of machine 1.

\textbf{Labor Cost Calculation:}
\[
\text{Labor\_Cost} = 
\begin{cases}
standard\_cost \cdot \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} & \text{if } \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} \frac{b_p \cdot time_{1,p}}{100} - overtime\_hour \right) & \text{otherwise}
\end{cases}
\]

\textbf{Constraints:}
\begin{align*}
\text{1. Machine Availability:} & \quad \sum_{p=1}^{P} \frac{b_p \cdot time_{m,p}}{100} \leq available_m, \quad \forall m = 2, \ldots, M \\
\text{2. Minimum Production Requirements:} & \quad b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
\end{align*}

\textbf{Non-negativity:}
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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

P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
cost_m = data['MachineCosts']
availability = data['Availability']
price_p = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour'][0]  #### Using only the first machine's overtime hour since it is relevant for labor cost

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
b = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function components
profit_from_sales = sum((price_p[p] - sum(cost_m[m] * time_required[m][p] / 100 for m in range(M))) * b[p] for p in range(P))

#### Labor Cost calculation
machine_1_usage = sum(b[p] * time_required[0][p] / 100 for p in range(P))
labor_cost = pulp.LpVariable('Labor_Cost', lowBound=0, cat='Continuous')

#### Defining labor cost constraint
problem += (labor_cost == standard_cost * machine_1_usage, "Labor_Cost_Standard") if machine_1_usage <= overtime_hour else \
    (labor_cost == standard_cost * overtime_hour + overtime_cost * (machine_1_usage - overtime_hour), "Labor_Cost_Overtime")

#### Define the objective function
problem += profit_from_sales - labor_cost, "Total_Profit"

#### Constraints
#### Machine availability constraints for machines other than machine 1
for m in range(1, M):
    problem += sum(b[p] * time_required[m][p] / 100 for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

#### Minimum production requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Part_{p}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

