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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Auto Parts Manufacturing Problem}

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the total number of parts.
    \item Let \( M \) be the total number of machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): hours required on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): available hours per month for machine \( m \).
    \item \( \text{price}_{p} \): selling price per batch of part \( p \).
    \item \( \text{setup\_time}_{p} \): setup time required for machine 1 for part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): number of batches produced for part \( p \).
    \item \( \text{setup\_flag}_{p} \): binary variable indicating whether part \( p \) is set up on machine 1 (1 if set up, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine Availability Constraints:} \\
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, & \quad \forall m \in \{1, 2, \ldots, M\} \\
\\
\text{Setup Time Constraint for Machine 1:} \\
\text{setup\_flag}_{p} \cdot \text{setup\_time}_{p} + \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \leq \text{available}_{1}, & \quad \text{for each } p \in \{1, 2, \ldots, P\} \\
\\
\text{Non-negativity and binary constraints:} \\
\text{batches}_{p} \geq 0, & \quad \forall p \in \{1, 2, \ldots, P\} \\
\text{setup\_flag}_{p} \in \{0, 1\}, & \quad \forall p \in \{1, 2, \ldots, P\}
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

\section*{Mathematical Model for Auto Parts Manufacturing Problem}

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the total number of parts.
    \item Let \( M \) be the total number of machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): hours required on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): available hours per month for machine \( m \).
    \item \( \text{price}_{p} \): selling price per batch of part \( p \).
    \item \( \text{setup\_time}_{p} \): setup time required for machine 1 for part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): number of batches produced for part \( p \).
    \item \( \text{setup\_flag}_{p} \): binary variable indicating whether part \( p \) is set up on machine 1 (1 if set up, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine Availability Constraints:} \\
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, & \quad \forall m \in \{1, 2, \ldots, M\} \\
\\
\text{Setup Time Constraint for Machine 1:} \\
\text{setup\_flag}_{p} \cdot \text{setup\_time}_{p} + \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \leq \text{available}_{1}, & \quad \text{for each } p \in \{1, 2, \ldots, P\} \\
\\
\text{Non-negativity and binary constraints:} \\
\text{batches}_{p} \geq 0, & \quad \forall p \in \{1, 2, \ldots, P\} \\
\text{setup\_flag}_{p} \in \{0, 1\}, & \quad \forall p \in \{1, 2, \ldots, P\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}'''

#### Loading data from JSON
data = json.loads(data_json)

#### Defining sets
P = len(data['prices'])  #### Total number of parts
M = len(data['machine_costs'])  #### Total number of machines

#### Defining the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total Profit"

#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_Constraint_Machine_{m+1}"

#### Setup Time Constraint for Machine 1
for p in range(P):
    problem += setup_flag[p] * data['setup_time'][p] + pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P)) <= data['availability'][0], f"Setup_Time_Constraint_Part_{p+1}"

#### Solving the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

