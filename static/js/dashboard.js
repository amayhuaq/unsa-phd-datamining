/* globals Chart:false, feather:false */

(function () {
    'use strict'

    var winHeight = window.innerHeight - 120;

    $("#btnExec").click(executeProcess);

    $("#circumplex").height(Math.round(2 * winHeight / 3) + "px");
    $("#chartSignals").height(Math.round(winHeight/3) + "px");

    $('#dataset').change(function() {
        $("#signals option").remove();
        if ($(this).val() != "") {
            loadSignals($(this).val(), $("#signals"));
        }
    });
}())
