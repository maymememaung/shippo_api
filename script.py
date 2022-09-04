from fileinput import filename
import shippo
from datetime import datetime

shippo.config.api_key = "shippo_test_4be2330f4cc15d6d278b60de93c2adbc7ded0d1d"

possible_cmds = {
    0: "Create Shipment",
    1: "Retrieve Shipment",
    2: "Retrieve Rates by Shipment ID",
    3: "Retrieve Parcel by Parcel ID",
    4: "Retrieve Parcel by Shipment ID",
    5: "Retrieve Address by Address ID",
    6: "Retrieve Address by Shipment ID",
    -1: "Quit"
}

dist_units = {
    0: "cm",
    1: "in",
    2: "ft",
    3: "mm",
    4: "m",
    5: "yd"
}

mass_units = {
    0: "g",
    1: "oz",
    2: "lb",
    3: "kg"
}


def printCommands():

    print("These are the possible commands with codes.")

    for code, cmd in possible_cmds.items():
        print("%s [%d]" % (cmd, code))


def printDistUnits():

    print("These are the possible distance units for your parcel dimensions.")

    for code, unit in dist_units.items():
        print("%s [%d]" % (unit, code))


def printMassUnits():

    print("These are the possible mass units for your parcel weight.")

    for code, unit in mass_units.items():
        print("%s [%d]" % (unit, code))


def validateCommand(input, dict):

    try:
        code = int(input)
    except:
        return False

    return code in dict


def validateDimensions(dimensions):

    for d in dimensions:
        try:
            d = int(d)
        except:
            return False
        finally:
            if d < 0:
                return False

    return True


def commandInput():

    printCommands()
    code = input("Enter command code.\n")

    while not (validateCommand(code, possible_cmds)):
        printCommands()
        code = input("Enter command code.\n")

    return int(code)


def createAddress(logfile):

    name = input("Enter Name:")
    country = input("Enter the two letter country code, e.g. US:")
    street = input("Enter the street address:")
    city = input("Enter the city:")
    state = input("Enter the state:")
    zip = input("Enter the zip code:")

    address_from = shippo.Address.create(
        name=name,
        street1=street,
        city=city,
        state=state,
        zip=zip,
        country=country,  # iso2 country code
    )

    print("Address Created. Address ID: %s" % (address_from.object_id))
    logfile.write("Address Created. Address ID: %s\n" % (address_from.object_id))

    add = {
        "name": name,
        "street1": street,
        "city": city,
        "state": state,
        "zip": zip,
        "country": country
    }

    return add


def createParcel(logfile):

    printDistUnits()
    dist_unit = input("\nEnter the distance unit code:")

    while not (validateCommand(dist_unit, dist_units)):
        print("Code not valid. Try again.")
        printDistUnits()
        dist_unit = input("Enter the distance unit code:")

    dimensions = input(
        "\nEnter length, width, and height separated by space:").split()
    while (not validateDimensions(dimensions)):
        print("\nDimension not valid. Try again.")
        dimensions = input(
            "\nEnter length, width, and height separated by space:").split()

    printMassUnits()
    mass_unit = input("\nEnter the mass unit code:")

    while (not validateCommand(mass_unit, mass_units)):
        print("Code not valid. Try again.")
        printMassUnits()
        mass_unit = input("\nEnter the mass unit code:")

    weight = input("\nEnter your parcel weight.")
    while (not validateDimensions([weight])):
        print("\nWeight not valid. Try again.")
        weight = input("\nEnter your parcel weight.")

    parcel = shippo.Parcel.create(
        length=dimensions[0],
        width=dimensions[1],
        height=dimensions[2],
        distance_unit=dist_units[int(dist_unit)],
        weight=weight,
        mass_unit=mass_units[int(mass_unit)]
    )

    print("Parcel Created. Parcel ID: %s" % (parcel.object_id))
    logfile.write("Parcel Created. Parcel ID: %s\n" % (parcel.object_id))

    parcel = {
        "length": dimensions[0],
        "width": dimensions[1],
        "height": dimensions[2],
        "distance_unit": dist_units[int(dist_unit)],
        "weight": weight,
        "mass_unit": mass_units[int(mass_unit)]
    }

    return parcel


def confirmShipment(sender_add, rcpt_add, parcel):

    print("\nSender Name and Address: %s" % (" ".join(sender_add.values())))

    print("\nRecipient Name and Address: %s" % (" ".join(rcpt_add.values())))

    print("\nParcel Information: %s" % (" ".join(parcel.values())))
    
    confirm = input("\nDo you want to continue creating this shipment? [y|n]")

    return confirm.lower() == "y"


def createShipment(logfile):
    print("\nYou are about to create a shipment.")

    print("\nEnter the sender address.")

    sender_add = createAddress(logfile)

    print("\nEnter the recipient address.")

    rcpt_add = createAddress(logfile)

    print("\nEnter the parcel information.")

    parcel = createParcel(logfile)

    confirm = confirmShipment(sender_add, rcpt_add, parcel)

    if (confirm):

        shipment = shippo.Shipment.create(
            address_from=sender_add,
            address_to=rcpt_add,
            parcels=[parcel],
            asynchronous=False
        )

        print("Shipment Created. Shipment ID: %s" % (shipment.object_id))
        logfile.write("Shipment Created. Shipment ID: %s\n" % (shipment.object_id))

    else:
        print("Aborting Operation.")


if __name__ == "__main__":

    quit = False

    print("-----------------------------------------")

    filename = datetime.now().strftime("%m-%d-%y,%H.%M.%S") + ".txt"

    with open("logs/" + filename, "w") as logfile:
        
        while not quit:

            cmd_code = commandInput()

            match cmd_code:
                case -1:
                    quit = True
                case 0:
                    createShipment(logfile)

            print("-----------------------------------------")

# address1 = shippo.Address.create(
#     name='John Smith',
#     street1='6512 Greene Rd.',
#     street2='',
#     company='Initech',
#     phone='+1 234 346 7333',
#     city='Woodridge',
#     state='IL',
#     zip='60517',
#     country='US',
#     metadata='Customer ID 123456'
# )

# print ('Success with Address 1 : %r' % (address1, ))

# address_from = {
#     "name": "Shawn Ippotle",
#     "street1": "215 Clayton St.",
#     "city": "San Francisco",
#     "state": "CA",
#     "zip": "94117",
#     "country": "US"
# }

# address_to = {
#     "name": "Mr Hippo",
#     "street1": "Broadway 1",
#     "city": "New York",
#     "state": "NY",
#     "zip": "10007",
#     "country": "US"
# }

# parcel = {
#     "length": "5",
#     "width": "5",
#     "height": "5",
#     "distance_unit": "in",
#     "weight": "2",
#     "mass_unit": "lb"
# }

# shipment = shippo.Shipment.create(
#     address_from = address_from,
#     address_to = address_to,
#     parcels = [parcel],
#     asynchronous = False
# )
