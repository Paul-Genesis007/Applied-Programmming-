import numpy as np
import os
def evalSpice(filename):
    # Check if the file address exists
    if not os.path.exists(filename):
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    # Read the file
    with open(filename, "r") as f1:
        f2 = f1.read()
    # Split the file into lines
    ckt = f2.splitlines()
    # Check for '.circuit' and '.end' markers
    if '.circuit' not in ckt:
        raise ValueError('Malformed circuit file')
    # Find indices for circuit section
    a = ckt.index('.circuit')
    b = ckt.index('.end')
    # Extract circuit section
    ckt1 = ckt[a + 1:b]
    length = len(ckt1)
    v_comps = []
    R = []
    V = []
    I = []
    nodes = set()
    node_voltages = {'GND': 0}
    k = 1
    for line in ckt1:
        l = line.split() 
        # Assign node voltages
        for i in l[1:3]:
            if i not in node_voltages:
                node_voltages[i] = k
                k += 1 
        if l[0][0] == 'R':          #For resistors values collection
            R.append([node_voltages[l[1]], node_voltages[l[2]], float(l[3])])
            nodes.update({node_voltages[l[1]], node_voltages[l[2]]})
        elif l[0][0] == 'V':        #For voltage source values collection
            if l[3] == 'dc':
                V.append([node_voltages[l[1]], node_voltages[l[2]], float(l[4])])
                nodes.update({node_voltages[l[1]], node_voltages[l[2]]})
                v_comps.append(l[0])
        elif l[0][0] == 'I':        #For current source values collection
            if l[3] == 'dc':
                I.append([node_voltages[l[1]], node_voltages[l[2]], l[4]])
                nodes.update({node_voltages[l[1]], node_voltages[l[2]]})
        elif l[0][0] not in 'VIR':
            raise ValueError('Only V, I, R elements are permitted')
    nodes = list(nodes)
    nodes_len = len(nodes)
    I_len = len(I)
    V_len = len(V)

    # Convert to numpy arrays
    R_arr = np.array(R, dtype=float)
    V_arr = np.array(V, dtype=float)
    I_arr = np.array(I, dtype=float)

    # Initialize matrices
    A = np.zeros((nodes_len + V_len  - 1, nodes_len + V_len - 1), dtype=float)
    B = np.zeros(nodes_len + V_len  - 1, dtype=float)
    for i in range(1, nodes_len):
        for r in R_arr:
            if (r[0] == i):
                A[i - 1][i - 1] += 1 / r[2]         # adding diagonal element with 1/R
                if (r[1] != 0):
                    A[i - 1][int(r[1]) - 1] -= 1 / r[2]     # adding off-diagonal element with -1/R
            if (r[1] == i):
                A[i - 1][i - 1] += 1 / r[2]      # adding diagonal element with 1/R
                if (r[0] != 0):
                    A[i - 1][int(r[0]) - 1] -= 1 / r[2]     # adding off-diagonal element with -1/R
    N = nodes_len- V_len 
    for v in V_arr:
        if v[0] != 0:
            A[N][int(v[0]) - 1] += 1        # Update element corresponding to positive node of voltage source
        if v[1] != 0:
            A[N][int(v[1]) - 1] -= 1        # Update element corresponding to negative node of voltage source
        B[N] = v[2]         # Set B matrix value for voltage source
        if int(v[0]) != 0:
            A[int(v[0]) - 1][-1] += 1       # Update element corresponding to positive node of voltage source (last row)
        if v[1] != 0:
            A[int(v[1]) - 1][-1] -= 1       # Update element corresponding to negative node of voltage source (last row)
        N = N + 1


    M = nodes_len - I_len
    for i in I_arr:
        if(int(i[0]) != 0):
            B[int(i[0]) - 1] -= 1       # Set B matrix value for current source (positive node)
        if(i[1] != 0):
            B[int(i[1]) - 1] += 1       # Set B matrix value for current source (negative node)
        M = M + 1

    try:
        x = np.linalg.solve(A, B)
    except:
        raise ValueError('Circuit error: no solution')
    
    #making the dictionaries to give the output as asked.
    for q in node_voltages:
        if(q != 'GND'):
            node_voltages[q] = x[node_voltages[q] - 1]
    i = 0
    I_dict = {}
    for comp in v_comps:
        I_dict.update({comp: x[len(node_voltages) - 1 + i]})            #this idea was discussed between my friend
        i += 1
    return node_voltages, I_dict


