from microbit import *
import radio

# Postavljanje radio komunikacijskog kanala
# I ukljucivanje radija
radio.config(channel=80)
radio.on()

# Inicijalizacija lista u koje ce se spremati id-ijevi
# primljeni odgovori, i zbrajati bodovi
serijski_brojeviL = ['None']
odgovoriL = ['None']
bodoviL = [0]

tocan_odgovor = 'None'

stanje = 1
staro_stanje = 0

# Funkcija koju pozivamo prilikom provjere pojedinog odogovora
def provjera_odgovora(tocan_odgovor):
    for ID in serijski_brojeviL:
        if ID != 'None':
            Index = serijski_brojeviL.index(ID)

            if (odgovoriL[Index] == tocan_odgovor):
                radio.send(str(ID + 'T'))
                bodoviL[Index] = bodoviL[Index] + 1

            else:
                radio.send(str(ID + 'N'))

# --> Pocetak programa <------------------------------
while True:
    
    # Spremanje primljene poruke u varijablu
    poruka = str(radio.receive())
    
    # Rasclanjivanje ID-ja i podatka koji je primljen u poruci
    if (poruka != 'None'):
        ID = str(poruka[:-1])
        podatak = str(poruka[-1])
        # Za nove ID-jeve dodavanje mjesta u listama
        if ID not in serijski_brojeviL:
            serijski_brojeviL.append(ID)
            bodoviL.append(0)
            odgovoriL.append('')
    else:
        ID = 'None'
        podatak = 'None'
        
    # Promijena rada microbita
    # Primanje_odgovora/Unos_tocnog_odgovora/Ispis_tablice_s_bodovima
    if (button_a.was_pressed()):
        stanje += 1
        if (stanje > 3):
            stanje = 1
            
    if (staro_stanje != stanje):
        display.show(str(stanje))
        staro_stanje = stanje
            
    # Ako je poslan zahtjev za primanje vlastitog imena
    if (podatak == 'I'):
        Ime = str(serijski_brojeviL.index(ID))
        radio.send(ID + Ime)

    # -------primanje odgovora--------------- 
    if (stanje == 1):  
        primljeni_odgovor = podatak
        if primljeni_odgovor != 'I' and primljeni_odgovor != 'None':
            odgovoriL[serijski_brojeviL.index(ID)] = primljeni_odgovor
            
    # --------unos tocnog odgovora i provjera odgovora ---------
    elif stanje == 2:     
        if (tocan_odgovor != 'None'):
            display.show(tocan_odgovor)
            
            # potvrda unosa odgovora, provjera, te zbrajanje bodova
            if button_b.is_pressed(): 
                display.show(Image.ALL_CLOCKS, delay=100)
                display.clear()
                # ---koristimo funkciju da bismo provjerili odgovor
                # ---i pribrojili bod ako je odgovor tocan
                provjera_odgovora(tocan_odgovor)   # <---
                tocan_odgovor = 'None'
                stanje = 1
        
        # Odabir tocnog odgovora preko jednog od tipkala
        if (pin0.read_digital()):
            tocan_odgovor = 'A'
            button_b.was_pressed()
        elif (pin1.read_digital()):
            tocan_odgovor = 'B'
            button_b.was_pressed()
        elif (pin2.read_digital()):
            tocan_odgovor = 'C'
            button_b.was_pressed()
        elif (pin8.read_digital()):
            tocan_odgovor = 'D'
            button_b.was_pressed()
    
    # ----- Ispisivanje tablice tocnih odgovora -----
    elif stanje == 3:
        if(button_b.is_pressed()):
            print("\nIme\tBroj bodova\n")
            for ind in range(1, len(odgovoriL)):
                broj_bodova = bodoviL[ind]
                print(str(ind) + "  \t" + str(broj_bodova))
                radio.send(str(serijski_brojeviL[ind]) + str(broj_bodova))
                
            stanje = 1