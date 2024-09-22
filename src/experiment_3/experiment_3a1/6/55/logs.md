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
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item \( cost_m \): Cost per hour of using machine \( m \).
    \item \( available_m \): Available hours on machine \( m \) per month.
    \item \( price_p \): Sale price per batch of part \( p \).
    \item \( min\_batches_p \): Minimum number of batches required for part \( p \).
    \item \( standard\_cost \): Standard labor cost per hour.
    \item \( overtime\_cost \): Overtime labor cost per hour.
    \item \( overtime\_hour \): Maximum hours before overtime applies.
    \item \( min\_profit \): Minimum desired profit.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit \( Z \):
\[
Z = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot h_m \right) - \text{Labor Cost}
\]
where \( h_m \) is the total hours used on machine \( m \).

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Production Constraints:}
    \[
    b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
    \]

    \item \textbf{Machine Availability Constraints:}
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
    \]

    \item \textbf{Total Hour Constraints for Machine 1:}
    \[
    h_1 \leq available_1 \quad \text{(Individual availability condition can be disregarded)}
    \]

    \item \textbf{Profit Constraint:}
    \[
    \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} (cost_m \cdot h_m) - \text{Labor Cost} \geq min\_profit
    \]

    \item \textbf{Labor Cost Calculation:}
    \[
    \text{Labor Cost} = 
    \begin{cases} 
      standard\_cost \cdot h_1 & \text{if } h_1 \leq overtime\_hour \\ 
      standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (h_1 - overtime\_hour) & \text{if } h_1 > overtime\_hour 
    \end{cases}
    \]

\end{itemize}

\subsection*{Output}
The outputs will be:
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit \)
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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item \( cost_m \): Cost per hour of using machine \( m \).
    \item \( available_m \): Available hours on machine \( m \) per month.
    \item \( price_p \): Sale price per batch of part \( p \).
    \item \( min\_batches_p \): Minimum number of batches required for part \( p \).
    \item \( standard\_cost \): Standard labor cost per hour.
    \item \( overtime\_cost \): Overtime labor cost per hour.
    \item \( overtime\_hour \): Maximum hours before overtime applies.
    \item \( min\_profit \): Minimum desired profit.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit \( Z \):
\[
Z = \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot h_m \right) - \text{Labor Cost}
\]
where \( h_m \) is the total hours used on machine \( m \).

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Production Constraints:}
    \[
    b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
    \]

    \item \textbf{Machine Availability Constraints:}
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M
    \]

    \item \textbf{Total Hour Constraints for Machine 1:}
    \[
    h_1 \leq available_1 \quad \text{(Individual availability condition can be disregarded)}
    \]

    \item \textbf{Profit Constraint:}
    \[
    \sum_{p=1}^{P} \left( price_p \cdot b_p \right) - \sum_{m=1}^{M} (cost_m \cdot h_m) - \text{Labor Cost} \geq min\_profit
    \]

    \item \textbf{Labor Cost Calculation:}
    \[
    \text{Labor Cost} = 
    \begin{cases} 
      standard\_cost \cdot h_1 & \text{if } h_1 \leq overtime\_hour \\ 
      standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (h_1 - overtime\_hour) & \text{if } h_1 > overtime\_hour 
    \end{cases}
    \]

\end{itemize}

\subsection*{Output}
The outputs will be:
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit \)
\end{itemize}

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

#### Problem definition
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

#### Variables
P = len(data['prices'])
b = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

#### Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * b[p] for p in range(P))
total_machine_cost = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P))) for m in range(len(data['machine_costs'])))
h_1 = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))
overtime_cost = pulp.lpSum(data['standard_cost'] * min(h_1, data['overtime_hour'])) + pulp.lpSum(data['overtime_cost'] * pulp.lpMax(0, h_1 - data['overtime_hour']))

problem += total_revenue - total_machine_cost - overtime_cost, "Total_Profit"

#### Constraints
#### Production Constraints
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"MinBatches_Constraint_{p}"

#### Machine Availability Constraints
for m in range(len(data['availability'])):
    problem += pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_{m}"

#### Total Hour Constraints for Machine 1
problem += h_1 <= data['availability'][0], "Total_Hour_Constraint_1"

#### Profit Constraint
problem += total_revenue - total_machine_cost - overtime_cost >= data['min_profit'], "Profit_Constraint"

#### Solve the problem
problem.solve()

#### Outputs
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches}')
print(f'Total Profit: <OBJ>{total_profit}</OBJ>')
```

