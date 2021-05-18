from microbit import *
import machine
import radio

# Postavljanje radio kkomunikacijskog kanala
# I ukljucivanje
radio.config(channel=80)
radio.on()

# Iščitavanje serijskog ID-ija microbita
ID = str(machine.unique_id())
ID = ID[4:26]
ID = ID.replace('\\', '').replace('x', '')

# Kreiranje slike kada odgovor nije odabran
fi_img = Image('00900:99999:90909:99999:00900')

# Inicijaliziranje varijable za odabir odgovora
odgovor = ['O', 'A', 'B', 'C', 'D']
index_odgovora = 0
stari_odgovor = 5

mojeIme = 'None'
primljena_poruka = 'None'

while True:
    # Prikaz trenutno odabranog odgovora
    if (stari_odgovor != index_odgovora):
        # Ako je odabran veci odgovor od 4 ponudjena
        if (index_odgovora >= 5 or index_odgovora == 0):
            index_odgovora = 0
            display.show(fi_img)
        else:
            display.show(str(odgovor[index_odgovora]))
        print(odgovor[index_odgovora])  # <- Print ne brisat, iz nekog razloga
        stari_odgovor = index_odgovora  # bez njega ne radi...

    # Posalji zahtjev za vlastito ime
    if (button_a.is_pressed() and button_b.is_pressed()):
        display.scroll('*')
        poruka = ID + 'I'
        radio.send(poruka)
        display.clear()
        button_b.was_pressed()
    
    # Promijeni odgovor, kruzno
    elif (button_a.was_pressed()):
        index_odgovora += 1
    
    # Potvrdi unos odgovora
    elif (button_b.was_pressed()):
        poruka = ID + odgovor[index_odgovora]
        index_odgovora = 0
        radio.send(poruka)
        display.show(Image.YES)
        sleep(1000)

    # Učitavanje radio poruke i spremanje u varijablu
    primljena_poruka = str(radio.receive())
    
    # Prikazivanje primljene poruke
    # Moze biti Ime, ili provjera odgovora
    if (ID in primljena_poruka):
        mojeIme = primljena_poruka.replace(ID, '')
        print(mojeIme)
        primljena_poruka = 'None'
        display.scroll(mojeIme)