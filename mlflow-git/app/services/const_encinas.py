## Constantes para los parametros disponibles a consultar a SINCA en la estación Las Encinas
diario = "diario.diario.ic"
horario = "horario.horario.ic"
mensual = "diario.mensual.ic"

## Periodo de la consulta (mensual, diario u horario)
periodo = horario

contaminacion = {

    # Dióxido de azufre
    'di_azufre' : ("./RIX/901/Cal/0001//0001." + periodo),

    # Monóxido de nitrógeno
    'mon_nitrogeno' : ("./RIX/901/Cal/0002//0002." + periodo),

    # Dióxido de nitrógeno
    'di_nitrogeno' : ("./RIX/901/Cal/0003//0003." + periodo),

    # Monóxido de carbono
    'mon_carbono' : ("./RIX/901/Cal/0004//0004." + periodo),

    # Ozono
    'ozono' : ("./RIX/901/Cal/0008//0008." + periodo),

    # Oxidos de nitrogeno
    'ox_nitrogeno' : ("./RIX/901/Cal/0NOX//0NOX." + periodo),

    # Material particulado PM10
    'pm10' : ("./RIX/901/Cal/PM10//PM10." + periodo),

    # Material particulado PM2.5
    'pm25' : ("./RIX/901/Cal/PM25//PM25." + periodo),

}
    # >>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
meteorologico = {
    # Radiación global
    'rad_global' : ("./RIX/901/Met/GLOB//horario_003.ic"),

    # Presión atmosferica
    'presion_atm' : ("./RIX/901/Met/PRES//horario_003.ic"),

    # Precipitaciones
    'precipitaciones' : ("./RIX/901/Met/RAIN//horario_004.ic"),

    # Humedad relativa del aire
    'humedad' : ("./RIX/901/Met/RHUM//horario_003.ic"),

    'temperatura' : ("./RIX/901/Met/TEMP//horario_010.ic"),

    # Dirección del viento
    'dir_viento' : ("./RIX/901/Met/WDIR//horario_010_spec.ic"),

    # Velocidad del viento
    'vel_viento' : ("./RIX/901/Met/WSPD//horario_010.ic"),

}