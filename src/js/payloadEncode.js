
 var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

 function InvalidCharacterError(message) {
   this.message = message;
 }
 InvalidCharacterError.prototype = new Error ();
 InvalidCharacterError.prototype.name = 'InvalidCharacterError';

 // encoder
 // [https://gist.github.com/999166] by [https://github.com/nignag]
 function btoa(input) {
   var str = String (input);
   for (
     // initialize result and counter
     var block, charCode, idx = 0, map = chars, output = '';
     // if the next str index does not exist:
     //   change the mapping table to "="
     //   check if d has no fractional digits
     str.charAt (idx | 0) || (map = '=', idx % 1);
     // "8 - idx % 1 * 8" generates the sequence 2, 4, 6, 8
     output += map.charAt (63 & block >> 8 - idx % 1 * 8)
   ) {
     charCode = str.charCodeAt (idx += 3 / 4);
     if (charCode > 0xFF) {
       throw new InvalidCharacterError ("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range.");
     }
     block = block << 8 | charCode;
   }
   return output;
 }

let VA = 50;

function ft(n, t) {
    for (var e = "", r = 0; r < n.length; r++)
        e += String.fromCharCode(t ^ n.charCodeAt(r));
    return e
}

var t = function() {
    var n = window.unescape || window.decodeURI;
    return {
        v: function(t) {
            var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
              , r = void 0
              , o = void 0
              , i = void 0
              , a = void 0
              , u = void 0
              , c = void 0
              , A = void 0
              , f = void 0
              , l = 0
              , s = 0
              , d = [];
            if (!t)
                return t;
            try {
                t = n(encodeURIComponent(t))
            } catch (n) {
                return t
            }
            do {
                r = t.charCodeAt(l++),
                o = t.charCodeAt(l++),
                i = t.charCodeAt(l++),
                f = r << 16 | o << 8 | i,
                a = f >> 18 & 63,
                u = f >> 12 & 63,
                c = f >> 6 & 63,
                A = 63 & f,
                d[s++] = e.charAt(a) + e.charAt(u) + e.charAt(c) + e.charAt(A)
            } while (l < t.length);var v = d.join("")
              , h = t.length % 3;
            return (h ? v.slice(0, h - 3) : v) + "===".slice(h || 3)
        }
    }
}

function aA(n){return btoa(encodeURIComponent(n).replace(/%([0-9A-F]{2})/g,function(n,t){return String.fromCharCode("0x"+t)}))}

function encodePayload(payload) {
    return aA(ft(payload, VA));
}