# Name -> Nidhi Mantri
# Student Id -> 2016kucp1014
# Program to make and Operator precedence parser
import sys
import re
from prettytable import PrettyTable

# to validate variables
def valid_variables(V):
    # Validity of Variables
    for i in V:
        c = V.count(i)
        if c > 1:
            output.write("Error -> Two or more same variables -> Invalid Grammar.")
            sys.exit()

# to validate terminals
def valid_terminals(T):
    # Validity of Terminals
    for i in T:
        c = T.count(i)
        if c > 1:
            output.write("Error -> Two or more same terminals -> Invalid Grammar.")
            sys.exit()

# to validate start variable
def valid_start_variable(S):
    # Validity of Start Variable
    s = len(S)
    if s > 1:
        output.write("Error -> Start Variable more than one -> Invalid Grammar.")
        sys.exit()

# to make a dictionary with variables as keys and productions as corresponding values
def Production_dict(P):
    prodt = {}
    for i in xrange(len(P)):
        x = P[i].split(' -> ')
        y = ''.join(x[1].split(' |')).strip('\n')
        y = y.split(' ')
        prodt[x[0]] = y
    return prodt

# if there is indirect recursion for a particular variable it will return True
def indirect_Recursion(V, S, prodt, value):
    # if indirect recursion exists
    var = []
    for i in V:
        if i == S:
            continue
        for j in prodt[i]:
            if j[value] is S and i not in var:  ###### S in j
                var.append(i)
    if var :
        all_v = []
        for i in prodt[S]:
            x = i[0]
            if x in V and x not in all_v:
                all_v.append(x)
        new_prodt = []
        return True
    return False

# it puts the productions of variable v in the productions of variable i to remove consecutive two variables...
# value is -1 for  first place variable, -1 indicating the last position
# value is 0 for second place variable, 0 indicating first position
def putting_productions(main, v, i, prodt, pro_copy, index, value):
    new_ps = []
    prodt[i].remove(main)
    for j in prodt[v]:
        new = main[:index+1+value] + j + main[index+2+value:]
        new_ps.append(new)
    if new_ps :
        prodt[i] += new_ps
        pro_copy[i] += new_ps
    return prodt, pro_copy

# to find the leading set 
def LeadingSet(V, T, prodt, lead):
    temp_lead = {}
    mark = {}
    temp_v = {}
    for i in V:
        temp_lead[i] = map(lambda e : e[0:2], prodt[i])
        lead[i] = []
        mark[i] = False
        temp_v[i] = []
    for i in temp_lead.keys():
        while temp_lead[i]:
            j = temp_lead[i][0]
            if j[0] in T:
                if j[0] not in lead[i] :
                    lead[i].append(j[0])
            elif mark[j[0]] == False :
                if len(j) > 1 and j[1] not in lead[i]:
                    # append the variable in temporary list,
                    #to further add the leading set of variable j in variable i
                    temp_v[i].append(j[0])
                    lead[i].append(j[1])
                    mark[j[0]] = True
                else:
                    temp_v[i].append(j[0])
                    mark[j[0]] = True
            elif mark[j[0]] == True:
                if len(j) > 1 and j[1] not in lead[i]:
                    lead[i].append(j[1])
            del temp_lead[i][0]
    # among temporary variables, appending the leading set of all these variables to main variable
    for i in temp_v.keys():
        if i in temp_v[i]:
            temp_v[i].remove(i)
        while temp_v[i] :
            j = temp_v[i][0]
            if temp_v[j]:
                temp_v[i].extend(temp_v[j])
            lead[i] += lead[j]
            temp_v[i].remove(j)
        lead[i] = list(set(lead[i]))
    return lead

# to find the trailing set
def TrailingSet(V, T, prodt, trail):
    temp_trail = {}
    mark = {}
    temp_v = {}
    for i in V:
        # getting last two characters in reverse order
        temp_trail[i] = map(lambda e : e[::-1][0:2], prodt[i])
        trail[i] = []
        mark[i] = False
        temp_v[i] = []
    for i in temp_trail.keys():
        while temp_trail[i]:
            j = temp_trail[i][0]
            if j[0] in T :
                if j[0] not in trail[i] :
                    trail[i].append(j[0])
            elif mark[j[0]] == False :
                if len(j) > 1 and j[1] not in trail[i]:
                    temp_v[i].append(j[0])
                    #lead[i].extend(lead[j[0]])
                    trail[i].append(j[1])
                    mark[j[0]] = True
                else:
                    temp_v[i].append(j[0])
                    #lead[i].extend(lead[j[0]])
                    mark[j[0]] = True
            elif mark[j[0]] == True:
                if len(j) > 1 and j[1] not in trail[i]:
                    trail[i].append(j[1])
            del temp_trail[i][0]

    for i in temp_v.keys():
        if i in temp_v[i]:
            temp_v[i].remove(i)
        while temp_v[i] :
            j = temp_v[i][0]
            if temp_v[j]:
                temp_v[i].extend(temp_v[j])
            trail[i] += trail[j]
            temp_v[i].remove(j)
        trail[i] = list(set(trail[i]))
    return trail

# for two consecutive variables
two_var = '[A-Z][A-Z]'

# main function to find leading set, trailing set and precedence relation table
def main():
    with open("input.txt","r") as myfile:
        V = myfile.readline().split(':')[1].strip(" \n")
        V = V.split(', ')
        T = myfile.readline().split(':')[1].strip(" \n")
        T = T.split(', ')
        S = myfile.readline().split(':')[1].strip(" \n")
        P = myfile.readlines()[1:]
    output = open("op_grammar.txt", 'w')
    # assign all the productions to the variable in dictionary form
    prodt = Production_dict(P)
    # Validity of Variables
    valid_variables(V)
    for i in prodt.keys():
        if i not in V:
            output.write("Invalid Variables\n")
            sys.exit()
    for i in prodt.keys():
        for j in prodt[i]:
            if j == '#':
                continue
            elif '#' in j:
                output.write("Invalid grammar, epsilon in the production\n")
                sys.exit()
            mp = list(j)
            while mp:
                if mp[0] in T:
                    del mp[0]
                    continue
                elif mp[0] in V:
                    del mp[0]
                    continue
                else:
                    output.write('Invalid Grammar\n')
                    sys.exit()
 
    # Validity of Terminals
    valid_terminals(T)
    # Validity of Start Variable
    valid_start_variable(S)
    
    pro_copy = Production_dict(P)
    # epsilon detection
    epsilon = []
    for i in V :
        if '#' in prodt[i] :
            prodt[i].remove('#')
            pro_copy[i].remove('#')
            epsilon.append(i)
    #print epsilon
    # To remove epsilon
    while epsilon:
        for i in V:
            if prodt[i] == []:
                prodt[i].append('#')
                pro_copy[i].append('#')
            for j in prodt[i]:
                if epsilon[0] in j:
                    index = j.find(epsilon[0])
                    #j = j.replace(epsilon[0], '')
                    j = j[:index] + j[index+1:]
                    if len(j) == 0:
                        j = '#'
                    prodt[i].append(j)
                    pro_copy[i].append(j)
        del epsilon[0]

    # if epsilon still exists then exit           
    for i in V :
        if '#' in prodt[i] :
            output.write("Error -> Can't proceed further, epsilon always remains there in productions.\n")
            output.write("This is not an OP Grammar\n")
            sys.exit()
    
    # consecutive two variables
    for i in V:
        while pro_copy[i]:
            main = pro_copy[i][0]
            #co_main = pro_copy[i][0]
            if re.findall(two_var, main):
                var_s = re.findall(two_var, main)
                index = main.index(var_s[0])
                x = var_s[0][0]
                y = var_s[0][1]
                yes_y, yes_yv, yes_x, yes_xv = True, True, True, True
                for j in prodt[y]:
                    if j[0] not in T:# and j[-1] == y:
                        yes_y = False
                    if j[0] == y:
                        yes_yv = False
                for j in prodt[x]:
                    if j[-1] not in T:# and j[-1] == y:
                        yes_x = False
                    if j[-1] == x:
                        yes_xv = False
                # for second variable
                if yes_y == True:
                    value = 0
                    prodt, pro_copy = putting_productions(main, y, i, prodt, pro_copy, index, value)
                # for first variable
                elif yes_x == True:
                    value = -1
                    prodt, pro_copy = putting_productions(main, x, i, prodt, pro_copy, index, value)
                # if variable in first ...
                elif yes_xv == True:
                    indirect_rec = indirect_Recursion(V, x, prodt, -1)
                    if not indirect_rec:
                        value = -1
                        prodt, pro_copy = putting_productions(main, x, i, prodt, pro_copy, index, value)
                # if variable in second ...
                elif yes_yv == True:
                    indirect_rec = indirect_Recursion(V, x, prodt, 0)
                    if not indirect_rec:
                        value = 0
                        prodt, pro_copy = putting_productions(main, y, i, prodt, pro_copy, index, value)
            del pro_copy[i][0]
        for j in prodt[i]:
            if re.findall(two_var, j):
                output.write("Error -> Still two consecutive variables are present..\n")
                output.write("This is not an OP Grammar.\n")
                sys.exit()
    output.write('%s\n' % prodt)

    leading_Set = {}
    leading_Set = LeadingSet(V, T, prodt, leading_Set)
    #print "LeadingSet -> ", leading_Set
    trailing_Set = {}
    trailing_Set = TrailingSet(V, T, prodt, trailing_Set)
    #print "TrailingSet -> ",trailing_Set
    lead_Table = PrettyTable()
    trail_Table = PrettyTable()
    lead_Table.field_names = ['V', "LeadingSet"]
    trail_Table.field_names = ['V', "TrailingSet"]
    # print the tables for leading and trailing set
    for i in V:
        lead_Table.add_row([i, leading_Set[i]])
        trail_Table.add_row([i, trailing_Set[i]])
    output.write("Leading Set of Variables : -\n%s\n" % lead_Table)
    output.write("Trailing Set of Variables : -\n%s\n" % trail_Table)
        
    # precedence relation table
    prec_table = {}
    keys = T+['$']
    for k in keys:
        prec_table[k] = {}
    for k in keys:
        for j in keys:
            prec_table[k][j] = []
    #'$' vs Leading(S) 
    for i in leading_Set[S]:
        prec_table['$'][i] = ['<.']
    # trailing(S) vs '$'
    for i in trailing_Set[S]:
        prec_table[i]['$'] = ['.>']
    for i in V:
        for j in prodt[i]:
            if len(j) == 1:
                continue
            for l in range(len(j)-1):
                if j[l] in T and j[l+1] in T:
                    prec_table[j[l]][j[l+1]].append('=')
                elif j[l] in T and j[l+1] in V:
                    for n in leading_Set[j[l+1]]:
                        prec_table[j[l]][n].append('<.')
                elif j[l] in V and j[l+1] in T:
                    for n in trailing_Set[j[l]]:
                        prec_table[n][j[l+1]].append('.>')
                if l <= len(j)-3:
                    if j[l] in T and j[l+2] in T and j[l+1] in V:
                        prec_table[j[l]][j[l+2]].append('=')
    entries = 0
    for i in keys:
        for k in keys:
            if len(prec_table[i][k]) > 1:
                entries = 1
                #sys.exit()
    # making a list of all the values for a particular variable in the order of  list 'key'
    list_table = {}
    for k in keys:
        list_table[k] = []
        for j in keys:
            list_table[k].append(prec_table[k][j])
    # pretty table output for precedence relation table..
    Table = PrettyTable()
    Table.field_names = ['T']+T+['$']
    for i in keys:
        list_table[i] = [i]+list_table[i]
        Table.add_row(list_table[i])
    #print Table
    output.write("Precedence Relation Table is : -\n")
    output.write("%s\n" % Table)
    if entries == 1:
        output.write("There are multiple entries in the table.\n")
        output.write("We can't construct an operator precedence parser for this grammar.\n")
    
if __name__ == '__main__':
    main()
