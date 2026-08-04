from app.dominio.reserva.entidad import Reserva
from app.dominio.reserva.excepciones import ReservaNoExiste
from app.puertos.salida.repositorio_reserva import RepositorioReserva


class CrearReserva:
    def __init__(self, repositorio: RepositorioReserva):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int = None, area_comun_id: int = None, propietario_id: int = None, fecha=None, hora_inicio=None, hora_fin=None) -> Reserva:
        return self.repositorio.crear(Reserva(
            condominio_id=condominio_id or 1, area_comun_id=area_comun_id,
            propietario_id=propietario_id, fecha=fecha,
            hora_inicio=hora_inicio, hora_fin=hora_fin,
        ))


class ListarReservas:
    def __init__(self, repositorio: RepositorioReserva):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, area_comun_id: int = None, propietario_id: int = None, fecha: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, area_comun_id=area_comun_id, propietario_id=propietario_id, fecha=fecha, pagina=pagina, por_pagina=por_pagina)


class ObtenerReserva:
    def __init__(self, repositorio: RepositorioReserva):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Reserva:
        reserva = self.repositorio.obtener_por_id(id)
        if not reserva:
            raise ReservaNoExiste("Reserva no encontrada")
        return reserva


class ActualizarReserva:
    def __init__(self, repositorio: RepositorioReserva):
        self.repositorio = repositorio

    def ejecutar(self, id: int, fecha=None, hora_inicio=None, hora_fin=None, estado: str = None) -> Reserva:
        reserva = self.repositorio.obtener_por_id(id)
        if not reserva:
            raise ReservaNoExiste("Reserva no encontrada")
        if fecha is not None: reserva.fecha = fecha
        if hora_inicio is not None: reserva.hora_inicio = hora_inicio
        if hora_fin is not None: reserva.hora_fin = hora_fin
        if estado is not None: reserva.estado = estado
        return self.repositorio.actualizar(reserva)


class EliminarReserva:
    def __init__(self, repositorio: RepositorioReserva):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        reserva = self.repositorio.obtener_por_id(id)
        if not reserva:
            raise ReservaNoExiste("Reserva no encontrada")
        return self.repositorio.eliminar(id)
