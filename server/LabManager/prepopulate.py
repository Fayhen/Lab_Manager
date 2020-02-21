import requests, random, time
import LabManager.dbModels as models
from LabManager import db, bcrypt
from datetime import timedelta


def random_dates(number):
    dates = []
    for _ in range(number):
        date = random.randint(1, int(time.time()))
        dates.append(int(str(date).split('.')[0]))
    dates.sort()
    return dates


def add_types():
    technician = models.PersonType(type_name = "technician")
    engineer = models.PersonType(type_name = "engineer")
    biologist = models.PersonType(type_name = "biologist")
    chemist = models.PersonType(type_name = "chemist")
    student = models.PersonType(type_name = "student")

    db.session.add(technician)
    db.session.add(engineer)
    db.session.add(biologist)
    db.session.add(chemist)
    db.session.add(student)
    db.session.commit()

    return print("Added person types.\n\n")


def add_genders():
    other = models.Gender(gender_name = "other")
    female = models.Gender(gender_name = "female")
    male = models.Gender(gender_name = "male")

    db.session.add(other)
    db.session.add(female)
    db.session.add(male)
    db.session.commit()

    return print("Added person genders.\n\n")
    

def add_personnel():

    def parse_gender(gender):
        if gender == "female":
            return 2
        elif gender == "male":
            return 3
        else:
            return 1
    
    def give_occupation(type_id):
        technician = [
            "Microscopy imaging technician",
            "Professional cell counter",
            "Field sampler",
            "Field security personnel",
            "Laboratory technician"
        ]
        engineer = [
            "Field engineer",
            "Maintenance"
        ]
        biologist = [
            "Ichtyologist. BSc.",
            "Microbiologist. MSc. Cell culture specialist.",
            "Microbiologist. PhD. Protozoan taxonomy specialist and researcher.",
            "Marine Biologist. PhD. Porifera taxonomy specialist and researcher;",
            "Biologist. MSc. Ecossystem modelling specialist and researcher.",
            "Environmental scientist. MSc. Coastal management specialist."
        ]
        chemist = [
            "Organic chemist. BSc.",
            "Organic chemist. BSc. Water quality assurance specialist.",
            "Organic chemist. MSc. Marine pollutants specialist and researcher.",
            "Mineral chemist. MSc."
        ]
        student = [
            "Grad student.",
            "Visitor student"
        ]

        if type_id == 1:
            return technician[random.randint(0, (len(technician) - 1))]
        elif type_id == 2:
            return engineer[random.randint(0, (len(engineer) - 1))]
        elif type_id == 3:
            return biologist[random.randint(0, (len(biologist) - 1))]
        elif type_id == 4:
            return chemist[random.randint(0, (len(chemist) - 1))]
        else:
            return student[random.randint(0, (len(student) - 1))]
    
    def give_institution():
        institution = [
            "Capital City Univerity",
            "Neighbor City University",
            "Coastal Research Center",
            "National Enviromental Authority",
            "Sister department"
        ]

        return institution[random.randint(0,(len(institution) - 1))]

    request = requests.get("https://uinames.com/api/?ext&amount=50&region=united states")
    names = request.json()

    for name in names:
        gender = parse_gender(name["gender"])
        type_id = random.randint(1, 5)
        occupation = give_occupation(type_id)
        institution = give_institution()

        new_person = models.Person(
            first_name = name["name"],
            last_name = name["surname"],
            middle_name = "",
            phone = name["phone"],
            birthday = name["birthday"]["raw"],
            occupation = occupation,
            institution = institution,
            is_visitor = bool(random.randint(0, 1)),
            type_id = type_id,
            gender_id = gender
        )

        print(f"Instatiated: {new_person.first_name} {new_person.last_name}, {occupation}, {institution}")

        db.session.add(new_person)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding personnel.")


def add_default_user():
    user = models.User(
        username = "DEFAULT",
        email = "default@email.com",
        password = bcrypt.generate_password_hash("default").decode("utf-8"),
        created = str(time.time()),
        last_modified = str(time.time()),
        person_id = 1
    )
    db.session.add(user)
    db.session.commit()

    return print("Default user added to person ID 1")


def add_frequency():
    for _ in range(250):
        date = random.randint(1, int(time.time()))
        time1 = str(time.time()).split('.')[1]
        time2 = random.randint(1, int(time1))

        freq = models.FrequencyEvent(
            date = date,
            entry_time = time2,
            exit_time = time1,
            person_id = random.randint(1, 50)
        )
        print(f"Instantiated: {freq.date}, {freq.entry_time}, {freq.exit_time}, {freq.person_id}")
        
        db.session.add(freq)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding frequencies.")


def add_equipments():
    equips = [
        ["Field Laptop", "HP Pavilion 15.6 HD 2019 Newest Thin and Light Laptop Notebook Computer, Intel AMD A6-9225, 8GB RAM, 1TB HDD, Bluetooth, Webcam, DVD-RW, WiFi, Win 10", True],
        ["Field Laptop", "Fast Dell Latitude E5470 HD Business Laptop Notebook PC (Intel Core i5-6300U, 8GB Ram, 256GB Solid State SSD, HDMI, Camera, WiFi, SC Card Reader), Win 10", True],
        ["Desktop computer", "Acer Aspire TC-885-UA91 Desktop, 9th Gen Intel Core i3-9100, 8GB DDR4, 512GB SSD, 8X DVD, 802.11AC Wifi, USB 3.1 Type C, Windows 10 ", False],
        ["Desktop computer", "HP 8300 Elite Small Form Factor Desktop Computer, Intel Core i5-3470 3.2GHz Quad-Core, 8GB RAM, 500GB SATA, Windows 10 Pro 64-Bit, USB 3.0", False],
        ["Desktop computer", "HP ProDesk 600 G1 SFF Slim Business Desktop Computer, Intel i5-4570 up to 3.60 GHz, 8GB RAM, 500GB HDD, DVD, USB 3.0, Windows 10", False],
        ["Optical microscope", "OMAX 40X-2000X Lab LED Binocular Microscope", True],
        ["Optical microscope", "OMAX 40X-2000X Lab LED Binocular Microscope", False],
        ["Optical microscope", "AmScope M150C-I 40X-1000X All-Metal Optical Glass Lenses Cordless LED Student Biological Compound Microscope", True],
        ["Precision balance", "Ohaus Pioneer PA163 Precision Balance, 160 g Capacity, 0.001 g Readability", False],
        ["Micropipette", "Microlit Lab Micropipette - Single-Channel Adjustable Volume Micro Pipette Fully Autoclavable Pipettor (100-1000ul)", False],
        ["Micropipette", "Microlit Lab Micropipette - Single-Channel Adjustable Volume Micro Pipette Fully Autoclavable Pipettor (100-1000ul)", True],
        ["Refractometer", "Brix Refractometer for Homebrew Beer with ATC, Dual Scale Specific Gravity 1.000-1.130 and Brix 0-32%", True],
        ["Mass spectrometer", "TSQ Altis™ Triple Quadrupole Mass Spectrometer", False],
        ["Centrifuge", "AMTAST 110V 60Hz Mini Centrifuge 10,000 RPM Adjustable", False],
        ["Laboratory oven", "Quincy Lab 10GC Aluminized Steel Bi-Metal Gravity Convection Oven, 0.7 Cubic feet", False],
        ["Furnace", "LMH muffle laboratory furnace", False],
        ["Portable multi-parameter meter", "PC60-Z Bluetooth Multi-Parameter Smart Tester (pH/Conductivity/TDS/Salinity/Resistivity/Temp.)", True],
        ["Handheld GPS", "Garmin eTrex 30x, Handheld GPS Navigator", True]
    ]

    for _ in range(35):
        index = random.randint(0, (len(equips) - 1))
        data = equips[index]

        equip = models.Inventory(
            name = data[0],
            description = data[1],
            field_eligible = data[2],
            buy_date = random.randint(1, int(time.time()))
        )
        print(f"Instantiated: {equip.name}")

        db.session.add(equip)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding equipments.")


def add_lendings():
    def get_names():
        request = requests.get("https://uinames.com/api/?amount=20&region=united states")
        data = request.json()
        names = []
        for name in data:
            first_name = name["name"]
            last_name = name["surname"]
            full_name = first_name + " " + last_name
            names.append(full_name)
        
        return names

    names = get_names()
    for _ in range(30):
        dates = random_dates(3)
        
        lending = models.Lendings(
            lender = names[random.randint(0, (len(names) - 1))],
            lend_date = dates[0],
            return_expected = dates[1],
            return_done = dates[2],
            observations = "Example lending. Dates are randomized and possibly wild.",
            inventory_id = random.randint(1, 35)
        )
        print(f"Instantiated: {lending.lender}, {lending.inventory_id}, {lending.lend_date}, {lending.return_expected}, {lending.return_done}")

        db.session.add(lending)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding equipment lendings.")


def add_issues():
    descriptions = [
        "Shorted fuse", "Stopped working", "Got wet"
    ]

    for _ in range(30):
        dates = random_dates(2)

        issue = models.TechnicalIssues(
            description = descriptions[random.randint(0, (len(descriptions) - 1))],
            report_date = dates[0],
            solution_date = dates[1],
            inventory_id = random.randint(1, 35)
        )
        print(f"Instantiated: {issue.inventory_id},{issue.description}")

        db.session.add(issue)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding technical issues.")


def add_notices():
    notices = [
        [f"{random.randint(1, int(time.time()))}", "Reunion reminder", "Reminding staff of reunion scheduled tommorrow at 9:00."],
        [f"{random.randint(1, int(time.time()))}", "Notice to junior staff", "Please do not eat inside laboratory space."],
        [f"{random.randint(1, int(time.time()))}", "Backup your data", "Reminding staff that maintenance of the faulty computer may require formatting the hard drive. PLEASE backup any data you might have stored on it. The maintenance will be next Thursday."],
        [f"{random.randint(1, int(time.time()))}", "Seminars upcoming", "The University has changed the dates for this semester's student seminars. Junior staff members are encouraged to participate and show your works."],
        [f"{random.randint(1, int(time.time()))}", "Pizza night", "Pizza night is confirmed for next Friday. Bring your hunger."]
    ]

    for _ in range(10):
        notice = notices[random.randint(0, (len(notices) - 1))]
        new = models.Notices(
            date = notice[0],
            title = notice[1],
            content = notice[2],
            archived = random.randint(0, 1),
            user_id = 1
        )
        print(f"Instantiated: {new.title}, {new.date}")

        db.session.add(new)
        db.session.commit()
        print("Instance commited.\n\n")
    
    return print("Finished adding notices.")


def add_trips():
    locations = [
        "Mount Desert Island and Acadia National Park", "Florida Keys",
        "Biscayne Bay National Park", "Glacier Bay National Park and Preserve",
        "Isle Royale National Park", "Virgin Islands National Park",
        "Forillon National Park", "Arrecife Alacranes National Park",
        "Islas Marietas National Park", "Isla Contoy National Park"
    ]

    for _ in range(25):
        personnel = []
        equipments = []
        dates = random_dates(3)

        for i in range(5):
            personnel.append(random.randint(1, 50))
        for j in range(5):
            equipments.append(random.randint(1, 35))

        trip = models.FieldEvent(
            location = locations[random.randint(0, (len(locations) - 1))],
            date_start = dates[0],
            date_end_expected = dates[1],
            date_end_done = dates[2],
            observations = "This is an example field trip with randomized data. Dates, locations and composition of deployed personnel and equipments may appear wild."
        )
        print(f"Instantiated: {trip.location}, {trip.date_start}")
        
        db.session.add(trip)
        db.session.commit()
        print("Instance commited.\n\n")

        print(f"Making personnel helper table insertions with: {personnel}")
        for person_id in personnel:
            insert = models.helper_field_person.insert().values(Person=person_id,
                FieldEvent=trip.id)
            db.session.execute(insert)

        print(f"Making equipment helper table insertions with: {equipments}")  
        for equip_id in equipments:
            insert = models.helper_field_equips.insert().values(Inventory=equip_id,
                FieldEvent=trip.id)
            db.session.execute(insert)

        print("Finished helper insertions.\n\n")


    return print("Finished adding field trips.")
