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
To formulate this problem as a linear program, we need to define the decision variables, the objective function, and the constraints based on the given information.

**Decision Variables:**

- Let \( x_p \) be the number of batches of part \( p \) produced. Here, \( p = 1, 2, \ldots, P \).

**Objective Function:**

- We aim to maximize the total profit. The profit for each part is the sales revenue minus the cost of using the machines. The objective function becomes:

\[
\text{Maximize } \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_p \right) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_{m} \right)
\]

**Constraints:**

1. **Machine Time Constraints:**
   - For each machine \( m \) except for the last two machines, we maintain the constraint on the maximum available hours:

\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} \quad \text{for } m = 1, 2, \ldots, M-2
\]

2. **Shared Availability for Last Two Machines:**
   - Machine \( M \) and \( M-1 \) can share availability, thus:

\[
\sum_{p=1}^{P} \text{time}_{M-1,p} \cdot x_p + \sum_{p=1}^{P} \text{time}_{M,p} \cdot x_p \leq \text{available}_{M-1} + \text{available}_{M}
\]

3. **Minimum Production Requirements:**

\[
x_p \geq \text{min_batches}_{p} \quad \text{for } p = 1, 2, \ldots, P
\]

4. **Non-negativity Constraints:**

\[
x_p \geq 0 \quad \text{for } p = 1, 2, \ldots, P
\]

Now, let's express the above information in the form of a LaTeX document:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables:}
\[
x_p \text{ : Number of batches of part } p \text{ produced, for } p = 1, 2, \ldots, P
\]

\subsection*{Objective Function:}
\[
\text{Maximize } \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_{m} \right)
\]

\subsection*{Constraints:}

\begin{itemize}
    \item \textbf{Machine Time Constraints:}
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m}, \quad m = 1, 2, \ldots, M-2
    \]

    \item \textbf{Shared Availability for Last Two Machines:}
    \[
    \sum_{p=1}^{P} \text{time}_{M-1,p} \cdot x_p + \sum_{p=1}^{P} \text{time}_{M,p} \cdot x_p \leq \text{available}_{M-1} + \text{available}_{M}
    \]

    \item \textbf{Minimum Production Requirements:}
    \[
    x_p \geq \text{min_batches}_{p}, \quad p = 1, 2, \ldots, P
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    x_p \geq 0, \quad p = 1, 2, \ldots, P
    \]
\end{itemize}

\end{document}
```

This mathematical model captures the essence of the problem and serves as a foundation for solving it using linear programming techniques.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables:}
\[
x_p \text{ : Number of batches of part } p \text{ produced, for } p = 1, 2, \ldots, P
\]

\subsection*{Objective Function:}
\[
\text{Maximize } \sum_{p=1}^{P} (\text{price}_{p} \cdot x_p) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \cdot \text{cost}_{m} \right)
\]

\subsection*{Constraints:}

\begin{itemize}
    \item \textbf{Machine Time Constraints:}
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m}, \quad m = 1, 2, \ldots, M-2
    \]

    \item \textbf{Shared Availability for Last Two Machines:}
    \[
    \sum_{p=1}^{P} \text{time}_{M-1,p} \cdot x_p + \sum_{p=1}^{P} \text{time}_{M,p} \cdot x_p \leq \text{available}_{M-1} + \text{available}_{M}
    \]

    \item \textbf{Minimum Production Requirements:}
    \[
    x_p \geq \text{min_batches}_{p}, \quad p = 1, 2, \ldots, P
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    x_p \geq 0, \quad p = 1, 2, \ldots, P
    \]
\end{itemize}

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

#### Extracting values from data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Defining parameters
P = len(prices)  #### Number of parts
M = len(availability)  #### Number of machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

#### Objective function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))

problem += profit

#### Constraints for machine time
for m in range(M - 2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

#### Shared availability for the last two machines
problem += pulp.lpSum(time_required[M - 2][p] * x[p] for p in range(P)) + \
           pulp.lpSum(time_required[M - 1][p] * x[p] for p in range(P)) <= availability[M - 2] + availability[M - 1]

#### Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

