# Módulo principal del E-Commerce - Lab 05 IS489
# Incluye: Pagos, Descuentos y Facturas

class PasarelaPagos:
    """Simula pasarela externa (se reemplaza con Mock en pruebas)"""
    def procesar_pago(self, monto, tarjeta):
        pass

class PagoService:
    MONTO_MINIMO = 1.0
    LIMITE_DIARIO = 5000.0
    TARJETAS_VALIDAS = ["visa", "mastercard"]
    IGV = 0.18

    def __init__(self, pasarela: PasarelaPagos):
        self.pasarela = pasarela

    def calcular_total_con_igv(self, subtotal: float) -> float:
        # Aplica IGV del 18% al subtotal
        if subtotal < 0:
            raise ValueError("Subtotal no puede ser negativo")
        return round(subtotal * (1 + self.IGV), 2)

    def validar_monto(self, monto: float) -> bool:
        # Verifica que el monto esté dentro de los límites
        return self.MONTO_MINIMO <= monto <= self.LIMITE_DIARIO

    def procesar_compra(self, monto: float, tarjeta: str) -> dict:
        # Procesa la compra validando tarjeta y monto
        if tarjeta.lower() not in self.TARJETAS_VALIDAS:
            return {"exitoso": False, "mensaje": "Tarjeta no válida"}
        if not self.validar_monto(monto):
            return {"exitoso": False, "mensaje": "Monto fuera de límites"}
        self.pasarela.procesar_pago(monto, tarjeta)
        return {"exitoso": True, "mensaje": "Pago procesado", "total": monto}


class DescuentoService:
    CUPONES = {"DESC10": 0.10, "DESC20": 0.20, "VERANO15": 0.15}

    def aplicar_cupon(self, subtotal: float, cupon: str) -> dict:
        # Aplica cupón si es válido y retorna nuevo total
        cupon = cupon.upper()
        if cupon not in self.CUPONES:
            return {"exitoso": False, "mensaje": "Cupón no válido", "total": subtotal}
        descuento = round(subtotal * self.CUPONES[cupon], 2)
        return {"exitoso": True, "descuento": descuento, "total": round(subtotal - descuento, 2)}

    def descuento_por_volumen(self, subtotal: float, cantidad: int) -> float:
        # 15% para 10+ unidades, 10% para 5+, sin descuento el resto
        if cantidad >= 10:
            return round(subtotal * 0.85, 2)
        elif cantidad >= 5:
            return round(subtotal * 0.90, 2)
        return subtotal


class FacturaService:
    _correlativo = 0

    def __init__(self, serie: str = "F001"):
        self.serie = serie

    def generar_factura(self, cliente: str, productos: list, subtotal: float, descuento: float = 0.0) -> dict:
        # Genera factura con número único, IGV y total final
        if not cliente:
            raise ValueError("Cliente requerido")
        if not productos:
            raise ValueError("Debe tener productos")
        if subtotal <= 0:
            raise ValueError("Subtotal debe ser mayor a cero")
        FacturaService._correlativo += 1
        base = round(subtotal - descuento, 2)
        igv = round(base * 0.18, 2)
        return {
            "numero": f"{self.serie}-{str(FacturaService._correlativo).zfill(5)}",
            "cliente": cliente,
            "productos": productos,
            "subtotal": subtotal,
            "descuento": descuento,
            "igv": igv,
            "total": round(base + igv, 2)
        }