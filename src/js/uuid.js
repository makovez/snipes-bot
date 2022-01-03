
MA = void 0;
        try {
            "undefined" != typeof crypto && crypto && crypto.getRandomValues && function() {
                var n = new Uint8Array(16);
                (MA = function() {
                    return crypto.getRandomValues(n),
                    n
                }
                )()
            }()
        } catch (n) {
            MA = void 0
        }
        MA || function() {
            var n = new Array(16);
            MA = function() {
                for (var t, e = 0; e < 16; e++)
                    0 == (3 & e) && (t = 4294967296 * Math.random()),
                    n[e] = t >>> ((3 & e) << 3) & 255;
                return n
            }
        }();

var HA = MA()
, PA = [1 | HA[0], HA[1], HA[2], HA[3], HA[4], HA[5]]
, YA = 16383 & (HA[6] << 8 | HA[7]), l = YA, UA = 0, d = UA, NA = 0, n = "c"

for (var _A = [], RA = {}, CA = 0; CA < 256; CA++)
            _A[CA] = (CA + 256).toString(16).substr(1),
            RA[_A[CA]] = CA;

function w() {
    return +new Date
}

function dt(n, t) {
    var e = t || 0
      , r = _A;
    return r[n[e++]] + r[n[e++]] + r[n[e++]] + r[n[e++]] + "-" + r[n[e++]] + r[n[e++]] + "-" + r[n[e++]] + r[n[e++]] + "-" + r[n[e++]] + r[n[e++]] + "-" + r[n[e++]] + r[n[e++]] + r[n[e++]] + r[n[e++]] + r[n[e++]] + r[n[e++]]
}

function vt(n, t, r, o) {
    //var i = e;
    //k(i("AAJjX3I"));
    NA = w()
    var a = "";
    var A = t && r || 0
      , f = t || [];
    n = n || {};
    var l = void 0 !== n.clockseq ? n.clockseq : YA
      , s = void 0 !== n.msecs ? n.msecs : w()
      , d = void 0 !== n.nsecs ? n.nsecs : UA + 1
      , v = s - NA + (d - UA) / 1e4;
    if (v < 0 && void 0 === n.clockseq && (l = l + 1 & 16383),
    (v < 0 || s > NA) && void 0 === n.nsecs && (d = 0),
    d >= 1e4)
        throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
    NA = s,
    UA = d,
    YA = l,
    s += 122192928e5;
    var h = (1e4 * (268435455 & s) + d) % 4294967296;
    f[A++] = h >>> 24 & 255,
    f[A++] = h >>> 16 & 255,
    f[A++] = h >>> 8 & 255,
    f[A++] = 255 & h;
    var p = s / 4294967296 * 1e4 & 268435455;
    f[A++] = p >>> 8 & 255,
    f[A++] = 255 & p,
    f[A++] = p >>> 24 & 15 | 16,
    f[A++] = p >>> 16 & 255,
    f[A++] = l >>> 8 | 128,
    f[A++] = 255 & l;
    for (var m = n.node || PA, g = 0; g < 6; g++)
        f[A + g] = m[g];
    var y = t || dt(f);
    return a === y ? a : (NaN,
    y)
}