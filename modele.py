import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

def is_lm(C0,c,T,I0,G,b,h,k,P,M,label):
   #funkcja IS:Y=C(Y-T)+I+G
   #funkcja LM: Y=(h/k)*r+(L/k)
   r=np.linspace(0,10,100);
   A=b/(1-c);
   B=(I0+G+C0-(c*T))/(1-c)
   Y_IS= (-A)*r +B;
   D=h/k;
   F=M/(k*P);
   Y_LM= D*r +F;
   plt.plot(Y_IS,r,color='pink',label='IS' f"{label}");
   plt.text(Y_IS[0], r[0], 'IS' f"{label}");
   plt.plot(Y_LM,r,color='blue',label='LM' f"{label}");
   plt.text(Y_LM[-1], r[-1], 'LM' f"{label}");
   diff=Y_IS-Y_LM;
   idx = np.where(np.diff(np.sign(diff)))[0][0];
   Y_int = Y_IS[idx];
   r_int = r[idx];
   plt.scatter([Y_int], [r_int], color='green', zorder=5, label='punkt przecięcia' f"{label}");

def as_ad(C0, c, T, I0, G, b, h, k, M, Y_natural, alpha, P_e, label):
    P = np.linspace(0.1, 10, 1000)
    # Definiujemy stałe części równania dla przejrzystości
    # A_bar to autonomiczne wydatki
    A_bar = C0 - c * T + I0 + G
    
    # multiplier_denom to mianownik mnożnika
    multiplier_denom = (1 - c) + (b * k) / h

    # Obliczamy Y_AD dla każdego poziomu cen P
    # Zauważ, że P jest teraz częścią licznika, a mianownik ma znak '+'
    Y_AD = (A_bar + (b / h) * (M / P)) / multiplier_denom

    # Krzywa AS (twoja formuła jest w porządku)
    Y_AS = Y_natural + alpha * np.log(P / P_e)

    plt.plot(Y_AD, P, color='red', label=f'AD {label}')
    plt.plot(Y_AS, P, color='black', label=f'AS {label}')

    diff = Y_AD - Y_AS
    przeciecia = np.where(np.diff(np.sign(diff)))[0]
    for idx in przeciecia:
        Y_int = Y_AD[idx]
        P_int = P[idx]
        plt.scatter([Y_int], [P_int], color='green', zorder=5, 
                    label=f'punkt przecięcia {label}' if idx == przeciecia[0] else "")

def przesunięcia():
    # Wspólne parametry
    C0 = float(input("Konsumpcja autonomiczna-C0: "))
    c = float(input("Skłonność do konsumpcji-c: "))
    T = float(input("Wpływy podatkowe-T: "))
    I0 = float(input("Inwestycje autonomiczne-I0: "))
    G = float(input("Wydatki rządowe-G: "))
    b = float(input("Wrażliwość inwestycji na zmianę stopy procentowej-b: "))
    h = float(input("Współczynnik h: "))
    k = float(input("Współczynnik k: "))
    M = float(input("Nominalna podaż pieniądza-M: "))

    # IS-LM
    P = float(input("Poziom cen dla IS-LM - P: "))

    # AS-AD
    Y_natural = float(input("Poziom PKB w równowadze długookresowej dla AS-AD - Y_natural: "))
    alpha = float(input("Nachylenie krótkookresowej krzywej podaży dla AS-AD - alpha: "))
    P_e = float(input("Oczekiwany poziom cen dla AS-AD - P_e: "))

    param_islm = {'C0': C0, 'c': c, 'T': T, 'I0': I0, 'G': G,'b': b, 'h': h, 'k': k, 'P': P, 'M': M,'label': ''}
    param_asad = {'C0': C0, 'c': c, 'T': T, 'I0': I0, 'G': G,'b': b, 'h': h, 'k': k, 'M': M,'Y_natural': Y_natural, 'alpha': alpha,'P_e': P_e, 'label': ''}

    zmiana = str(input("Czy któryś parametr uległ zmianie?")).strip().lower()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), dpi=100)

    if zmiana == 'nie':
        plt.sca(ax1)
        is_lm(**param_islm)
        ax1.set_xlabel('Y - PKB')
        ax1.set_ylabel('r - stopa procentowa')
        ax1.set_title('IS-LM')
        ax1.set_xlim(left=0)
        ax1.set_ylim(bottom=0)
        ax1.legend()

        plt.sca(ax2)
        as_ad(**param_asad)
        ax2.set_xlabel('Y - PKB')
        ax2.set_ylabel('P - poziom cen')
        ax2.set_title('AS-AD')
        ax2.set_xlim(left=0)
        ax2.set_ylim(bottom=0)
        ax2.legend()

        plt.show()

    elif zmiana == 'tak':
        x = str(input("Podaj parametr, który uległ zmianie:")).strip()

        if x in param_islm:
            y = str(input(f"Jak zmienił się parametr {x} w IS-LM: ")).strip()
            param2_islm = param_islm.copy()
            param2_islm[x] = eval(f"{x}{y}")
            param_islm['label'] = ' 1'
            param2_islm['label'] = ' 2'
        else:
            param2_islm = param_islm.copy()

        if x in param_asad:
            z = str(input(f"Jak zmienił się parametr {x} dla AS-AD: ")).strip()
            param2_asad = param_asad.copy()
            param2_asad[x] = float(z)
            param_asad['label'] = '1'
            param2_asad['label'] = '2'
        else:
            param2_asad = param_asad.copy()

        # Rysowanie IS-LM 
        plt.sca(ax1)
        is_lm(**param_islm)
        if x in param_islm:
            is_lm(**param2_islm)
        ax1.set_xlabel('Y - PKB')
        ax1.set_ylabel('r - stopa procentowa')
        ax1.set_title('IS-LM (przed i po zmianie)')
        ax1.set_xlim(left=0)
        ax1.set_ylim(bottom=0)
        ax1.legend()

        # Rysowanie AS-AD
        plt.sca(ax2)
        as_ad(**param_asad)
        if x in param_asad:
            as_ad(**param2_asad)
        ax2.set_xlabel('Y - PKB')
        ax2.set_ylabel('P - poziom cen')
        ax2.set_title('AS-AD (przed i po zmianie)')
        ax2.set_xlim(left=0)
        ax2.set_ylim(bottom=0)
        ax2.legend()

        plt.show()

    else:
        print("Wpisz 'tak' lub 'nie'.")

przesunięcia()

#Dane są: konsumpcja autonomiczna = 100, krańcowa skłonność do oszczędzania = 0,2, wrażliwość
#popytu na pieniądz na wysokość dochodu = 0,25, wrażliwość popytu na pieniądz na wysokość stopy
#procentowej = 6250; realny zasób pieniądza = 500, stopa opodatkowania dochodów = 0,25, wydatki
#rządowe = 800, inwestycje autonomiczne = 800, wrażliwość inwestycji na wysokość stopy
#procentowej = 5000.
#a) Ile wynoszą dochód i stopa procentowa w równowadze?
#b) O ile zmieni się dochód w wyniku wzrostu realnego zasobu pieniądza o 300?
#c) O ile zmieni się dochód w wyniku wzrostu wydatków rządowych o 300?
#d) O ile zmieniłby się dochód w modelu keynesowskim (bazującym na powyższych danych) w
#przypadku wzrostu wydatków rządowych o 300? Z czego wynika różnica pomiędzy
#odpowiedziami w pkt. c i d?
