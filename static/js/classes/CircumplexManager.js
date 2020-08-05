function CircumplexManager(idDiv) {
    this.idObj = "#" + idDiv;
    this.htmlObj = $(this.idObj);
}

CircumplexManager.prototype.plotPoints = function(points) {
    $(this.idObj + " canvas").remove();

    var visSpec = {
        $schema: vegaSchema,
        description: 'Arousal - Valence model',
        height: this.htmlObj.height(),
        width: this.htmlObj.height(),
        data: {
            values: points
        },
        mark: 'circle',
        encoding: {
            x: {
                title: 'Valence',
                field: 'valence', type: 'quantitative',
                scale: {"domain": [1, 9]},
                axis: {"grid": false, "tickCount": 9}

            },
            y: {
                title: 'Arousal',
                field: 'arousal', type: 'quantitative',
                scale: {"domain": [1, 9]},
                axis: {"grid": false, "tickCount": 9}
            },
            color: {
                field: "emotion",
                type: "nominal",
                legend: {
                    title: 'Emotion'
                }
            },
            size: {aggregate: "count"}
        }
    };
    vegaEmbed(this.idObj, visSpec);
}
