var featureManager = new FeatureManager("heatmap");
var circumplexMan = new CircumplexManager("circumplex");

function loadChannels(dbId) {
    var data = {'dataset': dbId};
    d3.json('load_channels').header("Content-Type", "application/json")
        .post(JSON.stringify(data), function (error, data) {
            if (data) {
                for (var i = 0; i < data.length; i++) {
                    $("#channels").append("<option value='" + data[i]['id'] + "'>" + data[i]['label'] + "</option>");
                }
            }
    });
}

function executeProcess() {
    var data = {
        'dataset': $("#dataset").val(),
        'fselector': $("#fselector").val(),
        'classifier': $("#classifier").val(),
        'windowSize': Number($("#winSize").val()),
        'windowOverlap': Number($("#winOverlap").val()),
        'channels': $("#channels").val()
    };

    if(data['dataset'] != "" && data['classifier'] != "" && !isNaN(data["windowSize"])
        && !isNaN(data["windowOverlap"]) && data["channels"].length > 0) {
        d3.json('process_dataset').header("Content-Type", "application/json")
            .post(JSON.stringify(data), function (error, data) {
                console.log("Executing", data);
                circumplexMan.plotPoints(data['class']);
                featureManager.plotFeatures([]);
        });
    }
}
