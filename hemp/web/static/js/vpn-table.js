var devices = $('#device-datatable').DataTable( {
    "ajax": {
            "type" : "GET",
            "url" : "/api/vpn",
            "dataSrc": function ( json ) {
                return json;
            }
            },

    "columns": [
                    { "data": "partner_name",
                     "render": function (data, type, row, meta) {
                        partner = row.partner_name
                        var url = '<a href="/vpn/' + partner + '">' + partner + '</a>'
                          return url
                    }
                },
                    { "data": "peer_ip" },
                    { "data": "transform_encryption"},
                    { "data": "transform_auth"},
                    { "data": "sequence"},
                ]
    }
);


// auto refresh the datatable
setInterval( function () {
    devices.ajax.reload();
}, 10000 );
