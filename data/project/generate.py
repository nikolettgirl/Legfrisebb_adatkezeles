from faker import Faker
import random
from model import Haircut,Hairstyle,BarberShop,Person



def generate_hairstyle(n:int,female_ratio=0.5)-> list[Hairstyle]:
    assert n>0
    assert 0 <= female_ratio <= 1
    noi_hajstilusok=["Blunt Bob","Short with Long Bangs,"
                                 "Modern Mullet","Long Pixie","Tapered Layers","Smooth Lob","Long Layers","Sleek and Straight",
                     "LOOSE CURLY AFRO","SPIKY PIXIE","CHOPPY LOB","CURTAIN BANGS","THE UNDERCUT","GELLED EDGES","ANGULAR AFRO","A-LINE LOB",
                     "SUPER-SHORT PIXIE","MOHAWK"]
    ferfi_hajstilusok=[ "blowout", "bowl cut", "buzz cut", "Caesar", "comb-over", "crew cut", "disconnected undercut", "dreadlocks", "fade" ]
    hajvagasok=[]
    female=random.random() <female_ratio
    for i in range(n):
        if female:
            # ha női akkor női stílus
            stilus=random.choice(noi_hajstilusok)
        else:
            stilus=random.choice(ferfi_hajstilusok)
        #az ár egy véletlenszerű érték
        ar=random.choice(range(2500,10000,100))
        hajvagasok.append(Hairstyle("h-" + (str(i).zfill(6)),stilus,ar))
    return hajvagasok

def generate_barbershop(n:int)->list[BarberShop]:
    assert n>0
    # a locale hu hogy magyarok legyenek a cégnevek
    fake=Faker(locale="hu_HU")
    boltok=[]
    for i in range(n):
        # a fake.company egy cégnevet generál a fake.adress pedig egy címet hozzá
        boltok.append(BarberShop("b-" + (str(i).zfill(6)),fake.company(),fake.street_adress(),random.choice(range(1,20))))
    return boltok

def generate_haircut(n:int,hajstilusok:list[Hairstyle],boltok:list[BarberShop],szemelyek:list[Person])->list[Haircut]:
    assert n>0
    assert len(hajstilusok)>0
    assert len(boltok)>0
    assert len(szemelyek)>0
    lista = []
    for i in range(n):
        szemely=random.choice(szemelyek)
        bolt=random.choice(boltok)
        hajstilus=random.choice(hajstilusok)
        lista.append(Haircut(f"T-{str(i).zfill(6)}",bolt.id,hajstilus.id,szemely.id))


    return lista



if __name__ == "__main__":
    x=generate_hairstyle(10,True)
    print(x)