from datetime import datetime, date, timedelta, time
from decimal import Decimal
from json import JSONEncoder, dumps, loads
from base64 import b64encode
from pydicts import casts, exceptions

# Forma en que debe parsearse los Decimals
class DecimalsWay:
    DecimalString=1  #Uses a String with decimal to detect decimals "Decimal('12.122')"
    String=2  #"12.122"
    Float=3  # 12.122

## Usa
class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            if casts.is_aware(o):
                return casts.dtaware2str(o)
            else: #naive
                return casts.dtnaive2str(o)
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, time):
            if o.utcoffset() is not None: #If it's aware
                raise ValueError("JSON can't represent timezone-aware times.")
            return casts.time2str(o)
        elif isinstance(o, timedelta):
            return casts.timedelta2str(o)
        elif isinstance(o, Decimal):
            return f"Decimal('{o}')"
        elif o.__class__.__name__ in ("Promise", "__proxy__"): #django.utils.functional
            return str(o)
        elif isinstance(o, bytes):
            return b64encode(o).decode("UTF-8")
        elif o.__class__.__name__=="Percentage":
            return o.value
        elif o.__class__.__name__=="Currency":
            return o.amount
        else:
            return super().default(o)

## Usa decimals como floats normalmwente para JS
class MyJSONEncoderDecimalsAsString(MyJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        else:
            return super().default(o)
            
## Usa decimals como floats normalmwente para JS
class MyJSONEncoderDecimalsAsFloat(MyJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        else:
            return super().default(o)

                
def MyJSONEncoder_dumps(r, indent=4):
    return dumps(r, cls=MyJSONEncoder, indent=indent)
                
def MyJSONEncoderDecimalsAsString_dumps(r, indent=4):
    return dumps(r, cls=MyJSONEncoderDecimalsAsString, indent=indent)
                
def MyJSONEncoderDecimalsAsFloat_dumps(r, indent=4):
    return dumps(r, cls=MyJSONEncoderDecimalsAsFloat, indent=indent)


def MyJSONEncoder_loads(s):
    def hooks_MyJSONEncoder(iter_value):
        return hooks(iter_value, DecimalsWay.DecimalString)
    ##############################
    return loads(s, object_hook=hooks_MyJSONEncoder)

def MyJSONEncoderDecimalsAsFloat_loads(s):
    
    def hooks_MyJSONEncoderAsFloat(iter_value):
        return hooks(iter_value, DecimalsWay.Float)
    ####################################
    return loads(s, object_hook=hooks_MyJSONEncoderAsFloat)        

def MyJSONEncoderDecimalsAsString_loads(s):
    def hooks_MyJSONEncoderAsString(iter_value):
        return hooks(iter_value, DecimalsWay.String)
    ######################################
    return loads(s, object_hook=hooks_MyJSONEncoderAsString)
    
    
def hooks(iter_value, decimals_way):
    """
        Iterates a dict or list to cast decimals and dtaware in json.loads using objeck_hook
    """
    def guess_cast(o, decimal_way):
        if decimal_way==DecimalsWay.DecimalString:
            if o.__class__==str and o.startswith("Decimal("):
                try:
                    return eval(o)
                except:
                    pass
                    
        # Guess date
        try:
            return casts.str2date(o)
        except exceptions.CastException:
            pass
            
        #Guess dtaware
        try:
            return casts.str2dtaware(o,"JsUtcIso")
        except exceptions.CastException:
            pass

        #Guess dtnaive
        try:
            return casts.str2dtnaive(o,"JsIso")
        except exceptions.CastException:
            pass

        #Guess time
        try:
            return casts.str2time(o)
        except exceptions.CastException:
            pass
                    
        # Guess date
        try:
            return casts.str2timedelta(o)
        except exceptions.CastException:
            pass

        #Guess Bytes
        try:
            b64bytes=casts.str2bytes(o)# o is a b64 string
            return casts.base64bytes2bytes(b64bytes)
        except:
            pass

        return o
    ########################################################
    
    if isinstance(iter_value, dict):
        for k, v in iter_value.items():
            if isinstance(v, dict):
                iter_value[k]=hooks(v, decimals_way)
            elif isinstance(iter_value, list):
                for i in v:
                    i=hooks(v, decimals_way)
            else:
                guessed=guess_cast(v, decimals_way)
#                print("GUESS_CAST", iter_value[k], decimals_way, "GOT", guessed, guessed.__class__)
                iter_value[k]=guessed
    elif isinstance(iter_value, list):
        for i in v:
            i=hooks(i, decimals_way)
    return iter_value
    
    

