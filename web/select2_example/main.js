//1: Se definen los parametros de configuración del select
var settings = {
    placeholder: "Selecciona un elemento del catálogo",
    allowClear: false,
    language: 'es',
    //Define el número mínimo de carácteres que requiere escribir el usuario para iniciar la búsqueda
    minimumInputLength: 4,
    //Se definirá más adelante
    ajax: undefined,
};

//2: Se definen la llamada ajax que se encarga de hacer la petición de los datos del catálogo. Para este ejemplo se cuenta con un JSON que simula el resultado de una petición REST
//2.1 Función data_func, se encarga de enviar a la petición ajax con los parámetros de búsqueda. Cuando la cadena llega ser mayor al tamaño definido en minimumInputLength, se envía la petición.
var data_func = function(params) {
    return { search: params.term };
};
//2.2 Función processResults_func, se encarga de procesar los resultados obtenidos de la petición. 
//El formato de un registro es: { "id": 1, "id_inm2022": "01INM_00003", "id_inm2019": "01INM_394", "id_cct": "01DES0002N", "domicilio": "CALLE EDMUNDO GAMEZ OROZCO, NUM EXT 118", "cve_mun": "01001", "cve_loc": "010010239", "nom_loc": "GENERAL JOSÉ MARÍA", "latitud": "22.0002780000000016", "longitud": "-102.202777999999995", "cp": "20320", "id_domicilio": null, "cve_facilitador": null, "facilitador": null, "fecha_captura": null, "hora_captura": null, "num_inmueble": null, "foto_escuela": null, "notas": null, "created_at": null, "updated_at": null, "deleted_at": null }
//Solo se mapeara en el id con el domicilio

var processResults_func = function(response) {
    return { results: response.map((s) => ({id: s.id, text: s.domicilio})) };
};

//2.3 Construcción de la llamada ajax
var ajax_call = {
    //Define el end point
    url: "data/domicilio.json",
    //Define el metodo de petición
    type: "get",
    //Formato de entraada
    dataType: "json",
    delay: 150,
    data: data_func,
    processResults: processResults_func
}

//2.4 Agregamos estas funciones a nuestro settings para el campo ajax
settings.ajax = ajax_call;

//3: Se define un evento('select2:select') que permite ejecutarse cuando un elemento es seleccionado.
var on_selected = function(params) {
    console.log(params);
};

//4: Se recomienda que el select se defina en el evento ready del documento cargado. El id del select es select_test_id
//En la versión 3.6 de Jquery $(function() {}) es equivalente a $(document).ready(function() {});
$(document).ready(function() {
    $("#select_test_id").select2(settings).on(on_selected);
});