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

\section*{Linear Programming Model}

Let:
\begin{itemize}
    \item \( P \) = number of different parts
    \item \( M \) = number of different machines
    \item \( batches_p \) = number of batches produced for part \( p \)
    \item \( time_{m,p} \) = hours required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \) = cost per hour of using machine \( m \)
    \item \( available_m \) = total available hours on machine \( m \) per month
    \item \( price_p \) = selling price per batch of part \( p \)
    \item \( min\_batches_p \) = minimum batches of part \( p \) that must be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \times batches_p) - \sum_{m=1}^{M} \left( cost_m \times \sum_{p=1}^{P} (time_{m,p} \times batches_p) \right)
\]

\subsection*{Constraints}
1. Production Constraints:
   \[
   batches_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
   \]
   
2. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} (time_{m,p} \times batches_p) \leq available_m \quad \forall m \in \{1, \ldots, M\}
   \]

3. Non-negativity Constraints:
   \[
   batches_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
   \]

\subsection*{Solution Variables}
The solution will provide:
\begin{itemize}
    \item \( batches_p \) = number of batches produced for part \( p \)
    \item \( total\_profit = Z \) = total profit obtained for the month
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

Let:
\begin{itemize}
    \item \( P \) = number of different parts
    \item \( M \) = number of different machines
    \item \( batches_p \) = number of batches produced for part \( p \)
    \item \( time_{m,p} \) = hours required on machine \( m \) to produce a batch of part \( p \)
    \item \( cost_m \) = cost per hour of using machine \( m \)
    \item \( available_m \) = total available hours on machine \( m \) per month
    \item \( price_p \) = selling price per batch of part \( p \)
    \item \( min\_batches_p \) = minimum batches of part \( p \) that must be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \times batches_p) - \sum_{m=1}^{M} \left( cost_m \times \sum_{p=1}^{P} (time_{m,p} \times batches_p) \right)
\]

\subsection*{Constraints}
1. Production Constraints:
   \[
   batches_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
   \]
   
2. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} (time_{m,p} \times batches_p) \leq available_m \quad \forall m \in \{1, \ldots, M\}
   \]

3. Non-negativity Constraints:
   \[
   batches_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
   \]

\subsection*{Solution Variables}
The solution will provide:
\begin{itemize}
    \item \( batches_p \) = number of batches produced for part \( p \)
    \item \( total\_profit = Z \) = total profit obtained for the month
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Define parameters
P = len(data['prices'])  #### Number of different parts
M = len(data['machine_costs'])  #### Number of different machines

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit_terms = [data['prices'][p] * batches[p] for p in range(P)]
cost_terms = [data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M)]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms), "Total_Profit"

#### Constraints
#### Minimum batches produced for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

