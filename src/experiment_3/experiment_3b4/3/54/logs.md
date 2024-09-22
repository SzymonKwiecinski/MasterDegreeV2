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
To model this problem as a Linear Programming (LP) problem, we need to define the decision variables, the objective function, and the constraints.

**Decision Variables:**
- Let \( x_p \) denote the number of batches of part \( p \) produced per month for \( p = 1, 2, \ldots, P \).

**Objective Function:**
- Maximize the total profit, which is the total sales revenue minus the total machine cost.
- The sales revenue from selling \( x_p \) batches of part \( p \) is \( \sum_{p=1}^{P} \text{price}_{p} \times x_p \).
- The cost for using machine \( m \) (except machine 1) is \( \sum_{p=1}^{P} \text{cost}_{m} \times \text{time}_{m,p} \times x_p \).
- Special cost for machine 1 due to labor: 
  - For usage up to \(\text{overtime\_hour}\), charge \(\text{standard\_cost}\) per hour.
  - For usage beyond \(\text{overtime\_hour}\), charge \(\text{overtime\_cost}\) per hour.

**Constraints:**
1. Production constraints: 
   - \( x_p \geq \text{min\_batches}_{p} \) for all \( p \).
   
2. Machine availability constraints for machines \( m = 2, \ldots, M \):
   - \( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m} \).

3. Special condition for machine 1:
   - \(\sum_{p=1}^{P} \text{time}_{1,p} \times x_p\) results in labor cost with standard and overtime rates.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturing}

\textbf{Decision Variables:}
\[
x_p \quad \text{(number of batches of part } p \text{ produced per month)}
\]

\textbf{Objective Function:}
Maximize the total profit, 
\[
\text{Profit} = \sum_{p=1}^{P} \text{price}_{p} \times x_p - \sum_{m=2}^{M} \left(\sum_{p=1}^{P} \text{cost}_{m} \times \text{time}_{m,p} \times x_p \right) - \text{Labor cost for machine 1}
\]

\textbf{Labor Cost for Machine 1:}
\[
\text{Labor cost} = 
\begin{cases} 
\text{standard\_cost} \times \text{usage} & \text{if } \text{usage} \leq \text{overtime\_hour}\\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times (\text{usage} - \text{overtime\_hour}) & \text{if } \text{usage} > \text{overtime\_hour}
\end{cases}
\]
where \(\text{usage} = \sum_{p=1}^{P} \text{time}_{1,p} \times x_p\)

\textbf{Constraints:}
\begin{align*}
& x_p \geq \text{min\_batches}_{p}, \quad \forall p \\
& \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m}, \quad \forall m = 2, \ldots, M
\end{align*}

\end{document}
```

This model will help determine the optimal number of batches of each part to produce in order to maximize profit while considering machine costs and labor for machine 1, contract obligations, and machine availability.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturing}

\textbf{Decision Variables:}
\[
x_p \quad \text{(number of batches of part } p \text{ produced per month)}
\]

\textbf{Objective Function:}
Maximize the total profit, 
\[
\text{Profit} = \sum_{p=1}^{P} \text{price}_{p} \times x_p - \sum_{m=2}^{M} \left(\sum_{p=1}^{P} \text{cost}_{m} \times \text{time}_{m,p} \times x_p \right) - \text{Labor cost for machine 1}
\]

\textbf{Labor Cost for Machine 1:}
\[
\text{Labor cost} = 
\begin{cases} 
\text{standard\_cost} \times \text{usage} & \text{if } \text{usage} \leq \text{overtime\_hour}\\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times (\text{usage} - \text{overtime\_hour}) & \text{if } \text{usage} > \text{overtime\_hour}
\end{cases}
\]
where \(\text{usage} = \sum_{p=1}^{P} \text{time}_{1,p} \times x_p\)

\textbf{Constraints:}
\begin{align*}
& x_p \geq \text{min\_batches}_{p}, \quad \forall p \\
& \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_{m}, \quad \forall m = 2, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Create the LP problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision variables
x = {p: pulp.LpVariable(f"x_{p}", lowBound=data['MinBatches'][p]) for p in range(data['NumParts'])}

#### Objective function components
profit_terms = [data['Prices'][p] * x[p] for p in range(data['NumParts'])]
machine1_usage = sum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))

#### Calculate Labor cost for Machine 1
if machine1_usage <= data['OvertimeHour'][0]:
    labor_cost = data['StandardCost'] * machine1_usage
else:
    labor_cost = data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (machine1_usage - data['OvertimeHour'][0])

#### Objective Function
profit = sum(profit_terms) - labor_cost - sum(
    data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts']))
    for m in range(1, data['NumMachines'])
)

problem += profit

#### Constraints
#### Machine time availability constraints for each machine (except machine 1 due to dynamic labor cost)
for m in range(1, data['NumMachines']):
    problem += sum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

