from genie.conf import Genie
from genie import parsergen
from genie.utils.diff import Diff
from pprint import pprint


"""
EIGRP-IPv4 Neighbors for AS(100)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
1   10.1.1.3                Tu1                      10 02:51:11   26   156  0  3
0   10.1.1.4                Tu1                      12 02:51:12    5   100  0  4

"""
def show_ip_eigrp_neighbors(uut):


    # Use connect method to initiate connection to the device under test
    if not uut.is_connected():
        uut.connect()

    command = 'show ip eigrp neighbors'
    headers = [["H", "Address", "Interface", "Hold", "Uptime", "SRTT", "RTO", " Q ", "Seq"],
        ['', '', '', '(sec)', '', '(ms)', '', 'Cnt', 'Num']
        ]

    # this one sort of works, however it catches the second line of headers as dict in the
    # resulting data structure
    # headers = ["H", "Address", "Interface", "Hold", "Uptime", "SRTT", "RTO", " Q ", "Seq"]
    label_fields = ["H", "Address", "Interface", "Uptime", "SRTT", "RTO", "QCnt", "SeqNum"]
    output = uut.execute(command)
    eigrp_dict = parsergen.oper_fill_tabular(device_output=output,
                                            device_os='iosxe',
                                            header_fields=headers,
                                            label_fields=label_fields,
                                            index=[2])
    return eigrp_dict.entries


tb = Genie.init('../default_testbed.yaml')
d = tb.devices.headend1
pprint(show_ip_eigrp_neighbors(d))
