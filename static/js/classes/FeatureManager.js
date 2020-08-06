function FeatureManager(idDiv) {
    this.idObj = "#" + idDiv;
    this.htmlObj = $(this.idObj);
}

FeatureManager.prototype.formatData = function(features) {
    var tmp, data = [];
    for (var i=0; i < features['feat_names'].length; i++) {
        for (var j=0; j < features['emo_names'].length; j++) {
            tmp = features['feat_names'][i].split("_");
            data.push({
                'feature': features['feat_names'][i],
                'emotion': features['emo_names'][j]['name'],
                'value': features['fcs'][i][j],
                'emotion_desc': features['emo_names'][j]['desc'],
                'signal': tmp[0],
                'channel': tmp[1]
            });
        }
    }
    return data;
}

FeatureManager.prototype.plotFeatures = function(features) {
    $(this.idObj + " canvas").remove();
    var data = this.formatData(features);
    console.log("FCS: ", data);

    // change of visualization by channel when quantity features is greater than 60
    var encodY = {
        title: null,
        field: "feature",
        type: "nominal",
        axis: {
            orient: "right"
        }
    };
    if(features["fcs"].length > 60) {
        encodY['field'] = "channel"
    }

    var visSpec = {
        $schema: vegaSchema,
        height: this.htmlObj.height() - 100,
        width: this.htmlObj.width() - 60,
        data: {
            values: data
        },
        "config": {
          "view": {
              "strokeWidth": 0,
              "step": 13
          },
          "axis": {
              "domain": false
          }
        },
        mark: {"type": "rect", "tooltip": {"content": "data"}},
        encoding: {
            x: {
                title: null,
                field: "emotion",
                type: "nominal"
            },
            y: encodY,
            color: {
                field: "value",
                aggregate: "mean",
                type: "quantitative",
                scale: {"range": "diverging", "domain": [-1,1]},
                legend: {
                    title: null,
                    direction: "horizontal",
                    orient: "bottom"
                }
            }
        }
    }
    vegaEmbed(this.idObj, visSpec);
}