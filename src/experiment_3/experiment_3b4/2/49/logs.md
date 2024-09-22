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

\section*{Mathematical Model}

Let \( P \) be the number of different parts and \( M \) be the number of different machines. Define the following variables and parameters:

\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time in hours required on machine \( m \) to produce a batch of 100 part \( p \).
    \item \( \text{cost}_{m} \): Cost in dollars per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Availability in hours per month for machine \( m \).
    \item \( \text{price}_{p} \): Selling price in dollars per batch of 100 part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) required to be produced each month.
    \item \( \text{batches}_{p} \): Decision variable representing the number of batches of part \( p \) to produce.
\end{itemize}

\subsection*{Objective Function}

The objective is to maximize the total profit. The profit is the total revenue from selling the parts minus the total cost of using the machines. Therefore, the objective function is:

\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p=1}^{P} (\text{price}_{p} \cdot \text{batches}_{p}) - \sum_{m=1}^{M} \sum_{p=1}^{P} (\text{cost}_{m} \cdot \text{time\_required}_{m,p} \cdot \text{batches}_{p})
\]

\subsection*{Constraints}

1. **Minimum Batch Requirement:**

   For each part, ensure that at least the minimum required batches are produced:
   \[
   \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
   \]

2. **Machine Availability Constraints:**

   For each machine, ensure that the total time used does not exceed available time:
   \[
   \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M-2
   \]

   For the last two machines, they can share availability:
   \[
   \sum_{p=1}^{P} (\text{time\_required}_{M,p} \cdot \text{batches}_{p}) + \sum_{p=1}^{P} (\text{time\_required}_{M-1,p} \cdot \text{batches}_{p}) \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Non-negativity:**

   \[
   \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
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

\section*{Mathematical Model}

Let \( P \) be the number of different parts and \( M \) be the number of different machines. Define the following variables and parameters:

\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time in hours required on machine \( m \) to produce a batch of 100 part \( p \).
    \item \( \text{cost}_{m} \): Cost in dollars per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Availability in hours per month for machine \( m \).
    \item \( \text{price}_{p} \): Selling price in dollars per batch of 100 part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) required to be produced each month.
    \item \( \text{batches}_{p} \): Decision variable representing the number of batches of part \( p \) to produce.
\end{itemize}

\subsection*{Objective Function}

The objective is to maximize the total profit. The profit is the total revenue from selling the parts minus the total cost of using the machines. Therefore, the objective function is:

\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p=1}^{P} (\text{price}_{p} \cdot \text{batches}_{p}) - \sum_{m=1}^{M} \sum_{p=1}^{P} (\text{cost}_{m} \cdot \text{time\_required}_{m,p} \cdot \text{batches}_{p})
\]

\subsection*{Constraints}

1. **Minimum Batch Requirement:**

   For each part, ensure that at least the minimum required batches are produced:
   \[
   \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
   \]

2. **Machine Availability Constraints:**

   For each machine, ensure that the total time used does not exceed available time:
   \[
   \sum_{p=1}^{P} (\text{time\_required}_{m,p} \cdot \text{batches}_{p}) \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M-2
   \]

   For the last two machines, they can share availability:
   \[
   \sum_{p=1}^{P} (\text{time\_required}_{M,p} \cdot \text{batches}_{p}) + \sum_{p=1}^{P} (\text{time\_required}_{M-1,p} \cdot \text{batches}_{p}) \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Non-negativity:**

   \[
   \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
   \]

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
    'min_batches': [10, 10, 10, 10]
}

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(len(data['prices']))]

#### Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(len(data['prices'])))
total_cost = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                        for m in range(len(data['machine_costs'])) 
                        for p in range(len(data['prices'])))

problem += total_revenue - total_cost, "Total_Profit"

#### Constraints
#### Minimum Batch Requirement
for p in range(len(data['prices'])):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

#### Machine Availability Constraints
for m in range(len(data['machine_costs']) - 2):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(len(data['prices'])))
                <= data['availability'][m]), f"Availability_Constraint_{m}"

#### Shared availability for last two machines
problem += (pulp.lpSum(data['time_required'][len(data['machine_costs'])-1][p] * batches[p] for p in range(len(data['prices']))) + 
            pulp.lpSum(data['time_required'][len(data['machine_costs'])-2][p] * batches[p] for p in range(len(data['prices'])))
            <= data['availability'][len(data['machine_costs'])-1] + data['availability'][len(data['machine_costs'])-2]), "Shared_Availability_Constraint"

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

