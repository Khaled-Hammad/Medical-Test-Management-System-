class Test:
    #1. Name: Hemoglobin (Hgb); Range: > 13.8, < 17.2; Unit: g/dL, 00-03-04
    def __init__(self, symbol, minValue, maxValue, unit, days, hour, mins):
        self._symbol = symbol
        self._minValue = minValue
        self._maxValue = maxValue
        self._unit = unit
        self._hour = hour
        self._mins = mins
        self._days = days

    #===========================geters===========================
    def get_symbol(self):
        return self._symbol
    
    def get_minValue(self):
        return self._minValue
    
    def get_maxValue(self):
        return self._maxValue
    
    def get_unit(self):
        return self._unit
    
    def get_hour(self):
        return self._hour
    
    def get_mins(self):
        return self._mins
    
    def get_days(self):
        return self._days

    #===========================seters===========================
    def set_symbol(self, symbol):
        self._symbol = symbol
    
    def set_minValue(self, minValue):
        self._minValue = minValue
    
    def set_maxValue(self, maxValue):
        self._maxValue = maxValue
    
    def set_unit(self, unit):
        self._unit = unit
    
    def set_hour(self, hour):
        self._hour = hour
    
    def set_mins(self, mins):
        self._mins = mins
    
    def set_days(self, days):
        self._days = days

        
    def to_string(self):
        print("  symbol =", self._symbol, "  minValue =", self._minValue, "  maxValue =", self._maxValue, "  unit =", self._unit, "  Days =", self._days, "  Hour =", self._hour, "  min =", self._mins)
        
        



        
# 1. Name: Hemoglobin (Hgb); Range: > 13.8, < 17.2; Unit: g/dL, 00-03-04
# 2. Name: Blood Glucose Test (BGT); Range: > 70, < 99; Unit: mg/dL, 00-12-06
# 3. Name: LDL Cholesterol Low-Density Lipoprotein (LDL); Range: < 100; Unit: mg/dL, 00-17-06
# 4. Name: Systolic Blood Pressure (systole); Range: < 120; Unit: mm Hg, 00-08-04
# 5. Name: Diastolic Blood Pressure (diastole); Range: < 80; Unit: mm Hg, 00-10-00