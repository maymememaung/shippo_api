from prettytable import PrettyTable, ALL

def printOptions(message, dictionary):

    print(message)

    for code, desc in dictionary.items():
        print("%s [%d]" % (desc, code))


def validateCommand(input, dict):

    try:
        code = int(input)
    except:
        return False

    return code in dict


def validateDimensions(dimensions):

    for d in dimensions:
        try:
            d = float(d)
            if d < 0:
                return False
        except:
            return False

    return True


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
    return ("length=%s,width=%s,height=%s %s,weight=%s %s" % (parcel["length"], parcel["width"], parcel["height"], parcel["distance_unit"], parcel["weight"], parcel["mass_unit"]))


def addressToString(address):
    return ("%s, %s, %s %s, %s %s" % (address["name"], address["street1"], address["city"], address["state"], address["zip"], address["country"]))