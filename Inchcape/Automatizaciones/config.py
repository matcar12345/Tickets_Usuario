DatosTicket = {
    "NOMBRE_SOLICITANTE": "mauricio medina ramirez",
    "IMPACTO": 4,
    "URGENCIA": "low",
    "CIUDAD_DE_IMPACTO": "Colombia",
    "CATEGORIA": "Hardware",
    "SUBCATEGORIA": "Laptop",
    "ITEMS": "Configuration",
    "SITIO": "Americas",
    "GRUPO": "Americas on Site DDC Colombia",
    "TECNICO": "",
    "TITULO_TEMA": "",
    "DESCRIPCION": "",
}

def setDatosTicket(objeto):
    for clave, valor in objeto.items():
        if(clave in DatosTicket):
            DatosTicket[clave] = valor
    from Inchcape.Automatizaciones.GenerarTicket.Generar_Ticket import GeneradorTicket
    print(DatosTicket)
    GeneradorTicket()
