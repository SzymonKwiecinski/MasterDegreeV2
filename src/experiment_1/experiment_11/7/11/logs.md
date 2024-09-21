# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Optimal Trading Strategy}

\subsection*{Parameters}
\begin{itemize}
    \item $Capacity$: Maximum storage capacity (constant)
    \item $HoldingCost$: Cost of holding one unit of product (constant)
    \item $Price_t$: Selling price in period $t$, for $t = 1, \ldots, N$
    \item $Cost_t$: Cost of buying in period $t$, for $t = 1, \ldots, N$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $B_t$: Quantity of goods bought in period $t$, for $t = 1, \ldots, N$
    \item $S_t$: Quantity of goods sold in period $t$, for $t = 1, \ldots, N$
    \item $I_t$: Inventory level at the end of period $t$, for $t = 1, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over the months:
\[
\max \sum_{t=1}^{N} \left( Price_t \cdot S_t - Cost_t \cdot B_t - HoldingCost \cdot I_t \right)
\]

\subsection*{Constraints}
\begin{align}
    & I_t \geq 0 \quad \forall t = 1, \ldots, N & \text{(Non-negative inventory)} \\
    & S_t \geq 0 \quad \forall t = 1, \ldots, N & \text{(Non-negative sales)} \\
    & B_t \geq 0 \quad \forall t = 1, \ldots, N & \text{(Non-negative purchases)} \\
    & I_t \leq Capacity \quad \forall t = 1, \ldots, N & \text{(Storage capacity)} \\
    & I_t = I_{t-1} + B_t - S_t \quad \forall t = 1, \ldots, N & \text{(Inventory balance)} \\
    & I_0 = 0 & \text{(Initial inventory)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])

#### Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

#### Decision variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]  #### Buy quantities
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]  #### Sell quantities
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]  #### Inventory levels

#### Objective function
profit = pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))
problem += profit, "Total_Profit"

#### Constraints
#### Initial inventory
problem += (I[0] == 0, "Initial_Inventory")

#### Inventory balance and capacity constraints
for t in range(N):
    if t > 0:
        problem += (I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}")
    problem += (I[t] <= data['capacity'], f"Storage_Capacity_{t}")  #### Storage capacity
    problem += (S[t] >= 0, f"Non_Negative_Sales_{t}")  #### Non-negative sales
    problem += (B[t] >= 0, f"Non_Negative_Purchases_{t}")  #### Non-negative purchases
    problem += (I[t] >= 0, f"Non_Negative_Inventory_{t}")  #### Non-negative inventory

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

