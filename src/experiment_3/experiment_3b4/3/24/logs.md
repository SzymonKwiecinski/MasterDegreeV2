# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a Mixed-Integer Programming (MIP) model, we need to define decision variables and constraints that align with the problem's requirements. Below is a mathematical formulation in LaTeX code:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Sets:}
\begin{align*}
K & : \text{Set of mines, } K = \{1, 2, \ldots, \text{n\_mines}\} \\
I & : \text{Set of years, } I = \{1, 2, \ldots, \text{n\_years}\}
\end{align*}

\textbf{Parameters:}
\begin{align*}
\text{n\_maxwork} & : \text{Maximum number of mines that can operate in any year} \\
\text{royalty}_k & : \text{Yearly royalty payable if mine $k$ is kept open} \\
\text{limit}_k & : \text{Upper limit of ore that can be extracted from mine $k$ per year} \\
\text{quality}_k & : \text{Quality of ore from mine $k$} \\
\text{requiredquality}_i & : \text{Required quality of ore in year $i$} \\
\text{price} & : \text{Selling price per ton of blended ore} \\
\text{discount} & : \text{Discount rate per annum}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{isoperated}_{k,i} & \in \{0, 1\} \quad \forall k \in K, i \in I \\
\text{amount}_{k,i} & \geq 0 \quad \forall k \in K, i \in I 
\end{align*}

\textbf{Objective Function:}
\[
\max \sum_{i \in I} \frac{1}{(1+\text{discount})^{i-1}} \left( \text{price} \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} \text{royalty}_k \cdot \text{isoperated}_{k,i} \right)
\]

\textbf{Constraints:}
\begin{align*}
& \sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork} \quad \forall i \in I \\
& 0 \leq \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i} \quad \forall k \in K, i \in I \\
& \sum_{k \in K} \text{amount}_{k,i} \cdot \text{quality}_k = \text{requiredquality}_i \cdot \sum_{k \in K} \text{amount}_{k,i} \quad \forall i \in I \\
& \text{isoperated}_{k,i} \geq \text{isoperated}_{k,i+1} \quad \forall k \in K, i \in I-1 \\
\end{align*}

\textbf{Explanation:}
\begin{itemize}
    \item The objective function seeks to maximize the discounted profit by considering revenue from selling ore and deducting royalties.
    \item Constraint (1) ensures that at most \text{n\_maxwork} mines can operate each year.
    \item Constraint (2) ensures that the amount of ore extracted from each mine does not exceed its limit and is zero if the mine is not operated.
    \item Constraint (3) ensures the quality of the blended ore meets the required quality in each year.
    \item Constraint (4) ensures once a mine is closed in a year, it cannot reopen in subsequent years.
\end{itemize}

\end{document}
```

This model optimizes the mine operations over multiple years while fulfilling constraints related to production limits, quality requirements, and operational restrictions.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Sets:}
\begin{align*}
K & : \text{Set of mines, } K = \{1, 2, \ldots, \text{n\_mines}\} \\
I & : \text{Set of years, } I = \{1, 2, \ldots, \text{n\_years}\}
\end{align*}

\textbf{Parameters:}
\begin{align*}
\text{n\_maxwork} & : \text{Maximum number of mines that can operate in any year} \\
\text{royalty}_k & : \text{Yearly royalty payable if mine $k$ is kept open} \\
\text{limit}_k & : \text{Upper limit of ore that can be extracted from mine $k$ per year} \\
\text{quality}_k & : \text{Quality of ore from mine $k$} \\
\text{requiredquality}_i & : \text{Required quality of ore in year $i$} \\
\text{price} & : \text{Selling price per ton of blended ore} \\
\text{discount} & : \text{Discount rate per annum}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{isoperated}_{k,i} & \in \{0, 1\} \quad \forall k \in K, i \in I \\
\text{amount}_{k,i} & \geq 0 \quad \forall k \in K, i \in I 
\end{align*}

\textbf{Objective Function:}
\[
\max \sum_{i \in I} \frac{1}{(1+\text{discount})^{i-1}} \left( \text{price} \sum_{k \in K} \text{amount}_{k,i} - \sum_{k \in K} \text{royalty}_k \cdot \text{isoperated}_{k,i} \right)
\]

\textbf{Constraints:}
\begin{align*}
& \sum_{k \in K} \text{isoperated}_{k,i} \leq \text{n\_maxwork} \quad \forall i \in I \\
& 0 \leq \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i} \quad \forall k \in K, i \in I \\
& \sum_{k \in K} \text{amount}_{k,i} \cdot \text{quality}_k = \text{requiredquality}_i \cdot \sum_{k \in K} \text{amount}_{k,i} \quad \forall i \in I \\
& \text{isoperated}_{k,i} \geq \text{isoperated}_{k,i+1} \quad \forall k \in K, i \in I-1 \\
\end{align*}

\textbf{Explanation:}
\begin{itemize}
    \item The objective function seeks to maximize the discounted profit by considering revenue from selling ore and deducting royalties.
    \item Constraint (1) ensures that at most \text{n\_maxwork} mines can operate each year.
    \item Constraint (2) ensures that the amount of ore extracted from each mine does not exceed its limit and is zero if the mine is not operated.
    \item Constraint (3) ensures the quality of the blended ore meets the required quality in each year.
    \item Constraint (4) ensures once a mine is closed in a year, it cannot reopen in subsequent years.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

#### Sets
K = range(data['n_mines'])
I = range(len(data['requiredquality']))

#### Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
isoperated = pulp.LpVariable.dicts("IsOperated", ((k, i) for k in K for i in I), cat='Binary')
amount = pulp.LpVariable.dicts("Amount", ((k, i) for k in K for i in I), lowBound=0)

#### Objective Function
problem += pulp.lpSum(
    pulp.lpSum(
        1 / (1 + data['discount'])**i * (
            data['price'] * pulp.lpSum(amount[k, i] for k in K) -
            pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in K)
        )
    ) for i in I
)

#### Constraints

#### Constraint (1): Maximum number of mines that can operate in any year
for i in I:
    problem += pulp.lpSum(isoperated[k, i] for k in K) <= data['n_maxwork'], f"MaxMines_Year_{i}"

#### Constraint (2): Ore extraction limits
for i in I:
    for k in K:
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i], f"Limit_Mine_{k}_Year_{i}"

#### Constraint (3): Quality requirements
for i in I:
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in K) == \
               data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in K), f"Quality_Year_{i}"

#### Constraint (4): Once closed, cannot reopen
for i in range(len(I) - 1):
    for k in K:
        problem += isoperated[k, i] >= isoperated[k, i + 1], f"NoReopen_Mine_{k}_Year_{i}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

