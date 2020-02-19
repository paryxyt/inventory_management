from mip import *


def inventory_mgmt(c, w, I, d, stcost, trcost, cap):
    
    """
    c = number of customers
    w = number of warehouses
    I = this is the number of items for which there is demand
    d = customer demand
    stcost = warehouse storage cost
    trcost = transportation cost between warehouse and customer
    cap = warehouse storage capacities
    """
    # declare optimization instance and decision variable
    m = Model()
    Z = [[[m.add_var(var_type=INTEGER, lb = 0) for j in range(c)] for i in range(I)] for k in range(w)]

    # constraints for warehouse capacity
    for k in range(w):
        m += xsum(stcost[i][k]*Z[k][i][j] for i in range(I) for j in range(c)) <= cap[k]

    # constraints to meet customer demands
    for i in range(I):
        for j in range(c):
            m += xsum(Z[k][i][j] for k in range(w)) >= d[i][j]

    # declare objective
    m.objective = minimize(xsum(trcost[k][i][j]*Z[k][i][j] for i in range(I) for j in range(c) for k in range(w)))

    status = m.optimize(max_seconds=300)
    return Z
 
