
    var topologyData = {}

    function getAjax(url, success) {
        var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        xhr.open('GET', url);
        xhr.onreadystatechange = function() {
            if (xhr.readyState>3 && xhr.status==200) success(xhr.responseText);
        };
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.send();
        return xhr;
    }

    getAjax('/api/topology', function(data){
            var json = JSON.parse(data);
            topologyData = json
            buildTopology(nx)
            }
            );

    function buildTopology (nx) {
        /**
         * define application
         */
        var Shell = nx.define(nx.ui.Application, {
            methods: {

                start: function () {
                    //your application main entry

                    // initialize a topology
                    var topo = new nx.graphic.Topology({
                        // set the topology view's with and height
                        width: 800,
                        height: 800,
                        // node config
                        nodeConfig: {
                            // label display name from of node's model, could change to 'model.id' to show id
                            label: 'model.name',
                            "iconType": "switch"
                        },
                        // link config
                        linkConfig: {
                            // multiple link type is curve, could change to 'parallel' to use parallel link
                            linkType: 'curve'
                        },
                        // show node's icon, could change to false to show dot
                        showIcon: true,
                        identityKey: 'id'
                    });

                    //set data to topology
                    topo.data(topologyData);
                    topo.attach(this)
                    // attach topology to document
                    // topo.attach(document.getElementById('topology'));
                },
                getContainer: function () {
                    return new nx.dom.Element(document.getElementById('topology'))
                }

            }
        });
        /**
     * create application instance
     */
    var shell = new Shell();

    /**
     * invoke start method
     */
    shell.start();
    }
