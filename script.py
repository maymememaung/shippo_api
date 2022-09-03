import shippo

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

def printCommands():

    print ("These are the possible commands with codes.")

    for code, cmd in possible_cmds.items():
        print("%s [%d]" % (cmd, code))

def validateCommand(input):

    try:
        code = int(input)
    except:
        return False

    return code in possible_cmds


def commandInput():

    printCommands()
    code = input("Enter command code.\n")

    while not (validateCommand(code)):
        printCommands()
        code = input("Enter command code.\n")

    return int(code)

def addressInput():
    pass


def createShipment():
    pass

if __name__ == "__main__":

    quit = False

    print("-----------------------------------------")

    while not quit:

        cmd_code = commandInput()

        match cmd_code:
            case -1:
                quit = True
            case 0:
                createShipment()
            case 1:
                print(possible_cmds[1])

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