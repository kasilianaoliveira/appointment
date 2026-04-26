from asyncpg.compat import StrEnum


class PaymentsMethod(StrEnum):
    CASH = "dinheiro"
    DEBIT_CARD = "cartão de débito"
    CREDIT_CARD = "cartão de crédito"
    PIX = "pix"
