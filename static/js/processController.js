var featureManager = new FeatureManager("heatmap");
var circumplexMan = new CircumplexManager("circumplex");
var vegaSchema = 'https://vega.github.io/schema/vega-lite/v4.json';

function loadSignals(data, htmlObj) {
    fetch('load_channels', {
        method: 'POST',
        body: JSON.stringify(data), // data can be `string` or {object}!
        headers:{ 'Content-Type': 'application/json' }
    }).then(res => res.json())
    .catch(error => console.error('Error:', error))
    .then(function(response) {
        if (response) {
            console.log("Response: ", response)
            sampleSize.value = response["sampleSize"];
            var channels = response["channels"];
            for (var i in channels) {
                htmlObj.append("<option value='" + channels[i]['id'] + "'>" + channels[i]['label'] + "</option>");
            }
        }
    });
}

function executeProcess(data) {
    fetch('process_dataset', {
        method: 'POST',
        body: JSON.stringify(data),
        headers:{ 'Content-Type': 'application/json' }
    }).then(res => res.json())
    .catch(error => console.error('Error:', error))
    .then(function(response) {
        console.log("Executing", response);
        circumplexMan.plotPoints(response['class']);
        featureManager.plotFeatures(response['features']);
    });
}
