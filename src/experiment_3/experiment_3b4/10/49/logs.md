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

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A division of an auto parts manufacturer produces different parts using various machines. Each part, when produced in a batch of 100, requires a specific amount of time on each machine. The division incurs a cost for using the machines, which have limited availability per month. Some machines can share their availability, simplifying the constraints. The objective is to determine the number of batches of each part to produce monthly to maximize profit, ensuring contractual obligations are met.

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{align*}
& P: \text{Set of parts, indexed by } p \\
& M: \text{Set of machines, indexed by } m 
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{time}_{m,p}: \text{Time required on machine } m \text{ to produce a batch of part } p \\
& \text{cost}_{m}: \text{Cost per hour of using machine } m \\
& \text{available}_{m}: \text{Available hours per month for machine } m \\
& \text{price}_{p}: \text{Selling price per batch of part } p \\
& \text{min\_batches}_{p}: \text{Minimum batches of part } p \text{ required per month}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{batches}_{p}: \text{Number of batches of part } p \text{ to produce}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Profit} = & \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) \\
& - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m}, \quad \forall m \in \{1, \ldots, M-2\} \\
& \sum_{p=1}^{P} \left( \text{time}_{M-1,p} \cdot \text{batches}_{p} \right) + \sum_{p=1}^{P} \left( \text{time}_{M,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{M-1} + \text{available}_{M} \\
& \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in \{1, \ldots, P\}
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

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Problem Description}

A division of an auto parts manufacturer produces different parts using various machines. Each part, when produced in a batch of 100, requires a specific amount of time on each machine. The division incurs a cost for using the machines, which have limited availability per month. Some machines can share their availability, simplifying the constraints. The objective is to determine the number of batches of each part to produce monthly to maximize profit, ensuring contractual obligations are met.

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{align*}
& P: \text{Set of parts, indexed by } p \\
& M: \text{Set of machines, indexed by } m 
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{time}_{m,p}: \text{Time required on machine } m \text{ to produce a batch of part } p \\
& \text{cost}_{m}: \text{Cost per hour of using machine } m \\
& \text{available}_{m}: \text{Available hours per month for machine } m \\
& \text{price}_{p}: \text{Selling price per batch of part } p \\
& \text{min\_batches}_{p}: \text{Minimum batches of part } p \text{ required per month}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{batches}_{p}: \text{Number of batches of part } p \text{ to produce}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Profit} = & \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) \\
& - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m}, \quad \forall m \in \{1, \ldots, M-2\} \\
& \sum_{p=1}^{P} \left( \text{time}_{M-1,p} \cdot \text{batches}_{p} \right) + \sum_{p=1}^{P} \left( \text{time}_{M,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{M-1} + \text{available}_{M} \\
& \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in \{1, \ldots, P\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
}

num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

#### Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f"batches_{p}", lowBound=data['min_batches'][p], cat='Continuous') for p in range(num_parts)]

#### Objective function
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(num_parts))
cost = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                  for m in range(num_machines) for p in range(num_parts))

problem += revenue - cost, "Total Profit"

#### Constraints
#### Machine constraints for machines 1 to M-2
for m in range(num_machines - 2):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts)) <= data['availability'][m], f"Machine_{m+1}_Constraint"

#### Combined constraint for the last two machines
problem += (
    pulp.lpSum(data['time_required'][num_machines - 2][p] * batches[p] for p in range(num_parts)) +
    pulp.lpSum(data['time_required'][num_machines - 1][p] * batches[p] for p in range(num_parts)) <= 
    data['availability'][num_machines - 2] + data['availability'][num_machines - 1],
    "Combined_Machine_Constraint"
)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

