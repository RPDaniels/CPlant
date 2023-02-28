import csv
import sqlcplants

class Language:
    def __init__(self, lang):
        self.lang = lang
        self.dict = {}
        if self.lang != "en":
            self.read_dict_from_csv()
            self.read_dict_from_db()

    def read_dict_from_csv(self):
        with open(f"{self.lang}.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.dict[row[0]] = row[1]

    def read_dict_from_db(self):
        dict2 = sqlcplants.getDictionary()
        self.dict.update(dict2)

    def get(self, key):
        if self.lang != "en":
            val = self.dict.get(key)
            if val == None:
                val = "*" + key
        else:
            val = key
        return val

    def rget(self, value):
        #print("value in rget:"+value)
        if self.lang != "en":
            for k, v in self.dict.items():
                if v == value:
                  return k
            return "*" + value
        else:
            return value

