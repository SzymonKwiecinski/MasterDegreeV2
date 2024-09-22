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

\textbf{Variables:}
\begin{itemize}
    \item Let $b_p$ be the number of batches produced for part $p$, where $p \in \{1, 2, \ldots, P\}$.
    \item Let $total\_profit$ be the total profit obtained for the month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} \left( time_{m,p} \cdot b_p \right) \right)
\]

\textbf{Subject to:}

\begin{itemize}
    \item \textbf{Production Requirements:} 
    \[
    b_p \geq min\_batches_p \quad \forall p \in \{1, 2, \ldots, P\}
    \]

    \item \textbf{Machine Hours Availability:} 
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \cdot b_p \right) \leq available_m \quad \forall m \in \{2, 3, \ldots, M\}
    \]

    \item \textbf{Machine 1 Labor Costs:} 
    \begin{itemize}
        \item If $\sum_{p=1}^{P} (time_{1,p} \cdot b_p) \leq overtime\_hour$:
        \[
        total\_cost_1 = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot b_p)
        \]
        
        \item If $\sum_{p=1}^{P} (time_{1,p} \cdot b_p) > overtime\_hour$:
        \[
        total\_cost_1 = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} (time_{1,p} \cdot b_p) - overtime\_hour \right)
        \end{itemize}
    \end{itemize}

    \item \textbf{Profit Condition:} 
    \[
    total\_profit \geq min\_profit
    \]

\textbf{Non-negativity Constraints:}
\[
b_p \geq 0 \quad \forall p \in \{1, 2, \ldots, P\}
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\textbf{Variables:}
\begin{itemize}
    \item Let $b_p$ be the number of batches produced for part $p$, where $p \in \{1, 2, \ldots, P\}$.
    \item Let $total\_profit$ be the total profit obtained for the month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} \left( time_{m,p} \cdot b_p \right) \right)
\]

\textbf{Subject to:}

\begin{itemize}
    \item \textbf{Production Requirements:} 
    \[
    b_p \geq min\_batches_p \quad \forall p \in \{1, 2, \ldots, P\}
    \]

    \item \textbf{Machine Hours Availability:} 
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \cdot b_p \right) \leq available_m \quad \forall m \in \{2, 3, \ldots, M\}
    \]

    \item \textbf{Machine 1 Labor Costs:} 
    \begin{itemize}
        \item If $\sum_{p=1}^{P} (time_{1,p} \cdot b_p) \leq overtime\_hour$:
        \[
        total\_cost_1 = standard\_cost \cdot \sum_{p=1}^{P} (time_{1,p} \cdot b_p)
        \]
        
        \item If $\sum_{p=1}^{P} (time_{1,p} \cdot b_p) > overtime\_hour$:
        \[
        total\_cost_1 = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot \left( \sum_{p=1}^{P} (time_{1,p} \cdot b_p) - overtime\_hour \right)
        \end{itemize}
    \end{itemize}

    \item \textbf{Profit Condition:} 
    \[
    total\_profit \geq min\_profit
    \]

\textbf{Non-negativity Constraints:}
\[
b_p \geq 0 \quad \forall p \in \{1, 2, \ldots, P\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "standard_cost": 20, "overtime_cost": 30, "overtime_hour": 400, "min_profit": 5000}')

#### Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

#### Constants
P = len(prices)  #### Number of parts
M = len(time_required)  #### Number of machines

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### batches produced for parts

#### Objective Function
total_profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) if pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= overtime_hour else
    (standard_cost * overtime_hour + overtime_cost * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) - overtime_hour))) 
    for m in range(M)
)

#### Adding the objective function to the problem
problem += total_profit, "Total_Profit"

#### Constraints
#### Production requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Requirement_for_part_{p}"

#### Machine hours availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

#### Profit condition
problem += total_profit >= min_profit, "Min_Profit_Condition"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

