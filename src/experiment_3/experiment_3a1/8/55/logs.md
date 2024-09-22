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
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( b_p \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \right) - \text{Labor Costs}
\]

Where the labor costs can be calculated based on the hours worked on Machine 1 as follows:

\[
\text{Labor Costs} = 
\begin{cases}
\text{standard\_cost} \cdot \text{total\_hours} & \text{if } \text{total\_hours} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{total\_hours} - \text{overtime\_hour}) & \text{if } \text{total\_hours} > \text{overtime\_hour}
\end{cases}
\]

Where \( \text{total\_hours} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot b_p \).

\subsection*{Constraints}
1. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_m \quad \text{for } m = 1, \ldots, M
   \]

2. Minimum Batch Production Constraints:
   \[
   b_p \geq \text{min\_batches}_p \quad \text{for } p = 1, \ldots, P
   \]

3. Profit Constraints:
   \[
   Z \geq \text{min\_profit}
   \]

4. Non-Negativity Constraints:
   \[
   b_p \geq 0 \quad \text{for } p = 1, \ldots, P
   \]

\subsection*{Output Variables}
The output will consist of:
\begin{itemize}
    \item The number of batches of each part produced: \( \text{batches} = [b_1, b_2, \ldots, b_P] \)
    \item The total profit obtained: \( \text{total\_profit} = Z \)
\end{itemize}

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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Decision Variables}
Let \( b_p \) be the number of batches produced for part \( p \) (for \( p = 1, \ldots, P \)).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \right) - \text{Labor Costs}
\]

Where the labor costs can be calculated based on the hours worked on Machine 1 as follows:

\[
\text{Labor Costs} = 
\begin{cases}
\text{standard\_cost} \cdot \text{total\_hours} & \text{if } \text{total\_hours} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{total\_hours} - \text{overtime\_hour}) & \text{if } \text{total\_hours} > \text{overtime\_hour}
\end{cases}
\]

Where \( \text{total\_hours} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot b_p \).

\subsection*{Constraints}
1. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_m \quad \text{for } m = 1, \ldots, M
   \]

2. Minimum Batch Production Constraints:
   \[
   b_p \geq \text{min\_batches}_p \quad \text{for } p = 1, \ldots, P
   \]

3. Profit Constraints:
   \[
   Z \geq \text{min\_profit}
   \]

4. Non-Negativity Constraints:
   \[
   b_p \geq 0 \quad \text{for } p = 1, \ldots, P
   \]

\subsection*{Output Variables}
The output will consist of:
\begin{itemize}
    \item The number of batches of each part produced: \( \text{batches} = [b_1, b_2, \ldots, b_P] \)
    \item The total profit obtained: \( \text{total\_profit} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Here is the Python script that implements the provided mathematical model using the Pulp library based on the given data. 

```python
import json
import pulp

#### Data from the provided JSON format
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

#### Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Objective function
profit_expr = pulp.lpSum([data['prices'][p] * b[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * b[p] for p in range(P)]) for m in range(M)]) 

#### Calculate total_hours for labor costs
total_hours = pulp.lpSum([data['time_required'][0][p] * b[p] for p in range(P)])  #### Hours from Machine 1
labor_costs = pulp.ifthen(total_hours <= data['overtime_hour'],
                          data['standard_cost'] * total_hours)
labor_costs += pulp.ifthen(total_hours > data['overtime_hour'],
                           data['standard_cost'] * data['overtime_hour'] +
                           data['overtime_cost'] * (total_hours - data['overtime_hour']))

#### Add labor costs to the profit expression
profit_expr -= labor_costs

#### Set the objective
problem += profit_expr, "Total_Profit"

#### Constraints
#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required[m][p]'] * b[p] for p in range(P)]) <= data['availability'][m], f"Availability_Constraint_{m+1}"

#### Minimum Batch Production Constraints
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batch_Constraint_{p+1}"

#### Profit Constraints
problem += profit_expr >= data['min_profit'], "Profit_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches}')
print(f' (Total Profit): <OBJ>{total_profit}</OBJ>')
```

This script sets up and solves the linear programming problem using the Pulp library, incorporating all the constraints and defining the objective function properly. The final output includes the batches produced for each part as well as the total profit achieved.

