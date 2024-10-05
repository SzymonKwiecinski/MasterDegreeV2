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
To solve this problem, we need to formulate it as a linear programming (LP) model. The objective is to maximize the profit, which is the total revenue from selling the parts minus the total costs incurred from machine usage and labor for Machine 1. Below is the formulation of the problem in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p$, with $p \in \{1, ..., P\}$.
    \item $M$: Set of machines, indexed by $m$, with $m \in \{1, ..., M\}$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 parts $p$.
    \item $cost_{m}$: Cost per hour for using machine $m$.
    \item $available_{m}$: Available hours per month for machine $m$.
    \item $price_{p}$: Selling price per batch (100 units) of part $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required per month.
    \item $standard\_cost$: Standard labor cost per hour for Machine 1.
    \item $overtime\_cost$: Overtime labor cost per hour for Machine 1.
    \item $overtime\_hour$: Maximum regular labor hours for Machine 1 before overtime applies.
    \item $min\_profit$: Minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce.
    \item $h_{1}^{reg}$: Regular working hours for Machine 1.
    \item $h_{1}^{over}$: Overtime hours for Machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=2}^{M} \sum_{p=1}^{P} \left( cost_{m} \times time_{m,p} \times batches_{p} \right) - \left( standard\_cost \times h_{1}^{reg} + overtime\_cost \times h_{1}^{over} \right)
\]

\subsection*{Constraints}
Machine constraints:
\[
\sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m}, \quad \forall m \in \{2, ..., M\}
\]

Machine 1 working hour constraints:
\[
h_{1}^{reg} + h_{1}^{over} \geq \sum_{p=1}^{P} time_{1,p} \times batches_{p}
\]
\[
h_{1}^{reg} \leq overtime\_hour
\]

Contractual obligations:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, ..., P\}
\]

Profit constraint:
\[
Z \geq min\_profit
\]

Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, ..., P\}
\]
\[
h_{1}^{reg} \geq 0, \quad h_{1}^{over} \geq 0
\]

\end{document}
```

This formulation ensures that all the given problem constraints are met, and it seeks to determine the optimal number of batches for each part to maximize profit while ensuring contractual and machine constraints are fulfilled.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p$, with $p \in \{1, ..., P\}$.
    \item $M$: Set of machines, indexed by $m$, with $m \in \{1, ..., M\}$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 parts $p$.
    \item $cost_{m}$: Cost per hour for using machine $m$.
    \item $available_{m}$: Available hours per month for machine $m$.
    \item $price_{p}$: Selling price per batch (100 units) of part $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required per month.
    \item $standard\_cost$: Standard labor cost per hour for Machine 1.
    \item $overtime\_cost$: Overtime labor cost per hour for Machine 1.
    \item $overtime\_hour$: Maximum regular labor hours for Machine 1 before overtime applies.
    \item $min\_profit$: Minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce.
    \item $h_{1}^{reg}$: Regular working hours for Machine 1.
    \item $h_{1}^{over}$: Overtime hours for Machine 1.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=2}^{M} \sum_{p=1}^{P} \left( cost_{m} \times time_{m,p} \times batches_{p} \right) - \left( standard\_cost \times h_{1}^{reg} + overtime\_cost \times h_{1}^{over} \right)
\]

\subsection*{Constraints}
Machine constraints:
\[
\sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m}, \quad \forall m \in \{2, ..., M\}
\]

Machine 1 working hour constraints:
\[
h_{1}^{reg} + h_{1}^{over} \geq \sum_{p=1}^{P} time_{1,p} \times batches_{p}
\]
\[
h_{1}^{reg} \leq overtime\_hour
\]

Contractual obligations:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, ..., P\}
\]

Profit constraint:
\[
Z \geq min\_profit
\]

Non-negativity constraints:
\[
batches_{p} \geq 0, \quad \forall p \in \{1, ..., P\}
\]
\[
h_{1}^{reg} \geq 0, \quad h_{1}^{over} \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
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

#### Indices
P = range(len(data['prices']))
M = range(len(data['machine_costs']))

#### Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

#### Decision Variables
batches = {p: pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in P}
h1_reg = pulp.LpVariable('h1_reg', lowBound=0, cat='Continuous')
h1_over = pulp.LpVariable('h1_over', lowBound=0, cat='Continuous')

#### Objective Function
problem += (
    pulp.lpSum(data['prices'][p] * batches[p] for p in P) 
    - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] for m in M[1:] for p in P)
    - (data['standard_cost'] * h1_reg + data['overtime_cost'] * h1_over)
), "Total_Profit"

#### Constraints

#### Machine constraints for machines other than Machine 1
for m in M[1:]:
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m]
    ), f"Machine_{m}_Availability"

#### Machine 1 working constraints
problem += (
    h1_reg + h1_over >= pulp.lpSum(data['time_required'][0][p] * batches[p] for p in P)
), "Machine_1_Working_Hours"

problem += (
    h1_reg <= data['overtime_hour']
), "Machine_1_Regular_Hours_Limit"

#### Contractual obligations
for p in P:
    problem += (
        batches[p] >= data['min_batches'][p]
    ), f"Min_Batches_{p}"

#### Profit constraint
problem += (
    pulp.lpSum(data['prices'][p] * batches[p] for p in P) 
    - pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] for m in M[1:] for p in P)
    - (data['standard_cost'] * h1_reg + data['overtime_cost'] * h1_over) >= data['min_profit']
), "Profit_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

