from __future__ import annotations

from dataclasses import field, dataclass
import random
from typing import Type, cast

from faker import Faker
from data.project.base import Dataset, Entity





@dataclass
class Haircut(Entity):
    # Hajvágások. Az ID az egyedi azonositó,a barbershop az üzletet tárolja ahol az történt,a hair a hajstílust,a person pedig egy embert.
    id:str =field(hash=True)
    barbershop:str =field(repr=True)
    hair:str= field(repr=True)
    person:str =field(repr=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> Haircut:
        return Haircut(seq[0], seq[1], seq[2], seq[3])

    def to_sequence(self) -> list[str]:
        return [self.id,self.barbershop,self.hair,self.person]

    @staticmethod
    def field_names() -> list[str]:
        return ["id","barbershop","hair","person"]

    @staticmethod
    def collection_name() -> str:
        return "haircut"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Haircut.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            barbershop varCHAR(8) NOT NULL,
            hair VARCHAR(8) NOT NULL,
            person VARCHAR(8) NOT NULL,
            

            FOREIGN KEY (barbershop) REFERENCES {BarberShop.collection_name()}(code),
            FOREIGN KEY (hair) REFERENCES {Hairstyle.collection_name()}(id),
            FOREIGN KEY (person) REFERENCES {Person.collection_name()}(plate)
        );
         """


@dataclass
class BarberShop(Entity):
    # ez a hely ahol vágja a hajat. Egy egyedi azonositója van,egy neve,egy címe meg egy kapacitása(hány ember lehet bent egyszerre)
    id:str = field(hash=True)
    name:str =field(repr=True)
    address:str =field(repr=True)
    capacity: int =field(repr=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> BarberShop:
        return BarberShop(seq[0], seq[1], seq[2], int(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id,self.name,self.address,str(self.capacity)]

    @staticmethod
    def field_names() -> list[str]:
        return ["id","name","address","capacity"]

    @staticmethod
    def collection_name() -> str:
        return "barbershops"

    @staticmethod
    def create_table() -> str:
        return f"""
          CREATE TABLE {BarberShop.collection_name()} (
              id VARCHAR(8) NOT NULL PRIMARY KEY,
              name VARCHAR(50),
              address VARCHAR(50),
              capacity TINYINT
          );
          """
@dataclass
class Hairstyle(Entity):
    # Hajstílus. Van egy egyedi azonositója,egy neve,és egy ára.
    id: str= field(hash=True)
    name: str =field(repr=True)
    cost: int =field(repr=True)

    @staticmethod
    def from_sequence(seq: list[str]) -> Hairstyle:
        return Hairstyle(seq[0], seq[1], int(seq[2]))

    def to_sequence(self) -> list[str]:
        return [self.id,self.name,str(self.cost)]

    @staticmethod
    def field_names() -> list[str]:
        return ["id","name","cost"]

    @staticmethod
    def collection_name() -> str:
        return "hairstyles"

    @staticmethod
    def create_table() -> str:
        return f"""
          CREATE TABLE {Hairstyle.collection_name()} (
              id VARCHAR(8) NOT NULL PRIMARY KEY,
              name VARCHAR(50),
              cost TIMYINT
          );
          """


@dataclass
class Person(Entity):
    # órán csinált személy osztály
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), bool(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            name VARCHAR(50),
            age TINYINT,
            male BOOLEAN
        );
        """


@dataclass #kicsit felcserélve
class CutDataset(Dataset):
    szemelyek: list[Person]
    hajstilusok : list[Hairstyle]
    utletek: list[BarberShop]
    hajvagasok : list[Haircut]

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res=dict()
        res[Person]=self.szemelyek
        res[Hairstyle]=self.hajstilusok
        res[BarberShop]=self.utletek
        res[Haircut]=self.hajvagasok
        return res

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person,Hairstyle,BarberShop,Haircut]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return CutDataset(
            cast(list[Person], entities[0]),
            cast(list[Hairstyle], entities[1]),
            cast(list[BarberShop], entities[2]),
            cast(list[Haircut], entities[3])
        )

    @staticmethod
    def generate(count_of_hairstyles:int,count_of_barbershops:int,count_of_persons:int,count_of_haircuts:int):
        # Ezek a generálófüggvények
        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "hu_HU",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people
        def generate_hairstyle(n: int, female_ratio=0.5) -> list[Hairstyle]:
            assert n > 0
            assert 0 <= female_ratio <= 1
            noi_hajstilusok = ["Blunt Bob", "Short with Long Bangs,"
                                            "Modern Mullet", "Long Pixie", "Tapered Layers", "Smooth Lob",
                               "Long Layers", "Sleek and Straight",
                               "LOOSE CURLY AFRO", "SPIKY PIXIE", "CHOPPY LOB", "CURTAIN BANGS", "THE UNDERCUT",
                               "GELLED EDGES", "ANGULAR AFRO", "A-LINE LOB",
                               "SUPER-SHORT PIXIE", "MOHAWK"]
            ferfi_hajstilusok = ["blowout", "bowl cut", "buzz cut", "Caesar", "comb-over", "crew cut",
                                 "disconnected undercut", "dreadlocks", "fade"]
            hajvagasok = []
            female = random.random() < female_ratio
            for i in range(n):
                if female:
                    # ha női akkor női stílus
                    stilus = random.choice(noi_hajstilusok)
                else:
                    stilus = random.choice(ferfi_hajstilusok)
                # az ár egy véletlenszerű érték
                ar = random.choice(range(2500, 10000, 100))
                hajvagasok.append(Hairstyle("h-" + (str(i).zfill(6)), stilus, ar))
            return hajvagasok

        def generate_barbershop(n: int) -> list[BarberShop]:
            assert n > 0
            # a locale hu hogy magyarok legyenek a cégnevek
            fake = Faker(locale="hu_HU")
            boltok = []
            for i in range(n):
                # a fake.company egy cégnevet generál a fake.address pedig egy címet hozzá
                boltok.append(BarberShop("b-" + (str(i).zfill(6)), fake.company(), fake.street_address() ,
                                         random.choice(range(1, 20))))
            return boltok

        def generate_haircut(n: int, hajstilusok: list[Hairstyle], boltok: list[BarberShop], szemelyek: list[Person]) -> \
        list[Haircut]:
            assert n > 0
            assert len(hajstilusok) > 0
            assert len(boltok) > 0
            assert len(szemelyek) > 0
            lista = []
            for i in range(n):
                szemely = random.choice(szemelyek)
                bolt = random.choice(boltok)
                hajstilus = random.choice(hajstilusok)
                lista.append(Haircut(f"T-{str(i).zfill(6)}", bolt.id, hajstilus.id, szemely.id))

            return lista
        emberek=generate_people(count_of_persons,min_age=14,max_age=80)
        hajstilusok=generate_hairstyle(count_of_hairstyles)
        uzletek=generate_barbershop(count_of_barbershops)
        hajvagasok=generate_haircut(count_of_haircuts,hajstilusok,uzletek,emberek)
        return CutDataset(emberek,hajstilusok,uzletek,hajvagasok)
