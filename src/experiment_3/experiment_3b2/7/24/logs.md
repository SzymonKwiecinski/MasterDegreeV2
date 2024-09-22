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
To solve the given problem, we need to create a mathematical model using Mixed-Integer Linear Programming (MIP). Let's define the decision variables, objective function, and constraints.

######### Decision Variables
- \( \text{isoperated}_{k,i} \): Binary variable indicating whether mine \( k \) is operated in year \( i \) (1 if operated, 0 otherwise).
- \( \text{amount}_{k,i} \): Continuous variable representing the amount of ore produced by mine \( k \) in year \( i \).

######### Objective Function
The objective is to maximize the net present value (NPV) of the profit over the years. The profit for each year is the revenue from selling ore minus the royalty costs. Revenue is calculated as the price per ton times the total amount of ore sold, and royalties are paid for each mine that is kept open.

The present value of profit in year \( i \) is given by:
\[ \text{PV}_i = \frac{\text{price} \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i} - \sum_{k=1}^{n_{\text{mines}}} \text{royalty}_k \cdot \text{isoperated}_{k,i}}{(1 + \text{discount})^i} \]

The objective is:
\[ \max \sum_{i=1}^{I} \text{PV}_i \]

######### Constraints
1. **Quality constraint**: The combined output must meet the required quality each year:
   \[
   \sum_{k=1}^{n_{\text{mines}}} \text{quality}_k \cdot \text{amount}_{k,i} = \text{requiredquality}_i \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i}, \quad \forall i
   \]

2. **Production limit**: Each mine cannot produce more than its limit:
   \[
   \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i}, \quad \forall k, i
   \]

3. **Operation limit**: At most \( n_{\text{maxwork}} \) mines can be operated each year:
   \[
   \sum_{k=1}^{n_{\text{mines}}} \text{isoperated}_{k,i} \leq n_{\text{maxwork}}, \quad \forall i
   \]

4. **Logical constraint**: Mines that are not operated cannot produce:
   \[
   \text{amount}_{k,i} = 0, \quad \text{if } \text{isoperated}_{k,i} = 0, \quad \forall k, i
   \]

Let's write the Linear Programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{align*}
& \text{Maximize } \sum_{i=1}^{I} \frac{\text{price} \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i} - \sum_{k=1}^{n_{\text{mines}}} \text{royalty}_k \cdot \text{isoperated}_{k,i}}{(1 + \text{discount})^i} \\
\text{subject to:} \\
& \sum_{k=1}^{n_{\text{mines}}} \text{quality}_k \cdot \text{amount}_{k,i} = \text{requiredquality}_i \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i}, \quad \forall i, \\
& \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i}, \quad \forall k, i, \\
& \sum_{k=1}^{n_{\text{mines}}} \text{isoperated}_{k,i} \leq n_{\text{maxwork}}, \quad \forall i, \\
& \text{amount}_{k,i} = 0, \quad \text{if } \text{isoperated}_{k,i} = 0, \quad \forall k, i, \\
& \text{isoperated}_{k,i} \in \{0, 1\}, \quad \forall k, i, \\
& \text{amount}_{k,i} \geq 0, \quad \forall k, i.
\end{align*}

\end{document}
```
This model can be implemented using a suitable optimization solver to determine the optimal values of the decision variables, which will indicate which mines to operate each year and the respective production levels.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{align*}
& \text{Maximize } \sum_{i=1}^{I} \frac{\text{price} \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i} - \sum_{k=1}^{n_{\text{mines}}} \text{royalty}_k \cdot \text{isoperated}_{k,i}}{(1 + \text{discount})^i} \\
\text{subject to:} \\
& \sum_{k=1}^{n_{\text{mines}}} \text{quality}_k \cdot \text{amount}_{k,i} = \text{requiredquality}_i \cdot \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i}, \quad \forall i, \\
& \text{amount}_{k,i} \leq \text{limit}_k \cdot \text{isoperated}_{k,i}, \quad \forall k, i, \\
& \sum_{k=1}^{n_{\text{mines}}} \text{isoperated}_{k,i} \leq n_{\text{maxwork}}, \quad \forall i, \\
& \text{amount}_{k,i} = 0, \quad \text{if } \text{isoperated}_{k,i} = 0, \quad \forall k, i, \\
& \text{isoperated}_{k,i} \in \{0, 1\}, \quad \forall k, i, \\
& \text{amount}_{k,i} \geq 0, \quad \forall k, i.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), lowBound=0)
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(len(requiredquality))), cat='Binary')

#### Objective function
problem += pulp.lpSum(
    (price * (pulp.lpSum(amount[k, i] for k in range(n_mines)) - pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines)))) / ((1 + discount) ** i)
    for i in range(len(requiredquality))
), "Total_Profit"

#### Constraints
for i in range(len(requiredquality)):
    problem += pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)), f"Quality_Constraint_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Limit_Constraint_{k}_{i}"

for i in range(len(requiredquality)):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Work_Constraint_{i}"

for k in range(n_mines):
    for i in range(len(requiredquality)):
        problem += amount[k, i] >= 0, f"Non_Negativity_Constraint_{k}_{i}"

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

