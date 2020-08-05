(function () {
    'use strict'

    var winHeight = window.innerHeight - 120;
    $("#circumplex").height(winHeight + "px");
    //$("#circumplex").height(Math.round(2 * winHeight / 3) + "px");
    //$("#chartSignals").height(Math.round(winHeight/3) + "px");

    $('#dataset').change(function() {
        $("#channels option").remove();
        if ($(this).val() != "") {
            var data = {'dataset': $(this).val()};
            loadSignals(data, $("#channels"));
        }
    });

    $("#btnExec").click(function() {
        var data = {
            'dataset': $("#dataset").val(),
            'fselector': $("#fselector").val(),
            'classifier': $("#classifier").val(),
            'nClasses': Number($("#nClasses").val()),
            'winSize': Number($("#winSize").val()),
            'winIni': Number($("#winIni").val()),
            'sampleSize': Number($("#sampleSize").val()),
            'channels': $("#channels").val(),
            'testSize': Number($("#testSize").val()),
            'mode': $("#mode").val()
        };
        if(data['dataset'] != "" && data['classifier'] != "" && !isNaN(data["winSize"]) && data["channels"].length > 0) {
            executeProcess(data);
        }
        else
            console.log("Some parameters is needed.")
    });
}())
