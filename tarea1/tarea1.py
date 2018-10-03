from Afnd import Afnd

import pdb


regExp = "|..baba"
# regExp = "|ab"

afnd1 = Afnd(regExp)
afnd1.addLoopsTexto()
afnd1.convertToAfd()

# pdb.set_trace();True