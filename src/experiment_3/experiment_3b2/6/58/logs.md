# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- Machine \var{1} requires a setup time of \var{setup_time_{p}} hours before it can be used for each part \var{p}.
- Other machines do not require a setup time.
- There are no minimum production quantities for any part.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "setup_time": [setup_time_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{setup_flags_{p}} indicates whether \var{part_{p}} is set up or not.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "setup_flags": [setup_flag_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem as a Mixed Integer Programming (MIP) problem, we need to define the decision variables, objective function, and constraints. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{align*}
& P = \text{set of parts (indexed by } p), \\
& M = \text{set of machines (indexed by } m).
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{time\_required}_{m,p} = \text{hours required by machine } m \text{ per batch of part } p, \\
& \text{cost}_{m} = \text{cost per hour for using machine } m, \\
& \text{available}_{m} = \text{available hours for machine } m \text{ per month}, \\
& \text{price}_{p} = \text{price per batch of part } p, \\
& \text{setup\_time}_{p} = \text{setup time required for machine 1 for part } p.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{batches}_{p} \in \mathbb{Z}_{\geq 0} = \text{number of batches to produce for part } p, \\
& \text{setup\_flag}_{p} \in \{0, 1\} = \text{1 if machine 1 is set up for part } p, \text{ 0 otherwise}.
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p \in P} \left( \text{price}_{p} \times \text{batches}_{p} \right) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \right) - \sum_{p \in P} \left( \text{setup\_time}_{p} \times \text{setup\_flag}_{p} \times \text{cost}_{1} \right)
\]

\subsection*{Constraints}
\begin{align*}
& \sum_{p \in P} \left( \text{time\_required}_{m,p} \times \text{batches}_{p} \right) + \delta_{m,1} \sum_{p \in P} \text{setup\_time}_{p} \times \text{setup\_flag}_{p} \leq \text{available}_{m}, \quad \forall m \in M, \\
& \text{setup\_flag}_{p} \leq \text{batches}_{p}, \quad \forall p \in P \quad (\text{setup only if producing}), \\
& \text{setup\_flag}_{p} \in \{0, 1\}, \quad \forall p \in P, \\
& \text{batches}_{p} \in \mathbb{Z}_{\geq 0}, \quad \forall p \in P.
\end{align*}

\end{document}
```

This formulation includes decision variables for the number of batches to produce for each part and binary variables to indicate whether a setup is performed for machine 1. The objective function aims to maximize the profit, considering both revenue from sales and costs of operations including setup times. Constraints ensure that machine hours do not exceed availability, and setups occur only if parts are produced.

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

\subsection*{Sets and Indices}
\begin{align*}
& P = \text{set of parts (indexed by } p), \\
& M = \text{set of machines (indexed by } m).
\end{align*}

\subsection*{Parameters}
\begin{align*}
& \text{time\_required}_{m,p} = \text{hours required by machine } m \text{ per batch of part } p, \\
& \text{cost}_{m} = \text{cost per hour for using machine } m, \\
& \text{available}_{m} = \text{available hours for machine } m \text{ per month}, \\
& \text{price}_{p} = \text{price per batch of part } p, \\
& \text{setup\_time}_{p} = \text{setup time required for machine 1 for part } p.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{batches}_{p} \in \mathbb{Z}_{\geq 0} = \text{number of batches to produce for part } p, \\
& \text{setup\_flag}_{p} \in \{0, 1\} = \text{1 if machine 1 is set up for part } p, \text{ 0 otherwise}.
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p \in P} \left( \text{price}_{p} \times \text{batches}_{p} \right) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \right) - \sum_{p \in P} \left( \text{setup\_time}_{p} \times \text{setup\_flag}_{p} \times \text{cost}_{1} \right)
\]

\subsection*{Constraints}
\begin{align*}
& \sum_{p \in P} \left( \text{time\_required}_{m,p} \times \text{batches}_{p} \right) + \delta_{m,1} \sum_{p \in P} \text{setup\_time}_{p} \times \text{setup\_flag}_{p} \leq \text{available}_{m}, \quad \forall m \in M, \\
& \text{setup\_flag}_{p} \leq \text{batches}_{p}, \quad \forall p \in P \quad (\text{setup only if producing}), \\
& \text{setup\_flag}_{p} \in \{0, 1\}, \quad \forall p \in P, \\
& \text{batches}_{p} \in \mathbb{Z}_{\geq 0}, \quad \forall p \in P.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

#### Sets and indices
P = range(len(data['prices']))  #### Parts
M = range(len(data['machine_costs']))  #### Machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", P, cat='Binary')

#### Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) for m in M) - \
         pulp.lpSum(data['setup_time'][p] * setup_flag[p] * data['machine_costs'][0] for p in P)

problem += profit

#### Constraints
for m in M:
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) +
                 (1 if m == 0 else 0) * pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in P) 
                 <= data['availability'][m], f"Availability_Constraint_Machine_{m}")

for p in P:
    problem += setup_flag[p] <= batches[p], f"Setup_Constraint_Part_{p}"

#### Solve the optimization problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

