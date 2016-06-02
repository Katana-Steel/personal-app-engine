
var forms = new Object();

function menu_toggle(prefix)
{
    var m = document.getElementById('menu');
    var r = m.rows;
    prefix += '_'; 
    var pl = prefix.length
    for (var i =0;i<r.length;i++) {
        var ele = r[i];
        var n = ele.id;
        if(n.substr(0,pl) == prefix) {
            for(var j=0; j<ele.cells.length;j++) {
                if(ele.cells[j].style.display != "table-cell")
                    ele.cells[j].style.display="table-cell";
                else
                    ele.cells[j].style.display="none";
            }
        }
    }
}

function add_form(frm, page, method)
{
    var f;
    if(forms[frm]) {
        f = forms[frm];
    } else {
        f = new sack();
    }

    f.requestFile = page;
    if(typeof method == "undefined")
        f.method = "POST";
    else
        f.method = method;
    forms[frm] = f;
}

function frm_filled(frm)
{
    var form = document.getElementById(frm);
    var input = form.getElementsByTagName("input");
    for (var i=0;i<input.length;i++) {
        var n = input[i];
        if((n.type == "text" || n.type == "password") && n.value == "") {
            n.focus();
            return false;
        }
    }
    var select = form.getElementsByTagName("select");
    for (var i = 0; i < select.length; i++) {
        var n = select[i];
        if (n.value == "") {
            n.focus();
            return false;
        }
    }
    return true;
}

function submit_form(divId, frm)
{
    var f = forms[frm]
    if(f == null) return;
    if(!frm_filled(frm)) return;

    var form = document.getElementById(frm);
    var input = form.getElementsByTagName("input");
    for (var i=0;i<input.length;i++) {
        var n = input[i];
        if(n.type == "text" || n.type == "password" || n.type == "hidden")
            f.encVar(n.name, n.value);
    }
    var select = form.getElementsByTagName("select");
    for (var i = 0; i < select.length; i++) {
        var n = select[i];
        f.encVar(n.name, n.value);
    }
    f.onCompletion = function () { ajax_showContent(divId, idx); };
    var idx = dynamicContent_ajaxObjects.length;
    dynamicContent_ajaxObjects[idx] = f;
    f.runAJAX();
    forms[frm] = false;
}

function keypress(event, divId, frm)
{
    var keynum
    if(window.event) // IE
	{
        keynum = event.keyCode;
	}
    else if(event.which) // Netscape/Firefox/Opera
	{
        keynum = event.which;
	}

	if(keynum == 13) {
        if(!frm_filled(frm)) return false;
        submit_form(divId, frm);
    }
    return true;
}
