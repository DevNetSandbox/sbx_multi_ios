var devices = $('#device-datatable').DataTable( {
    "ajax": {
            "type" : "GET",
            "url" : "/api/device",
            "dataSrc": function ( json ) {
                return json;
            }
            },

    "columns": [
                    { "data": "hostname" },
                    { "data": "model" },
                    { "data": "version"},
                    { "data": "ip_address"}
                ]
    }
);


// auto refresh the datatable
setInterval( function () {
    devices.ajax.reload();
}, 10000 );
