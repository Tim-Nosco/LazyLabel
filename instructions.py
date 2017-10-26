from util.add import Add
from util.sub import Sub
from util.label import Label
from util.br import Br
from util.icmp import Icmp
from util.ret import Ret
from util.assign import Assign

by_name = {"add":Add,"sub":Sub,"br":Br,"icmp":Icmp,"ret":Ret,"label":Label,"assign":Assign}
as_list = by_name.values()