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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) represent the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required on machine \( m \) for producing a batch of part \( p \) (in hours)
    \item \( \text{cost}_m \): cost per hour of machine \( m \)
    \item \( \text{available}_m \): availability of machine \( m \) (in hours)
    \item \( \text{price}_p \): selling price of a batch of part \( p \)
    \item \( \text{min\_batches}_p \): minimum required batches of part \( p \)
    \item \( \text{standard\_cost} \): standard labor cost per hour for machine 1
    \item \( \text{overtime\_cost} \): overtime labor cost per hour for machine 1
    \item \( \text{overtime\_hour} \): number of hours before overtime applies
    \item \( \text{min\_profit} \): minimum required profit per month
\end{itemize}

\subsection*{Objective Function}
Maximize total profit, which can be defined as:

\[
\text{total\_profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \text{hours\_used}_m \right) - \text{labor\_cost}
\]

where the labor cost for machine 1 is calculated based on the total hours used:

\[
\text{hours\_used}_1 = \sum_{p=1}^{P} \left( \text{time}_{1,p} \cdot b_p \right)
\]

and 

\[
\text{labor\_cost} = 
\begin{cases} 
    \text{standard\_cost} \cdot \text{hours\_used}_1 & \text{if } \text{hours\_used}_1 \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours\_used}_1 - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]

\subsection*{Constraints}

\begin{itemize}
    \item Availability constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_m \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirements for each part \( p \):
    \[
    b_p \geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
    \]

    \item Profit requirement:
    \[
    \text{total\_profit} \geq \text{min\_profit}
    \end{itemize}
\]

\subsection*{Non-negativity Constraints}
\[
b_p \geq 0 \quad \forall p = 1, \ldots, P
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

\subsection*{Variables}
Let \( b_p \) represent the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): time required on machine \( m \) for producing a batch of part \( p \) (in hours)
    \item \( \text{cost}_m \): cost per hour of machine \( m \)
    \item \( \text{available}_m \): availability of machine \( m \) (in hours)
    \item \( \text{price}_p \): selling price of a batch of part \( p \)
    \item \( \text{min\_batches}_p \): minimum required batches of part \( p \)
    \item \( \text{standard\_cost} \): standard labor cost per hour for machine 1
    \item \( \text{overtime\_cost} \): overtime labor cost per hour for machine 1
    \item \( \text{overtime\_hour} \): number of hours before overtime applies
    \item \( \text{min\_profit} \): minimum required profit per month
\end{itemize}

\subsection*{Objective Function}
Maximize total profit, which can be defined as:

\[
\text{total\_profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \text{hours\_used}_m \right) - \text{labor\_cost}
\]

where the labor cost for machine 1 is calculated based on the total hours used:

\[
\text{hours\_used}_1 = \sum_{p=1}^{P} \left( \text{time}_{1,p} \cdot b_p \right)
\]

and 

\[
\text{labor\_cost} = 
\begin{cases} 
    \text{standard\_cost} \cdot \text{hours\_used}_1 & \text{if } \text{hours\_used}_1 \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours\_used}_1 - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]

\subsection*{Constraints}

\begin{itemize}
    \item Availability constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_m \quad \forall m = 1, \ldots, M
    \]

    \item Minimum production requirements for each part \( p \):
    \[
    b_p \geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
    \]

    \item Profit requirement:
    \[
    \text{total\_profit} \geq \text{min\_profit}
    \end{itemize}
\]

\subsection*{Non-negativity Constraints}
\[
b_p \geq 0 \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON format
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

#### Extract parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Objective Function
#### Labor cost calculation
hours_used_1 = pulp.lpSum(time_required[0][p] * b[p] for p in range(P))
labor_cost = pulp.LpVariable("labor_cost")

problem += (pulp.lpSum(prices[p] * b[p] for p in range(P)) 
             - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M))
             - labor_cost, "Total_Profit")

#### Constraints for labor cost
problem += labor_cost == (
    standard_cost * hours_used_1 if hours_used_1 <= overtime_hour 
    else (standard_cost * overtime_hour + overtime_cost * (hours_used_1 - overtime_hour))
)

#### Availability constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}")

#### Minimum production requirements for each part
for p in range(P):
    problem += (b[p] >= min_batches[p], f"Min_Batches_Constraint_{p+1}")

#### Profit requirement constraint
total_profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M)) - labor_cost
problem += (total_profit >= min_profit, "Profit_Requirement")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

