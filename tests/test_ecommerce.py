# Pruebas unitarias del E-Commerce - Lab 05 IS489
# Patrón AAA: Arrange, Act, Assert | Framework: pytest + MagicMock

import pytest
from unittest.mock import MagicMock
from ecommerce.ecommerce import PagoService, PasarelaPagos, DescuentoService, FacturaService


# ── PAGOS ────────────────────────────────────────────────

def test_calcula_igv_correctamente():
    # Arrange
    servicio = PagoService(MagicMock())
    # Act
    total = servicio.calcular_total_con_igv(100.0)
    # Assert
    assert total == 118.0

def test_subtotal_negativo_lanza_error():
    servicio = PagoService(MagicMock())
    with pytest.raises(ValueError):
        servicio.calcular_total_con_igv(-10.0)

def test_monto_minimo_es_valido():
    # Boundary Testing: valor exacto en el límite inferior
    servicio = PagoService(MagicMock())
    assert servicio.validar_monto(1.0) is True

def test_monto_por_debajo_minimo_invalido():
    servicio = PagoService(MagicMock())
    assert servicio.validar_monto(0.99) is False

def test_monto_maximo_es_valido():
    # Boundary Testing: valor exacto en el límite superior
    servicio = PagoService(MagicMock())
    assert servicio.validar_monto(5000.0) is True

def test_compra_exitosa_con_visa():
    # Mock de pasarela para aislar la prueba
    pasarela_mock = MagicMock()
    servicio = PagoService(pasarela_mock)
    resultado = servicio.procesar_compra(200.0, "visa")
    assert resultado["exitoso"] is True
    pasarela_mock.procesar_pago.assert_called_once_with(200.0, "visa")

def test_tarjeta_invalida_rechazada():
    servicio = PagoService(MagicMock())
    resultado = servicio.procesar_compra(200.0, "amex")
    assert resultado["exitoso"] is False


# ── DESCUENTOS ───────────────────────────────────────────

def test_cupon_valido_aplica_descuento():
    servicio = DescuentoService()
    resultado = servicio.aplicar_cupon(100.0, "DESC20")
    assert resultado["exitoso"] is True
    assert resultado["total"] == 80.0

def test_cupon_invalido_rechazado():
    servicio = DescuentoService()
    resultado = servicio.aplicar_cupon(100.0, "PROMO2025")
    assert resultado["exitoso"] is False

def test_descuento_volumen_10_unidades():
    servicio = DescuentoService()
    assert servicio.descuento_por_volumen(100.0, 10) == 85.0

def test_sin_descuento_menos_5_unidades():
    servicio = DescuentoService()
    assert servicio.descuento_por_volumen(100.0, 3) == 100.0


# ── FACTURAS ─────────────────────────────────────────────

def test_factura_generada_correctamente():
    servicio = FacturaService()
    factura = servicio.generar_factura("Juan Pérez", ["Laptop"], 100.0)
    assert factura["total"] == 118.0
    assert factura["igv"] == 18.0
    assert "F001" in factura["numero"]

def test_factura_con_descuento_calcula_bien():
    servicio = FacturaService()
    factura = servicio.generar_factura("Ana García", ["Mouse"], 100.0, descuento=20.0)
    assert factura["total"] == 94.4  # (100-20) * 1.18

def test_cliente_vacio_lanza_error():
    servicio = FacturaService()
    with pytest.raises(ValueError):
        servicio.generar_factura("", ["Laptop"], 100.0)

def test_sin_productos_lanza_error():
    servicio = FacturaService()
    with pytest.raises(ValueError):
        servicio.generar_factura("Juan", [], 100.0)