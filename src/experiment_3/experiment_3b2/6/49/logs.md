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

\section*{Mathematical Model for Maximizing Profit}

\textbf{Sets:}
\begin{itemize}
    \item Let \( P \) be the set of parts produced, indexed by \( p \).
    \item Let \( M \) be the set of machines, indexed by \( m \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{availability}_{m} \): Hours available per month on machine \( m \).
    \item \( \text{prices}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) to be produced.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches of part \( p \) to be produced.
\end{itemize}

\textbf{Objective:}

Maximize the total profit, which is the difference between total revenue and total cost:

\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p \in P} \left( \text{prices}_{p} \times \text{batches}_{p} \right) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \right)
\]

\textbf{Constraints:}

\begin{enumerate}
    \item Machine time availability constraints for all machines except \( m = M \) and \( m = M-1 \):
    \[
    \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{availability}_{m}, \quad \forall m \in \{1, \ldots, M-2\}
    \]

    \item Combined availability constraint for machines \( M \) and \( M-1 \):
    \[
    \sum_{p \in P} \left( \text{time\_required}_{M,p} \times \text{batches}_{p} + \text{time\_required}_{M-1,p} \times \text{batches}_{p} \right) \leq \text{availability}_{M} + \text{availability}_{M-1}
    \]

    \item Minimum production requirements:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in P
    \]

    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p \in P
    \]
\end{enumerate}

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

\section*{Mathematical Model for Maximizing Profit}

\textbf{Sets:}
\begin{itemize}
    \item Let \( P \) be the set of parts produced, indexed by \( p \).
    \item Let \( M \) be the set of machines, indexed by \( m \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{availability}_{m} \): Hours available per month on machine \( m \).
    \item \( \text{prices}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) to be produced.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches of part \( p \) to be produced.
\end{itemize}

\textbf{Objective:}

Maximize the total profit, which is the difference between total revenue and total cost:

\[
\text{Maximize} \quad \text{total\_profit} = \sum_{p \in P} \left( \text{prices}_{p} \times \text{batches}_{p} \right) - \sum_{m \in M} \left( \text{cost}_{m} \times \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \right)
\]

\textbf{Constraints:}

\begin{enumerate}
    \item Machine time availability constraints for all machines except \( m = M \) and \( m = M-1 \):
    \[
    \sum_{p \in P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{availability}_{m}, \quad \forall m \in \{1, \ldots, M-2\}
    \]

    \item Combined availability constraint for machines \( M \) and \( M-1 \):
    \[
    \sum_{p \in P} \left( \text{time\_required}_{M,p} \times \text{batches}_{p} + \text{time\_required}_{M-1,p} \times \text{batches}_{p} \right) \leq \text{availability}_{M} + \text{availability}_{M-1}
    \]

    \item Minimum production requirements:
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p \in P
    \]

    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p \in P
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]  #### time required for each machine and part
machine_costs = [160, 10, 15]  #### costs per hour for each machine
availability = [200, 300, 500]  #### available hours for each machine
prices = [570, 250, 585, 430]  #### selling prices for each part
min_batches = [10, 10, 10, 10]  #### minimum batches for each part

#### Set up the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
parts = range(len(prices))  #### parts indexed by p
batches = pulp.LpVariable.dicts("batches", parts, lowBound=0)  #### batches of parts to produce

#### Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in parts)
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in parts) for m in range(len(machine_costs)))
problem += revenue - cost, "Total_Profit"

#### Constraints
#### Machine time availability constraints for machines 1 to M-2
for m in range(len(machine_costs) - 2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in parts) <= availability[m], f"Machine_{m+1}_availability"

#### Combined availability constraint for machines M and M-1
problem += pulp.lpSum((time_required[-2][p] + time_required[-1][p]) * batches[p] for p in parts) <= availability[-2] + availability[-1], "Combined_availability"

#### Minimum production requirements
for p in parts:
    problem += batches[p] >= min_batches[p], f"Min_batches_for_part_{p+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

