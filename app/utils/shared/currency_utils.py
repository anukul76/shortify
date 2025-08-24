from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional, Union
from enum import Enum
import re


class CurrencyCode(str, Enum):
    """Supported currency codes (ISO 4217)"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    INR = "INR"
    JPY = "JPY"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    CNY = "CNY"
    SGD = "SGD"
    HKD = "HKD"
    NZD = "NZD"
    SEK = "SEK"
    NOK = "NOK"
    DKK = "DKK"
    PLN = "PLN"
    CZK = "CZK"
    HUF = "HUF"
    RUB = "RUB"
    BRL = "BRL"
    MXN = "MXN"
    ZAR = "ZAR"
    KRW = "KRW"
    THB = "THB"
    MYR = "MYR"
    PHP = "PHP"
    IDR = "IDR"
    VND = "VND"
    AED = "AED"
    SAR = "SAR"
    QAR = "QAR"
    KWD = "KWD"
    BHD = "BHD"
    OMR = "OMR"
    JOD = "JOD"
    LBP = "LBP"
    EGP = "EGP"
    TRY = "TRY"
    ILS = "ILS"


class CurrencyInfo:
    """Currency information class"""
    def __init__(self, code: str, name: str, symbol: str, decimal_places: int = 2):
        self.code = code
        self.name = name
        self.symbol = symbol
        self.decimal_places = decimal_places


class CurrencyUtil:
    """Utility class for currency operations"""
    
    # Currency information mapping
    CURRENCY_INFO: Dict[str, CurrencyInfo] = {
        "USD": CurrencyInfo("USD", "US Dollar", "$", 2),
        "EUR": CurrencyInfo("EUR", "Euro", "€", 2),
        "GBP": CurrencyInfo("GBP", "British Pound", "£", 2),
        "INR": CurrencyInfo("INR", "Indian Rupee", "₹", 2),
        "JPY": CurrencyInfo("JPY", "Japanese Yen", "¥", 0),
        "CAD": CurrencyInfo("CAD", "Canadian Dollar", "C$", 2),
        "AUD": CurrencyInfo("AUD", "Australian Dollar", "A$", 2),
        "CHF": CurrencyInfo("CHF", "Swiss Franc", "CHF", 2),
        "CNY": CurrencyInfo("CNY", "Chinese Yuan", "¥", 2),
        "SGD": CurrencyInfo("SGD", "Singapore Dollar", "S$", 2),
        "HKD": CurrencyInfo("HKD", "Hong Kong Dollar", "HK$", 2),
        "NZD": CurrencyInfo("NZD", "New Zealand Dollar", "NZ$", 2),
        "SEK": CurrencyInfo("SEK", "Swedish Krona", "kr", 2),
        "NOK": CurrencyInfo("NOK", "Norwegian Krone", "kr", 2),
        "DKK": CurrencyInfo("DKK", "Danish Krone", "kr", 2),
        "PLN": CurrencyInfo("PLN", "Polish Zloty", "zł", 2),
        "CZK": CurrencyInfo("CZK", "Czech Koruna", "Kč", 2),
        "HUF": CurrencyInfo("HUF", "Hungarian Forint", "Ft", 2),
        "RUB": CurrencyInfo("RUB", "Russian Ruble", "₽", 2),
        "BRL": CurrencyInfo("BRL", "Brazilian Real", "R$", 2),
        "MXN": CurrencyInfo("MXN", "Mexican Peso", "$", 2),
        "ZAR": CurrencyInfo("ZAR", "South African Rand", "R", 2),
        "KRW": CurrencyInfo("KRW", "South Korean Won", "₩", 0),
        "THB": CurrencyInfo("THB", "Thai Baht", "฿", 2),
        "MYR": CurrencyInfo("MYR", "Malaysian Ringgit", "RM", 2),
        "PHP": CurrencyInfo("PHP", "Philippine Peso", "₱", 2),
        "IDR": CurrencyInfo("IDR", "Indonesian Rupiah", "Rp", 0),
        "VND": CurrencyInfo("VND", "Vietnamese Dong", "₫", 0),
        "AED": CurrencyInfo("AED", "UAE Dirham", "د.إ", 2),
        "SAR": CurrencyInfo("SAR", "Saudi Riyal", "﷼", 2),
        "QAR": CurrencyInfo("QAR", "Qatari Riyal", "﷼", 2),
        "KWD": CurrencyInfo("KWD", "Kuwaiti Dinar", "د.ك", 3),
        "BHD": CurrencyInfo("BHD", "Bahraini Dinar", ".د.ب", 3),
        "OMR": CurrencyInfo("OMR", "Omani Rial", "﷼", 3),
        "JOD": CurrencyInfo("JOD", "Jordanian Dinar", "د.ا", 3),
        "LBP": CurrencyInfo("LBP", "Lebanese Pound", "ل.ل", 2),
        "EGP": CurrencyInfo("EGP", "Egyptian Pound", "£", 2),
        "TRY": CurrencyInfo("TRY", "Turkish Lira", "₺", 2),
        "ILS": CurrencyInfo("ILS", "Israeli Shekel", "₪", 2),
    }
    
    @staticmethod
    def is_valid_currency_code(currency_code: str) -> bool:
        """Check if a currency code is valid"""
        return currency_code.upper() in CurrencyUtil.CURRENCY_INFO
    
    @staticmethod
    def get_currency_info(currency_code: str) -> Optional[CurrencyInfo]:
        """Get currency information by code"""
        return CurrencyUtil.CURRENCY_INFO.get(currency_code.upper())
    
    @staticmethod
    def get_currency_symbol(currency_code: str) -> str:
        """Get currency symbol by code"""
        info = CurrencyUtil.get_currency_info(currency_code)
        return info.symbol if info else currency_code.upper()
    
    @staticmethod
    def get_currency_name(currency_code: str) -> str:
        """Get currency name by code"""
        info = CurrencyUtil.get_currency_info(currency_code)
        return info.name if info else currency_code.upper()
    
    @staticmethod
    def get_decimal_places(currency_code: str) -> int:
        """Get number of decimal places for a currency"""
        info = CurrencyUtil.get_currency_info(currency_code)
        return info.decimal_places if info else 2
    
    @staticmethod
    def format_amount(
        amount: Union[int, float, Decimal, str],
        currency_code: str,
        show_symbol: bool = True,
        show_code: bool = False,
        locale: str = "en_US"
    ) -> str:
        """Format currency amount with proper decimal places and symbol"""
        # Convert to Decimal for precise calculations
        if isinstance(amount, str):
            amount = Decimal(amount)
        elif isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        # Get currency info
        info = CurrencyUtil.get_currency_info(currency_code)
        if not info:
            raise ValueError(f"Invalid currency code: {currency_code}")
        
        # Round to appropriate decimal places
        decimal_places = info.decimal_places
        quantized_amount = amount.quantize(
            Decimal('0.1') ** decimal_places,
            rounding=ROUND_HALF_UP
        )
        
        # Format the amount
        if decimal_places == 0:
            formatted_amount = f"{quantized_amount:,.0f}"
        else:
            formatted_amount = f"{quantized_amount:,.{decimal_places}f}"
        
        # Add symbol and/or code
        result = formatted_amount
        if show_symbol:
            result = f"{info.symbol}{result}"
        if show_code:
            result = f"{result} {info.code}"
        
        return result
    
    @staticmethod
    def parse_amount(amount_str: str, currency_code: str) -> Decimal:
        """Parse currency amount string to Decimal"""
        # Remove currency symbols and codes
        info = CurrencyUtil.get_currency_info(currency_code)
        if info:
            # Remove currency symbol and code
            cleaned = amount_str.replace(info.symbol, "").replace(info.code, "")
        else:
            cleaned = amount_str
        
        # Remove common formatting characters
        cleaned = re.sub(r'[,\s]', '', cleaned)
        
        # Convert to Decimal
        try:
            return Decimal(cleaned)
        except Exception as e:
            raise ValueError(f"Invalid amount format: {amount_str}") from e
    
    @staticmethod
    def convert_to_minor_units(amount: Union[int, float, Decimal, str], currency_code: str) -> int:
        """Convert currency amount to minor units (cents, paise, etc.)"""
        # Convert to Decimal
        if isinstance(amount, str):
            amount = Decimal(amount)
        elif isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        # Get decimal places
        decimal_places = CurrencyUtil.get_decimal_places(currency_code)
        
        # Convert to minor units
        multiplier = Decimal('10') ** decimal_places
        return int(amount * multiplier)
    
    @staticmethod
    def convert_from_minor_units(minor_units: int, currency_code: str) -> Decimal:
        """Convert minor units to currency amount"""
        decimal_places = CurrencyUtil.get_decimal_places(currency_code)
        divisor = Decimal('10') ** decimal_places
        return Decimal(minor_units) / divisor
    
    @staticmethod
    def is_zero_amount(amount: Union[int, float, Decimal, str], currency_code: str) -> bool:
        """Check if amount is zero considering currency precision"""
        return CurrencyUtil.compare_amounts(amount, 0, currency_code) == 0
    
    @staticmethod
    def is_positive_amount(amount: Union[int, float, Decimal, str], currency_code: str) -> bool:
        """Check if amount is positive considering currency precision"""
        return CurrencyUtil.compare_amounts(amount, 0, currency_code) > 0
    
    @staticmethod
    def is_negative_amount(amount: Union[int, float, Decimal, str], currency_code: str) -> bool:
        """Check if amount is negative considering currency precision"""
        return CurrencyUtil.compare_amounts(amount, 0, currency_code) < 0
    
    @staticmethod
    def get_absolute_amount(amount: Union[int, float, Decimal, str], currency_code: str) -> Decimal:
        """Get absolute value of currency amount"""
        # Convert to Decimal
        if isinstance(amount, str):
            amount = Decimal(amount)
        elif isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        # Get absolute value
        result = abs(amount)
        
        # Round to appropriate decimal places
        decimal_places = CurrencyUtil.get_decimal_places(currency_code)
        return result.quantize(
            Decimal('0.1') ** decimal_places,
            rounding=ROUND_HALF_UP
        )
    
    @staticmethod
    def validate_amount(amount: Union[int, float, Decimal, str], 
                       currency_code: str,
                       min_amount: Optional[Union[int, float, Decimal, str]] = None,
                       max_amount: Optional[Union[int, float, Decimal, str]] = None) -> bool:
        """Validate currency amount within optional min/max bounds"""
        try:
            # Convert to Decimal
            if isinstance(amount, str):
                amount = Decimal(amount)
            elif isinstance(amount, (int, float)):
                amount = Decimal(str(amount))
            
            # Check if currency is valid
            if not CurrencyUtil.is_valid_currency_code(currency_code):
                return False
            
            # Check min amount
            if min_amount is not None:
                if CurrencyUtil.compare_amounts(amount, min_amount, currency_code) < 0:
                    return False
            
            # Check max amount
            if max_amount is not None:
                if CurrencyUtil.compare_amounts(amount, max_amount, currency_code) > 0:
                    return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_supported_currencies() -> Dict[str, CurrencyInfo]:
        """Get all supported currencies"""
        return CurrencyUtil.CURRENCY_INFO.copy()
    
    @staticmethod
    def get_currency_codes() -> list:
        """Get list of all supported currency codes"""
        return list(CurrencyUtil.CURRENCY_INFO.keys())


# Quick helper functions
def format_currency(amount: Union[int, float, Decimal, str], currency_code: str) -> str:
    """Quick currency formatting"""
    return CurrencyUtil.format_amount(amount, currency_code)


def parse_currency(amount_str: str, currency_code: str) -> Decimal:
    """Quick currency parsing"""
    return CurrencyUtil.parse_amount(amount_str, currency_code)


def is_valid_currency(currency_code: str) -> bool:
    """Quick currency validation"""
    return CurrencyUtil.is_valid_currency_code(currency_code)