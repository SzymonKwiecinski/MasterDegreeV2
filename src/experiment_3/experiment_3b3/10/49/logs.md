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
- Machine \var{M} and Machine \var{M-1} can share availability.
- Individual availability conditions for Machine \var{M} and Machine \var{M-1} can be disregarded.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Variables}
Let \(b_p\) be the number of batches produced of part \(p\), where \(p = 1, 2, \ldots, P\).  
Let \(T\) be the total profit.

\subsection*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): time required on machine \(m\) to produce one batch of part \(p\) (in hours).
    \item \(cost_{m}\): cost per hour of using machine \(m\).
    \item \(available_{m}\): availability of machine \(m\) (in hours) per month.
    \item \(price_{p}\): selling price per batch of part \(p\).
    \item \(min\_batches_{p}\): minimum number of batches that must be produced for part \(p\) to fulfill a contract.
\end{itemize}  

\subsection*{Objective Function}
The objective is to maximize the total profit \(T\), which can be expressed as:
\[
T = \sum_{p=1}^{P} (price_{p} \cdot b_{p} - \sum_{m=1}^{M} cost_{m} \cdot \frac{time_{m,p}}{100} \cdot b_{p})
\]

\subsection*{Constraints}
1. **Production Constraints**: Each part must meet the minimum production requirement:
   \[
   b_{p} \geq min\_batches_{p}, \quad \forall p
   \]

2. **Machine Availability Constraints**: The total time used on all machines for all produced parts must not exceed the available time:
   \[
   \sum_{p=1}^{P} \sum_{m=1}^{M} time_{m,p} \cdot b_{p} \leq \sum_{m=1}^{M} available_{m}
   \]

3. **Non-negativity Constraints**: The number of batches produced must be non-negative:
   \[
   b_{p} \geq 0, \quad \forall p
   \]

\subsection*{Output}
The solution will yield the batch quantities:
\[
\text{Output: } \{batches = [b_{p} \text{ for } p = 1, \ldots, P], \, total\_profit = T \}
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Variables}
Let \(b_p\) be the number of batches produced of part \(p\), where \(p = 1, 2, \ldots, P\).  
Let \(T\) be the total profit.

\subsection*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): time required on machine \(m\) to produce one batch of part \(p\) (in hours).
    \item \(cost_{m}\): cost per hour of using machine \(m\).
    \item \(available_{m}\): availability of machine \(m\) (in hours) per month.
    \item \(price_{p}\): selling price per batch of part \(p\).
    \item \(min\_batches_{p}\): minimum number of batches that must be produced for part \(p\) to fulfill a contract.
\end{itemize}  

\subsection*{Objective Function}
The objective is to maximize the total profit \(T\), which can be expressed as:
\[
T = \sum_{p=1}^{P} (price_{p} \cdot b_{p} - \sum_{m=1}^{M} cost_{m} \cdot \frac{time_{m,p}}{100} \cdot b_{p})
\]

\subsection*{Constraints}
1. **Production Constraints**: Each part must meet the minimum production requirement:
   \[
   b_{p} \geq min\_batches_{p}, \quad \forall p
   \]

2. **Machine Availability Constraints**: The total time used on all machines for all produced parts must not exceed the available time:
   \[
   \sum_{p=1}^{P} \sum_{m=1}^{M} time_{m,p} \cdot b_{p} \leq \sum_{m=1}^{M} available_{m}
   \]

3. **Non-negativity Constraints**: The number of batches produced must be non-negative:
   \[
   b_{p} \geq 0, \quad \forall p
   \]

\subsection*{Output}
The solution will yield the batch quantities:
\[
\text{Output: } \{batches = [b_{p} \text{ for } p = 1, \ldots, P], \, total\_profit = T \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

#### Constants
num_parts = len(prices)
num_machines = len(machine_costs)

#### Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f"b_{p}", lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]

#### Objective Function
profit_terms = [
    prices[p] * batches[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(num_machines))
    for p in range(num_parts)
]
problem += pulp.lpSum(profit_terms), "Total_Profit"

#### Machine Availability Constraints
for m in range(num_machines):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m],
        f"Machine_{m}_Availability"
    )

#### Solve the problem
problem.solve()

#### Output the results
batches_solution = [pulp.value(b) for b in batches]
print("Optimal batch quantities:")
for p, batch_count in enumerate(batches_solution):
    print(f"Part {p + 1}: {batch_count:.2f} batches")

print(f'Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

