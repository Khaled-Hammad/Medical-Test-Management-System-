import re

class Record:
    # 2024-01-01 14:10
    def __init__ (self, name, begin_date, result, unit, status, completed_date):
        # print(completed_date)
        # try:
                self._name = name
                self._begin_date = begin_date
                self._completed_date = completed_date
                self._begin_year = int(begin_date.split("-")[0])
                self._begin_month = int(begin_date.split("-")[1])
                self._begin_day = int(begin_date.split("-")[2].split(" ")[0])
                self._begin_hour = int(begin_date.split(" ")[1].split(":")[0])
                self._begin_minute = int(begin_date.split(" ")[1].split(":")[1])
                self._result = result
                self._unit = unit
                self._status = status
                if re.match(r"[Cc]ompleted", self._status) is not None:
                    self._completed_year = int(completed_date.split("-")[0])
                    self._completed_month = int(completed_date.split("-")[1])
                    self._completed_day = int(completed_date.split("-")[2].split(" ")[0])
                    self._completed_hour = int(completed_date.split(" ")[1].split(":")[0])
                    self._completed_minute = int(completed_date.split(" ")[1].split(":")[1])
                else:
                    self._completed_year = None
                    self._completed_month = None
                    self._completed_day = None
                    self._completed_hour = None
                    self._completed_minute = None
        # except Exception:
        #     print("not valid date entery")
            
        
    #============================Getters===========================
    def get_name(self):
        return self._name

    def get_begin_date(self):
        return self._begin_date

    def get_begin_year(self):
        return self._begin_year

    def get_begin_month(self):
        return self._begin_month

    def get_begin_day(self):
        return self._begin_day

    def get_begin_hour(self):
        return self._begin_hour

    def get_begin_minute(self):
        return self._begin_minute

    def get_result(self):
        return self._result

    def get_unit(self):
        return self._unit

    def get_status(self):
        return self._status

    def get_completed_date(self):
        return self._completed_date

    def get_completed_year(self):
        return self._completed_year

    def get_completed_month(self):
        return self._completed_month

    def get_completed_day(self):
        return self._completed_day

    def get_completed_hour(self):
        return self._completed_hour

    def get_completed_minute(self):
        return self._completed_minute

    #================================Setters===========================
    
    def set_name(self, name):
        self._name = name

    def set_begin_year(self, begin_year):
        self._begin_year = begin_year

    def set_begin_month(self, begin_month):
        self._begin_month = begin_month

    def set_begin_day(self, begin_day):
        self._begin_day = begin_day

    def set_begin_hour(self, begin_hour):
        self._begin_hour = begin_hour

    def set_begin_minute(self, begin_minute):
        self._begin_minute = begin_minute

    def set_result(self, result):
        self._result = result

    def set_unit(self, unit):
        self._unit = unit

    def set_status(self, status):
        self._status = status

    def set_completed_year(self, completed_year):
        self._completed_year = completed_year

    def set_completed_month(self, completed_month):
        self._completed_month = completed_month

    def set_completed_day(self, completed_day):
        self._completed_day = completed_day

    def set_completed_hour(self, completed_hour):
        self._completed_hour = completed_hour

    def set_completed_minute(self, completed_minute):
        self._completed_minute = completed_minute

    def str(self):
        print(f"name='{self._name}', "
                f"begin_date='{self._begin_year}-{self._begin_month}-{self._begin_day}', "
                f"begin_time='{self._begin_hour}:{self._begin_minute}', "
                f"result='{self._result}', unit='{self._unit}', status='{self._status}'\n, "
                f"completed_date='{self._completed_year}-{self._completed_month}-{self._completed_day}', "
                f"completed_time='{self._completed_hour}:{self._completed_minute}')\n")
