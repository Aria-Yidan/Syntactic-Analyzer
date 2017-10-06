# -*- coding:UTF-8 -*-
m = []
m.append("SELECT [ ENAME = 'Mary' & DNAME = 'Research' ] ( EMPLOYEE JOIN DEPARTMENT )")
m.append("PROJECTION [ BDATE ] ( SELECT [ ENAME = 'John' & DNAME = 'Research' ] ( EMPLOYEE JOIN DEPARTMENT ) )")
m.append("SELECT [ ESSN = '01' ] ( PROJECTION [ ESSN, PNAME ] ( WORKS_ON JOIN PROJECT ) )")
keywords = {"SELECT":0, "PROJECTION":1, "JOIN":2}
joinattribute = {"EMPLOYEE || DEPARTMENT":"DNO","WORKS_ON || PROJECT":"PNO"}

def makequerytree(m):
    m = str(m)
    flag = 0
    QueryTree = []
    temp_query = []
    Query = m.split(" ")
    for temp in Query:
        if (temp != ")"):
            temp_query.append(temp)
            if (temp == "JOIN"):
                QueryTree.append(temp)
                flag = 1
        if (flag == 1):
            del temp_query[temp_query.index("JOIN")]
            flag = 0
        
        if (temp == "("):
            QueryTree.append(" ".join(temp_query[:-1]))
            temp_query = []
    QueryTree.append(" || ".join(temp_query))
    return QueryTree

def optimizequerytree(QueryTree):
    QueryTree = list(QueryTree)
    BetterQueryTree = list(QueryTree)
    temp_list = []
    for temp_query in QueryTree:
        temp_list = temp_query.split(" ")
        temp_key = temp_list[0]
        if (temp_key in keywords):
            temp_list = " ".join(temp_list[1:])
            if (temp_key == "PROJECTION"):
                for i in range(len(QueryTree)):
                    temp_k = (QueryTree[i].split(" "))[0]
                    if (temp_k not in keywords):
                        break 
                temp_join = joinattribute[QueryTree[i]]
                
                temp_list = temp_list[1:-1].split(",")
                for i in range(len(temp_list)):
                    temp_list[i] = temp_key + " [" + temp_list[i] + ", "+ temp_join + " ]"
                if (len(temp_list) == 1):
                    temp_list.append(temp_key + " [ " + temp_join + " ]")
                temp_list = " || ".join(temp_list)
                
                for i in range(len(BetterQueryTree)):
                    temp_key = (BetterQueryTree[i].split(" "))[0]
                    if (temp_key not in keywords):
                        BetterQueryTree.insert(i,temp_list)
                        break 
    temp_list = []
    for temp_query in QueryTree:
        temp_list = temp_query.split(" ")
        temp_key = temp_list[0]
        if (temp_key in keywords):
            temp_list = " ".join(temp_list[1:])
            if (temp_key == "SELECT"):
                temp_list = temp_list[1:-1].split("&")
                for i in range(len(temp_list)):
                    temp_list[i] = temp_key + " [" + temp_list[i] + "]"
                temp_list = " || ".join(temp_list)
                
                del BetterQueryTree[BetterQueryTree.index(temp_query)]
                for i in range(len(BetterQueryTree)):
                    temp_key = (BetterQueryTree[i].split(" "))[0]
                    if (temp_key not in keywords):
                        BetterQueryTree.insert(i,temp_list)
                        break
    
    return BetterQueryTree

for i in range(len(m)):
    print "m[",i,"]=",m[i]
cmd = -1
while (cmd != '0'):
    print "Inputs : ",
    cmd = raw_input()
    
    print "\n#----------------------------#"
    QueryTree = makequerytree(m[int(cmd) - 1])
    for temp in QueryTree:
        print temp
    print "\n#----------------------------#"
    BetterQueryTree = optimizequerytree(QueryTree)
    for temp in BetterQueryTree:
        print temp
    print "\n#----------------------------#"
