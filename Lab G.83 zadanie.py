def proc(x,mi,ma):
    p=-1;
    q=len(x);
    i=0;
    while i<q:
        if x[i]<mi:
            p+=1;
            x[i],x[p]=x[p],x[i];
            i+=1;
        elif x[i]>ma:
            q-=1;
            x[i],x[q]=x[q],x[i];
        else:
            i+=1;
    return x;

#funkcja przestawia elementy listy x, tak, aby na początku znajdowały się liczby
#<mi, następnie liczby w przedziale [mi,ma], na końcu liczby >ma
#złożoność pamięciowa: O(1)
#złożoność czasowa optymistyczna = złożoność czasowa pesymistyczna = O(n)
