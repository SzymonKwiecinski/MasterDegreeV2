# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Alloy Production}

\subsection*{Objective}
Minimize the total cost of the alloys used in the production:
\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{Price}_k \cdot x_k
\]

\subsection*{Constraints}
1. The total quantity of alloys produced is exactly \(\text{AlloyQuantity}\):
\[
\sum_{k=1}^{K} x_k = \text{AlloyQuantity}
\]

2. The quantity of each target component in the alloy must be met or exceeded:
\[
\sum_{k=1}^{K} \text{Ratio}_{k,m} \cdot x_k \geq \text{Target}_m \quad \forall m \in \{1, 2, \ldots, M\}
\]

3. The quantity of component \(k\) in alloy \(m\) must adhere to the specified \(\text{Ratio}\):
\[
\text{Ratio}_{k,m} \cdot x_k \quad \text{(implicitly included in the above constraint)}
\]

4. Each alloy's quantity is non-negative:
\[
x_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Parameters}
\begin{itemize}
    \item \(\text{AlloyQuantity}\): Total quantity of alloy to produce (constant)
    \item \(\text{Target}_m\): Quantity of target components in the alloy for each \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Ratio}_{k,m}\): Ratio of each component \(k\) in the alloy \(m\) for each \(k \in \{1, 2, \ldots, K\}\) and \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Price}_k\): Price of each alloy \(k\) for each \(k \in \{1, 2, \ldots, K\}\)
\end{itemize}

\subsection*{Decision Variables}
\[
x_k \quad \text{(quantity of alloy } k \text{ to produce)}
\]

\end{document}</MATH_MODEL>
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Parameters
AlloyQuantity = data['alloy_quant']
Target = data['target']
Ratio = data['ratio']
Price = data['price']

#### Number of alloys and components
K = len(Price)  #### number of alloys
M = len(Target)  #### number of target components

#### Create the problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### x[k] >= 0

#### Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
#### 1. Total quantity of alloys produced is exactly AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(K)) == AlloyQuantity, "Total_Alloy_Quantity"

#### 2. Each target component requirement must be met or exceeded
for m in range(M):
    problem += pulp.lpSum(Ratio[k][m] * x[k] for k in range(K)) >= Target[m], f"Target_Requirement_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

