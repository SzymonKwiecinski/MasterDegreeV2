# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Wild Sports produces \var{M} different products using \var{N} different raw materials.
- The company has \var{available_{i}} of raw material \var{i} available.
- Product \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Product \var{j} has a selling price of \var{price_j} per unit.
- Product \var{j} has a production cost of \var{cost_j} per unit produced.
- Product \var{j} has a forecasted maximum demand of \var{demand_j} for the month.

INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}

OBJECTIVE: How many of each product should the sports produce in order to maximize its profit for the month?

OUTPUT INFO:

- the amount of each product produced \var{amount_{j}}.
- \var{total_profit} shows the total profit of the company for the month.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\textbf{Sets:}
\begin{itemize}
    \item Let \( M \) be the number of products.
    \item Let \( N \) be the number of raw materials.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_i \): Amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): Amount of raw material \( i \) required to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{price}_j \): Selling price of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{cost}_j \): Production cost of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{demand}_j \): Maximum forecasted demand for product \( j \) for \( j = 1, \ldots, M \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( \text{amount}_j \) be the amount of product \( j \) produced for \( j = 1, \ldots, M \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{j=1}^{M} \left( \text{price}_j \cdot \text{amount}_j - \text{cost}_j \cdot \text{amount}_j \right)
\]
which simplifies to:
\[
Z = \sum_{j=1}^{M} \left( (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j \right)
\]

\textbf{Constraints:}
\begin{itemize}
    \item Raw material constraints:
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i \quad \forall i = 1, \ldots, N
    \]
    \item Demand constraints:
    \[
    \text{amount}_j \leq \text{demand}_j \quad \forall j = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    \text{amount}_j \geq 0 \quad \forall j = 1, \ldots, M
    \end{itemize}
\]

\textbf{Output:}
\begin{itemize}
    \item The optimal amount of each product produced: \( \text{amount}_j \) for \( j = 1, \ldots, M \).
    \item The total profit: \( Z \).
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

\section*{Linear Programming Model for Wild Sports}

\textbf{Sets:}
\begin{itemize}
    \item Let \( M \) be the number of products.
    \item Let \( N \) be the number of raw materials.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{available}_i \): Amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): Amount of raw material \( i \) required to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{price}_j \): Selling price of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{cost}_j \): Production cost of product \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{demand}_j \): Maximum forecasted demand for product \( j \) for \( j = 1, \ldots, M \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( \text{amount}_j \) be the amount of product \( j \) produced for \( j = 1, \ldots, M \).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{j=1}^{M} \left( \text{price}_j \cdot \text{amount}_j - \text{cost}_j \cdot \text{amount}_j \right)
\]
which simplifies to:
\[
Z = \sum_{j=1}^{M} \left( (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j \right)
\]

\textbf{Constraints:}
\begin{itemize}
    \item Raw material constraints:
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i \quad \forall i = 1, \ldots, N
    \]
    \item Demand constraints:
    \[
    \text{amount}_j \leq \text{demand}_j \quad \forall j = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    \text{amount}_j \geq 0 \quad \forall j = 1, \ldots, M
    \end{itemize}
\]

\textbf{Output:}
\begin{itemize}
    \item The optimal amount of each product produced: \( \text{amount}_j \) for \( j = 1, \ldots, M \).
    \item The total profit: \( Z \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)  #### Number of products
N = len(available)  #### Number of raw materials

#### Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective function
profit = pulp.lpSum((prices[j] - costs[j]) * amounts[j] for j in range(M))
problem += profit

#### Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amounts[j] for j in range(M)) <= available[i]

#### Constraints for demand
for j in range(M):
    problem += amounts[j] <= demands[j]

#### Solve the problem
problem.solve()

#### Print the output
for j in range(M):
    print(f'Optimal amount of product {j}: {amounts[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

