
let Ul = "_pxhd"; 


// get _pxhd value from cookie
function yt(n) {
    var t = void 0;
    if (n && "string" == typeof n)
        try {
            var e = "; " + document.cookie
              , r = e.split("; " + n + "=");
            2 === r.length && (t = r.pop().split(";").shift())
        } catch (n) {}
    return t
}

function Zr() {
    return rs || (rs = yt(Ul)),
    rs
}