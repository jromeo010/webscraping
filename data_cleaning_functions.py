import csv,re


def write_output(ROW,OUTPUT_CSV):
    with open(OUTPUT_CSV,'ab') as file:
        writer = csv.writer(file,dialect='excel')
        writer.writerow(ROW)



def CLEAN_VICS_PRICE(VICS_PRICE):
        try:
            VICS_PRICE = re.findall(r'(?:[\$]{1}[,\d]+.?\d*)',VICS_PRICE)
            VICS_PRICE = float(VICS_PRICE[0].replace('$',''))
        except:
            VICS_PRICE = None
            pass
        return VICS_PRICE

def CLEAN_PRICE(PRICE):
        try:
            PRICE = PRICE.replace('$','') #replace text
        except:
            pass
        return PRICE
def CLEAN_SIZE(SIZE):
        try:
            SIZE = SIZE.partition('  |')[0]#split string to include relevant info
            SIZE = SIZE.replace('ct','')
            SIZE = SIZE.replace('each','')
            SIZE = SIZE.replace('144 fl oz','12')
            SIZE = SIZE.replace('144 oz', '12')
            SIZE = SIZE.replace('72 fl oz', '6')
            SIZE = SIZE.replace('72 oz', '6')
            SIZE = SIZE.replace('6 oz', '6')
            SIZE = SIZE.replace('250 ml', '4')
            SIZE = SIZE.replace('48 oz', '4')
            SIZE = SIZE.replace('64 oz', '4')
            SIZE = SIZE.replace('24 oz', '2')
            SIZE = SIZE.replace('19.2 oz', '2')
            SIZE = SIZE.replace('24 fl oz', '2')
            SIZE = SIZE.replace('25.4 oz', '2')
            SIZE = SIZE.replace('25 oz', '2')
            SIZE = SIZE.replace('22 oz', '2')
            SIZE = SIZE.replace('1 pint', '1')
            SIZE = SIZE.replace('12 fl oz', '1')
            SIZE = SIZE.replace('12 oz', '1')
            SIZE = SIZE.strip()
        except:
            pass
        return SIZE
