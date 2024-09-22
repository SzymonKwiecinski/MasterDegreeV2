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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Problem Description}

We are tasked with determining the optimal number of batches of each part \( p \) to produce in order to maximize profit while adhering to machine availability and production constraints. The objective is to exceed a specified minimum profit.

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( P \): Set of parts, indexed by \( p \).
    \item \( M \): Set of machines, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time\_required}[m][p] \): Hours machine \( m \) needs to produce a batch of part \( p \).
    \item \( \text{machine\_costs}[m] \): Cost per hour for machine \( m \).
    \item \( \text{availability}[m] \): Total available hours per month for machine \( m \).
    \item \( \text{prices}[p] \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}[p] \): Minimum batches required for part \( p \).
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): Number of hours up to which standard cost applies for machine 1.
    \item \( \text{min\_profit} \): Minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches to produce for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{total\_profit} = \sum_{p \in P} \text{prices}[p] \times \text{batches}_{p} - \sum_{m \in M} \text{machine\_costs}[m] \sum_{p \in P} \text{time\_required}[m][p] \times \text{batches}_{p} - \text{Labor cost for machine 1}
\]

The labor cost for machine 1 is calculated as:
\[
\text{Labor cost for machine 1} = 
\begin{cases} 
\text{hours1} \times \text{standard\_cost}, & \text{if } \text{hours1} \leq \text{overtime\_hour} \\
\text{overtime\_hour} \times \text{standard\_cost} + (\text{hours1} - \text{overtime\_hour}) \times \text{overtime\_cost}, & \text{if } \text{hours1} > \text{overtime\_hour}
\end{cases}
\]
where 
\[
\text{hours1} = \sum_{p \in P} \text{time\_required}[1][p] \times \text{batches}_{p}
\]

\subsection*{Constraints}
1. Machine Time Availability:
   \[
   \sum_{p \in P} \text{time\_required}[m][p] \times \text{batches}_{p} \leq \text{availability}[m], \quad \forall m \in \{2, 3, \ldots, M\}
   \]
   For machine 1, the availability constraint is not considered due to outsourcing.

2. Minimum Batch Requirement:
   \[
   \text{batches}_{p} \geq \text{min\_batches}[p], \quad \forall p \in P
   \]

3. Minimum Profit Requirement:
   \[
   \text{total\_profit} \geq \text{min\_profit}
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

\subsection*{Problem Description}

We are tasked with determining the optimal number of batches of each part \( p \) to produce in order to maximize profit while adhering to machine availability and production constraints. The objective is to exceed a specified minimum profit.

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( P \): Set of parts, indexed by \( p \).
    \item \( M \): Set of machines, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time\_required}[m][p] \): Hours machine \( m \) needs to produce a batch of part \( p \).
    \item \( \text{machine\_costs}[m] \): Cost per hour for machine \( m \).
    \item \( \text{availability}[m] \): Total available hours per month for machine \( m \).
    \item \( \text{prices}[p] \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}[p] \): Minimum batches required for part \( p \).
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): Number of hours up to which standard cost applies for machine 1.
    \item \( \text{min\_profit} \): Minimum desired profit.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches to produce for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{total\_profit} = \sum_{p \in P} \text{prices}[p] \times \text{batches}_{p} - \sum_{m \in M} \text{machine\_costs}[m] \sum_{p \in P} \text{time\_required}[m][p] \times \text{batches}_{p} - \text{Labor cost for machine 1}
\]

The labor cost for machine 1 is calculated as:
\[
\text{Labor cost for machine 1} = 
\begin{cases} 
\text{hours1} \times \text{standard\_cost}, & \text{if } \text{hours1} \leq \text{overtime\_hour} \\
\text{overtime\_hour} \times \text{standard\_cost} + (\text{hours1} - \text{overtime\_hour}) \times \text{overtime\_cost}, & \text{if } \text{hours1} > \text{overtime\_hour}
\end{cases}
\]
where 
\[
\text{hours1} = \sum_{p \in P} \text{time\_required}[1][p] \times \text{batches}_{p}
\]

\subsection*{Constraints}
1. Machine Time Availability:
   \[
   \sum_{p \in P} \text{time\_required}[m][p] \times \text{batches}_{p} \leq \text{availability}[m], \quad \forall m \in \{2, 3, \ldots, M\}
   \]
   For machine 1, the availability constraint is not considered due to outsourcing.

2. Minimum Batch Requirement:
   \[
   \text{batches}_{p} \geq \text{min\_batches}[p], \quad \forall p \in P
   \]

3. Minimum Profit Requirement:
   \[
   \text{total\_profit} \geq \text{min\_profit}
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


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
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Define the sets
P = range(len(data['prices']))  #### Parts
M = range(len(data['machine_costs']))  #### Machines

#### Define the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Continuous')

#### Objective Function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
               pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) for m in M) - \
               pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) * data['standard_cost'] if pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) <= data['overtime_hour'] else \
               (data['overtime_hour'] * data['standard_cost'] + 
                (pulp.lpSum(data['time_required'][1][p] * batches[p] for p in P) - data['overtime_hour']) * data['overtime_cost'])

problem += total_profit, "Objective"

#### Constraints
#### Machine Time Availability for machines 2 and 3
for m in range(1, len(data['machine_costs'])):  #### skipping machine 1
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m], f"MachineAvailability_{m}"

#### Minimum Batch Requirement
for p in P:
    problem += batches[p] >= data['min_batches'][p], f"MinBatches_{p}"

#### Minimum Profit Requirement
problem += total_profit >= data['min_profit'], "MinProfit"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

