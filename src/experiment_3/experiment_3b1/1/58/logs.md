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

\section*{Mathematical Model for Auto Parts Manufacturer}

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( time_{m,p} \) be the time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item Let \( cost_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( available_{m} \) be the available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price per batch of part \( p \).
    \item Let \( setup\_time_{p} \) be the setup time (in hours) required for machine 1 before producing part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( batches_{p} \) be the number of batches produced for part \( p \).
    \item Let \( setup\_flag_{p} \) be a binary variable indicating whether part \( p \) is set up (1 if yes, 0 if no).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]
    
    \item Setup time constraint for machine 1 (only for parts that are set up):
    \[
    \sum_{p=1}^{P} (setup\_flag_{p} \cdot setup\_time_{p}) \leq available_{1}
    \]

    \item Non-negativity and integrality constraints:
    \[
    batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
    \[
    setup\_flag_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\subsection*{Output}
The output of the model will include:
\begin{itemize}
    \item \( batches = [batches_{p} \text{ for } p = 1, \ldots, P] \)
    \item \( setup\_flags = [setup\_flag_{p} \text{ for } p = 1, \ldots, P] \)
    \item \( total\_profit = Z \)
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

\section*{Mathematical Model for Auto Parts Manufacturer}

\subsection*{Sets}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( time_{m,p} \) be the time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item Let \( cost_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( available_{m} \) be the available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price per batch of part \( p \).
    \item Let \( setup\_time_{p} \) be the setup time (in hours) required for machine 1 before producing part \( p \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( batches_{p} \) be the number of batches produced for part \( p \).
    \item Let \( setup\_flag_{p} \) be a binary variable indicating whether part \( p \) is set up (1 if yes, 0 if no).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]
    
    \item Setup time constraint for machine 1 (only for parts that are set up):
    \[
    \sum_{p=1}^{P} (setup\_flag_{p} \cdot setup\_time_{p}) \leq available_{1}
    \]

    \item Non-negativity and integrality constraints:
    \[
    batches_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
    \[
    setup\_flag_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\subsection*{Output}
The output of the model will include:
\begin{itemize}
    \item \( batches = [batches_{p} \text{ for } p = 1, \ldots, P] \)
    \item \( setup\_flags = [setup\_flag_{p} \text{ for } p = 1, \ldots, P] \)
    \item \( total\_profit = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

#### Parameters
time_required = data['time_required']  #### Machine time required for each part
machine_costs = data['machine_costs']  #### Cost per hour for each machine
availability = data['availability']      #### Available hours per month for each machine
prices = data['prices']                  #### Selling price per batch of part
setup_time = data['setup_time']          #### Setup time for each part

P = len(prices)     #### Number of different parts
M = len(machine_costs)  #### Number of different machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit

#### Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m])

#### Setup time constraint for machine 1
problem += (pulp.lpSum([setup_flags[p] * setup_time[p] for p in range(P)]) <= availability[0])

#### Solve the problem
problem.solve()

#### Output results
batches_solution = [batches[p].varValue for p in range(P)]
setup_flags_solution = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches_solution}')
print(f'Setup flags: {setup_flags_solution}')
print(f'Total Profit: <OBJ>{total_profit}</OBJ>')
```

