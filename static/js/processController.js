var featureManager = new FeatureManager("heatmap");
var circumplexMan = new CircumplexManager("circumplex");

function loadSignals(dbId, htmlObj) {
    var data = {'dataset': dbId};
    d3.json('load_signals').header("Content-Type", "application/json")
        .post(JSON.stringify(data), function (error, data) {
            if (data) {
                for (var signal in data) {
                    htmlObj.append("<option value='" + signal + "'>" + signal + "</option>");
                }
            }
    });
}

function executeProcess() {
    var data = {
        'dataset': $("#dataset").val(),
        //'fselector': $("#fselector").val(),
        'classifier': $("#classifier").val(),
        'winSize': Number($("#winSize").val()),
        'winIni': 0,
        'sampleSize': 128,
        'signals': $("#signals").val()
    };

    if(data['dataset'] != "" && data['classifier'] != "" && !isNaN(data["winSize"])
        && data["signals"].length > 0) {
        d3.json('process_dataset').header("Content-Type", "application/json")
            .post(JSON.stringify(data), function (error, data) {
                console.log("Executing", data);
                circumplexMan.plotPoints(data['class']);
                featureManager.plotFeatures(data['features']);
        });
    }
    else
        console.log("Some parameters is needed.")
}
