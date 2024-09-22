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

\section*{Mathematical Model}

\textbf{Sets:}
\begin{align*}
  & P = \text{set of parts, indexed by } p \\
  & M = \text{set of machines, indexed by } m \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
  & \text{time\_required}_{m,p} = \text{time required on machine } m \text{ for a batch of part } p \\
  & \text{cost}_{m} = \text{cost per hour for using machine } m \\
  & \text{available}_{m} = \text{hours available for machine } m \text{ per month} \\
  & \text{price}_{p} = \text{selling price per batch of part } p \\
  & \text{min\_batches}_{p} = \text{minimum number of batches for part } p \text{ required per month} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
  & \text{batches}_{p} = \text{number of batches of part } p \text{ produced (integer)} \\
\end{align*}

\textbf{Objective Function:}
Maximize the profit, which is revenue minus the cost:
\[
\text{max} \quad \text{total\_profit} = \sum_{p \in P} (\text{price}_{p} \times \text{batches}_{p}) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) \right)
\]

\textbf{Constraints:}
\begin{align*}
  & \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m \in M \quad \text{(machine availability constraint)} \\
  & \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in P \quad \text{(minimum production requirement)} \\
  & \text{batches}_{p} \in \mathbb{Z}^{+}, \quad \forall p \in P \quad \text{(non-negativity and integrality)}
\end{align*}

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

\section*{Mathematical Model}

\textbf{Sets:}
\begin{align*}
  & P = \text{set of parts, indexed by } p \\
  & M = \text{set of machines, indexed by } m \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
  & \text{time\_required}_{m,p} = \text{time required on machine } m \text{ for a batch of part } p \\
  & \text{cost}_{m} = \text{cost per hour for using machine } m \\
  & \text{available}_{m} = \text{hours available for machine } m \text{ per month} \\
  & \text{price}_{p} = \text{selling price per batch of part } p \\
  & \text{min\_batches}_{p} = \text{minimum number of batches for part } p \text{ required per month} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
  & \text{batches}_{p} = \text{number of batches of part } p \text{ produced (integer)} \\
\end{align*}

\textbf{Objective Function:}
Maximize the profit, which is revenue minus the cost:
\[
\text{max} \quad \text{total\_profit} = \sum_{p \in P} (\text{price}_{p} \times \text{batches}_{p}) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) \right)
\]

\textbf{Constraints:}
\begin{align*}
  & \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m \in M \quad \text{(machine availability constraint)} \\
  & \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in P \quad \text{(minimum production requirement)} \\
  & \text{batches}_{p} \in \mathbb{Z}^{+}, \quad \forall p \in P \quad \text{(non-negativity and integrality)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


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
    'min_batches': [10, 10, 10, 10]
}

#### Define sets
P = range(len(data['prices']))  #### set of parts
M = range(len(data['machine_costs']))  #### set of machines

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Integer')

#### Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) 
                     for m in M)

problem += profit, "Total_Profit"

#### Constraints
for m in M:
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m], f"Machine_Availability_{m}"

for p in P:
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

