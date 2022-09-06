import sys
from shippo.error import InvalidRequestError, AddressError
import shippo
from datetime import datetime
from utilities import *

shippo.config.api_key = "shippo_test_4be2330f4cc15d6d278b60de93c2adbc7ded0d1d"

possible_cmds = {
    0: "Create Shipment",
    1: "Retrieve Shipment",
    2: "Retrieve Rates by Shipment ID",
    3: "Retrieve Parcel by Parcel ID",
    4: "Retrieve Parcel by Shipment ID",
    5: "Retrieve Address by Address ID",
    6: "Retrieve Addresses by Shipment ID",
    7: "Retrieve All Shipments",
    8: "Get Last Shipment ID",
    9: "Retrieve Last Shipment",
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

shipment_fields = ["object_id", "status", "shipment_date",
                   "address_from", "address_to", "parcels"]

rate_fields = ["provider", "servicelevel", "duration_terms",
               "estimated_days", "amount", "currency"]


def commandInput():

    printOptions("These are the possible commands with codes.", possible_cmds)
    code = input("Enter command code.\n")

    while (not validateCommand(code, possible_cmds)):
        printOptions("These are the possible commands with codes.", possible_cmds)
        code = input("Code Invalid. Try again.\n")

    return int(code)


def createAddress(logfile):

    success = False

    while (not success):

        name = input("Enter Name:")
        street = input("Enter the street address:")
        city = input("Enter the city:")
        state = input("Enter the state:")
        zip = input("Enter the zip code:")
        country = input("Enter the two letter country code, e.g. US:")

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
            if (address_from.validation_results and not address_from.validation_results.is_valid):
                raise AddressError(
                    address_from.validation_results.messages[0].text, None, address_from.validation_results.messages[0].code)
            success = True

        except InvalidRequestError as e:
            print("\n", list(e.http_body.values())[0][0], "Please try again.")

        except AddressError as e:
            print("\n", e.args[0], "Please try again.")

    print("Address Created. Address ID: %s" % (address_from.object_id))
    logfile.write("Address Created. Address ID: %s\n" %
                  (address_from.object_id))

    add = {field: address_from[field] for field in add_fields}

    return add


def createParcel(logfile):

    printOptions("These are the possible distance units for your parcel dimensions.", dist_units)
    dist_unit = input("\nEnter the distance unit code:")

    while not (validateCommand(dist_unit, dist_units)):
        dist_unit = input("Code not valid. Try again.")

    dimensions = input(
        "\nEnter length, width, and height separated by space:").split()

    while (not validateDimensions(dimensions) or len(dimensions) < 3):
        dimensions = input(
            "\nDimension not valid. Try again.").split()

    printOptions("These are the possible mass units for your parcel weight.", mass_units)
    mass_unit = input("\nEnter the mass unit code:")

    while (not validateCommand(mass_unit, mass_units)):
        mass_unit = input("\nCode not valid. Try again.")

    weight = input("\nEnter your parcel weight.")
    while (not validateDimensions(weight)):
        weight = input("\nWeight not valid. Try again.")

    try:
        parcel = shippo.Parcel.create(
            length=dimensions[0],
            width=dimensions[1],
            height=dimensions[2],
            distance_unit=dist_units[int(dist_unit)],
            weight=weight,
            mass_unit=mass_units[int(mass_unit)]
        )

    except Exception as e:
        print(e)
        sys.exit(1)

    print("Parcel Created. Parcel ID: %s" % (parcel.object_id))
    logfile.write("Parcel Created. Parcel ID: %s\n" % (parcel.object_id))

    parcel = {field: parcel[field] for field in parcel_fields}

    return parcel


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

        try:
            shipment = shippo.Shipment.create(
                address_from=sender_add,
                address_to=rcpt_add,
                parcels=[parcel],
                asynchronous=False
            )

        except Exception as e:
            print(e)

        else:
            print("Shipment Created. Shipment ID: %s" % (shipment.object_id))
            logfile.write("Shipment Created. Shipment ID: %s\n" %
                          (shipment.object_id))

    else:
        print("Aborting Operation.")


def confirmShipment(sender_add, rcpt_add, parcel):

    print("\nSender Name and Address:", (addressToString(sender_add)))

    print("\nRecipient Name and Address:", (addressToString(rcpt_add)))

    print("\nParcel Information:", (parcelToString(parcel)))

    confirm = input("\nDo you want to continue creating this shipment? [y|n]")

    return confirm.lower() == "y"


def retrieveShipment():
    shipment_id = input("\nEnter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
    except:
        print("No shipment found.")
    else:
        displayShipments(shipment_fields, [shipment])


def retrieveParcelByParcelId():
    parcel_id = input("\nEnter Parcel ID:")

    try:
        parcel = shippo.Parcel.retrieve(parcel_id)
    except:
        print("No parcel found.")
    else:
        displayData(parcel_fields, [parcel])


def retrieveParcelByShipmentId():
    shipment_id = input("\nEnter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
    except:
        print("No parcel found.")
    else:
        displayData(parcel_fields, [shipment.parcels[0]])


def retrieveRatesByShipmentId():
    shipment_id = input("\nEnter Shipment ID:")

    try:
        rates = shippo.Shipment.get_rates(shipment_id, asynchronous=False)
    except:
        print("No rates found.")
    else:
        for rate in rates.results:
            rate.servicelevel = rate.servicelevel.name
        displayData(rate_fields, rates.results)


def retrieveAddressByAddressId():
    address_id = input("\nEnter Address ID:")

    try:
        add = shippo.Address.retrieve(address_id)
    except:
        print("Address not found.")
    else:
        displayData(add_fields, [add])


def retrieveAddressesbyShipmentId():
    shipment_id = input("\nEnter Shipment ID:")

    try:
        shipment = shippo.Shipment.retrieve(shipment_id)
    except:
        print("No shipment found.")
    else:
        displayShipments(["address_from", "address_to"], [shipment])


def retrieveAllShipments():
    shipments = shippo.Shipment.all()
    displayShipments(shipment_fields, shipments.results)


def getLastShipmentId():
    shipments = shippo.Shipment.all()
    
    if (len(shipments) > 1):
        print(shipments.results[0].object_id)
    else:
        print("There are no shipments.")


def retrieveLastShipment():
    shipments = shippo.Shipment.all()

    if (len(shipments) > 1):
        displayShipments(shipment_fields, shipments.results[:1])
    else:
        print("There are no shipments.")


def displayShipments(headers, shipments):
    for shipment in shipments:

        shipment["address_from"] = addressToString(shipment["address_from"])
        shipment["address_to"] = addressToString(shipment["address_to"])
        shipment["parcels"] = list(map(parcelToString, shipment["parcels"]))

    displayData(headers, shipments)

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
                    retrieveAddressesbyShipmentId()
                case 7:
                    retrieveAllShipments()
                case 8:
                    getLastShipmentId()
                case 9:
                    retrieveLastShipment()

            print("-----------------------------------------")
