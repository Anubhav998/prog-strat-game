import pprint


def pretty_print(output):
    """pretty prints an output

    :param output: any python structure
    :return: string
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(output)
