from genie import parsergen


def show_ip_eigrp_neighbors(uut):
    """
    Parsing show ip eigrp neigbors using parsergen

    sample output
    EIGRP-IPv4 Neighbors for AS(100)
    H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                       (sec)         (ms)       Cnt Num
    1   10.1.1.3                Tu1                      10 02:51:11   26   156  0  3
    0   10.1.1.4                Tu1                      12 02:51:12    5   100  0  4

    """ # noqa
    # Use connect method to initiate connection to the device under test
    if not uut.is_connected():
        uut.connect()

    # collect show command output
    command = 'show ip eigrp neighbors'
    output = uut.execute(command)

    try:
        headers = ["H", "Address", "Interface", "Hold",
                   "Uptime", "SRTT", "RTO", " Q ", "Seq"]

        label_fields = ["H", "Address", "Interface", "Uptime",
                        "SRTT", "RTO", "QCnt", "SeqNum"]

        eigrp_dict = parsergen.oper_fill_tabular(device_output=output,
                                                 device_os='iosxe',
                                                 header_fields=headers,
                                                 label_fields=label_fields,
                                                 index=[1])
        if '' in eigrp_dict.entries:
            del eigrp_dict.entries['']

        return eigrp_dict.entries

    except Exception as e:
        pass
