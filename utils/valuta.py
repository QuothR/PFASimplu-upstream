import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from cursvalutarbnr import ron_exchange_rate
from functools import lru_cache
import cursvalutarbnr
import requests
import xmltodict
from decimal import Decimal, ROUND_HALF_UP


# BNR a mutat XML-urile de curs de pe www.bnr.ro pe curs.bnr.ro (august 2026).
# www.bnr.ro raspunde acum cu redirect 302 catre o pagina HTML, iar libraria
# cursvalutarbnr 1.0.5 are hostul vechi scris in cod. Inlocuim functia de
# descarcare cu una identica, dar cu hostul nou.
BNR_HOST = "https://curs.bnr.ro"


def _get_bnr_rates_for_year(year: int):
    cache = True
    url = f"{BNR_HOST}/files/xml/years/nbrfxrates{year}.xml"
    r = requests.get(url)
    bnr_ron_rates = xmltodict.parse(r.content)

    if "Cube" not in bnr_ron_rates["DataSet"]["Body"]:
        cache = False
        r = requests.get(f"{BNR_HOST}/nbrfxrates10days.xml")
        bnr_ron_rates = xmltodict.parse(r.content)

    exchange_rates = {}
    for entries in bnr_ron_rates["DataSet"]["Body"]["Cube"]:
        rates = {}
        for entry in entries["Rate"]:
            currency = entry["@currency"]
            value = Decimal(entry["#text"])
            multiplier = Decimal(entry.get("@multiplier", "1"))
            rates[currency] = float(
                (value * multiplier).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
            )
        exchange_rates[entries["@date"]] = rates

    return exchange_rates, cache


cursvalutarbnr.get_bnr_rates_for_year = _get_bnr_rates_for_year


@lru_cache(maxsize=None)
def to_ron(amount: float, currency: str, dateValue: datetime.date):
    if isinstance(dateValue, str):
        dateValue = datetime.datetime.strptime(dateValue, "%Y-%m-%d").date()
    return ron_exchange_rate(
        amount, currency, None if dateValue == "" else dateValue.isoformat()
    )

@lru_cache(maxsize=None)
def ron_to_eur(amount: float, year: int):
    january = datetime.date(year, 1, 5).isoformat()
    return round(
        (amount / ron_exchange_rate(1, "EUR", january)),
        2,
    )


class TipTranzactie(models.TextChoices):
    BANCAR = "BANCAR", _("💳 BANCAR")
    NUMERAR = "NUMERAR", _("💵 NUMERAR")


class Valuta(models.TextChoices):
    RON = "RON", _('RON - Romania')
    EUR = "EUR", _("EUR - European Union Zone")
    USD = "USD", _("USD - USA")
    GBP = "GBP", _("GBP - UK")
    CHF = "CHF", _("CHF - Switzerland")
    CAD = "CAD", _("CAD - Canada")
    AED = "AED", _("AED - UAE")
    AUD = "AUD", _("AUD - Australia")
    BGN = "BGN", _("BGN - Bulgaria")
    BRL = "BRL", _("BRL - Brazil")
    CNY = "CNY", _("CNY - China")
    CZK = "CZK", _("CZK - Czech Republic")
    DKK = "DKK", _("DKK - Denmark")
    EGP = "EGP", _("EGP - Egypt")
    HUF = "HUF", _("HUF - Hungary")
    INR = "INR", _("INR - India")
    JPY = "JPY", _("JPY - Japan")
    KRW = "KRW", _("KRW - South Korea")
    MDL = "MDL", _("MDL - Moldova")
    MXN = "MXN", _("MXN - Mexico")
    NOK = "NOK", _("NOK - Norway")
    NZD = "NZD", _("NZD - New Zealand")
    PLN = "PLN", _("PLN - Poland")
    RSD = "RSD", _("RSD - Serbia")
    RUB = "RUB", _("RUB - Russia")
    SEK = "SEK", _("SEK - Sweden")
    THB = "THB", _("THB - Thailand")
    TRY = "TRY", _("TRY - Turkey")
    UAH = "UAH", _("UAH - Ukraine")
    XAU = "XAU", _("XAU - Gold")
    XDR = "XDR", _("XDR - IMF Special Drawing Rights")
    ZAR = "ZAR", _("ZAR - South Africa")