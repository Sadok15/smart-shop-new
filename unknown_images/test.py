M=array([[int]*n for i in range (n)])
    for i in range (n):
        for j in range (n):
            M[i,j]=int(input("M["+str(i)+","+str(j)+"]="))
            while (M[i,j]<1):
                M[i,j]=int(input("M["+str(i)+","+str(j)+"]="))
