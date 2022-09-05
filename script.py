from shippo.error import InvalidRequestError, AddressError
from fileinput import filename
import shippo
from datetime import datetime
from prettytable import PrettyTable, ALL


shippo.config.api_key = "shippo_test_4be2330f4cc15d6d278b60de93c2adbc7ded0d1d"

possible_cmds = {
    0: "Create Shipment",
    1: "Retrieve Shipment",
    2: "Retrieve Rates by Shipment ID",
    3: "Retrieve Parcel by Parcel ID",
    4: "Retrieve Parcel by Shipment ID",
    5: "Retrieve Address by Address ID",
    6: "Retrieve Address by Shipment ID",
    7: "Retrieve All Shipments",
    8: "Get Last Shipment ID",
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

add_fields = ["name", "street1", "city", "state", "zip", "country"]

parcel_fields = ["width", "length", "height",
                 "weight", "distance_unit", "mass_unit"]

shipment_fields = ["object_id", "status", "shipment_date", "address_from", "address_to", "parcels"]

rate_fields = ["provider", "servicelevel", "duration_terms", "estimated_days", "amount", "currency"]


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
            if d < 0:
                return False
        except:
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

    success = False

    while (not success):

        name = input("Enter Name:")
        country = input("Enter the two letter country code, e.g. US:")
        street = input("Enter the street address:")
        city = input("Enter the city:")
        state = input("Enter the state:")
        zip = input("Enter the zip code:")

        try:
            address_from = shippo.Address.create(
                name=name,
                street1=street,
                city=city,
                state=state,
                zip=zip,
                country=country,  # iso2 country code
                validate=True
            )
            if not address_from.validation_results.is_valid:
                raise AddressError(
                    address_from.validation_results.messages[0].text, None, address_from.validation_results.messages[0].code)
            print("Address Created. Address ID: %s" % (address_from.object_id))
            success = True

        except InvalidRequestError as e:
            print(list(e.http_body.values())[0][0], "Please try again.")
            # print(e.args[0])

        except AddressError as e:
            print(e.args[0], "Please try again.")

    logfile.write("Address Created. Address ID: %s\n" %
                  (address_from.object_id))

    # add = {
    #     "name": address_from.name,
    #     "street1": address_from.street1,
    #     "city": address_from.city,
    #     "state": address_from.state,
    #     "zip": address_from.zip,
    #     "country": address_from.country
    # }

    add = {field: address_from[field] for field in add_fields}

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
        logfile.write("Shipment Created. Shipment ID: %s\n" %
                      (shipment.object_id))

    else:
        print("Aborting Operation.")


def retrieveShipment():
    shipment_id = input("Enter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
        displayShipments([shipment])
    except:
        print("No shipment found.")


def retrieveParcelByParcelId():
    parcel_id = input("Enter Parcel ID:")

    try:
        parcel = shippo.Parcel.retrieve(parcel_id)
        displayData(parcel_fields, [parcel])
        # parcelToString(parcel)
    except:
        print("No parcel found.")


def retrieveRatesByShipmentId():
    shipment_id = input("Enter Shipment ID:")

    try:
        rates = shippo.Shipment.get_rates(shipment_id, asynchronous=False)
        for rate in rates.results:
            rate.servicelevel = rate.servicelevel.name
        displayData(rate_fields, rates.results)
    except:
        print("No rates found.")


def retrieveParcelByShipmentId():
    shipment_id = input("Enter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
        displayData(parcel_fields, [shipment.parcels[0]])
    except:
        print("No parcel found.")


def retrieveAddressByAddressId():
    address_id = input("Enter Address ID:")
    try:
        add = shippo.Address.retrieve(address_id)
        # displayData(add_fields, [add])
        addressToString(add)
    except:
        print("Address not found.")


def retrieveAddressbyShipmentId():
    shipment_id = input("Enter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
        add = shippo.Address.retrieve(shipment.address_from.object_id)
        displayData(add_fields, [add])
    except:
        print("No parcel found.")


def retrieveAllShipments():
    shipments = shippo.Shipment.all()
    # print(shipments)
    displayShipments(shipments.results)


def getLastShipmentId():
    shipments = shippo.Shipment.all()
    print(shipments.results[0].object_id)


def printTable(headers, data):
    x = PrettyTable()
    x.field_names = headers
    for record in data:
        row = []
        for header in headers:
            row.append(record[header])
        x.add_row(row)

    x._max_width = {header: 20 for header in headers}
    x.hrules = ALL

    print(x)


def displayData(headers, data):
    print_method = input(
        "Do you want a table format or a raw format? [t|r]")
    if (print_method.lower() == 't'):
        printTable(headers, data)
    else:
        print(data)


def parcelToString(parcel):
    return ("length=%s,width=%s,height=%s %s,weight=%s %s" % (parcel.length, parcel.width, parcel.height, parcel.distance_unit, parcel.weight, parcel.mass_unit))


def addressToString(address):
    return ("%s, %s, %s %s, %s %s" % (address.name, address.street1, address.city, address.state, address.zip, address.country))


def displayShipments(shipments):
    records = []
    for shipment in shipments:
        row = []
        for header in shipment_fields:
            if header == "address_from" or header == "address_to":
                row.append(addressToString(shipment[header]))
            
            elif header == "parcels":
                row.append(parcelToString(shipment[header][0]))
            
            else:
                row.append(shipment[header])
        records.append(row)
    x = PrettyTable()
    x.field_names = shipment_fields
    for row in records:
        x.add_row(row)
    x._max_width = {"address_from": 20, "address_to": 20, "parcels": 20, "object_id": 20}
    x.hrules = ALL
    print(x)


if __name__ == "__main__":

    quit = False

    print("-----------------------------------------")

    filename = datetime.now().strftime("%m-%d-%y,%H.%M.%S") + ".txt"

    with open("logs/" + filename, "w") as logfile:

        while not quit:
            # printTable()

            cmd_code = commandInput()

            match cmd_code:
                case -1:
                    quit = True
                case 0:
                    createShipment(logfile)
                case 1:
                    retrieveShipment()
                case 2:
                    retrieveRatesByShipmentId()
                case 3:
                    retrieveParcelByParcelId()
                case 4:
                    retrieveParcelByShipmentId()
                case 5:
                    retrieveAddressByAddressId()
                case 6:
                    retrieveAddressbyShipmentId()
                case 7:
                    retrieveAllShipments()
                case 8:
                    getLastShipmentId()

            print("-----------------------------------------")
