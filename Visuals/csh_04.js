// code is Chris Shier's https://www.csh.bz/line/03.html project. Check his stuff out!
// permission was granted to the Dotrix team for non-commercial purposes on 17APR2024

var getWindowSize = function(){
    var w=window,
        d=document,
        e=d.documentElement,
        g=d.getElementsByTagName('body')[0];
  
    cw = w.innerWidth||e.clientWidth||g.clientWidth;
    ch = w.innerHeight||e.clientHeight||g.clientHeight;
  
    cMin = Math.min(cw, ch);
    cMax = Math.max(cw, ch);
  }
  getWindowSize();
  
  var sizeCanvas = function(w, h){
    canvas = document.getElementById('canvas');
    canvas.setAttribute("height", h);
    canvas.setAttribute("width", w);
  }
  sizeCanvas(cw, ch);
  
  var sizeContext = function(w, h){
    ctx = document.getElementById('canvas').getContext('2d');
  }
  sizeContext(cw, ch);
  
  function windowGotResized(){
    //thank you to tim baker http://bon.gs/ for this code
    //copy canvas
    var canvasCopy = document.createElement("canvas"),
        ow = cw,
        oh = ch;
    canvasCopy.setAttribute("width", ow);
    canvasCopy.setAttribute("height", oh);
    var contextCopy = canvasCopy.getContext('2d');
    contextCopy.drawImage(canvas, 0, 0);
  
    //resize canvas
    getWindowSize();
    sizeCanvas(cw, ch);
  
    //paste copied canvas onto resized canvas
    ctx.drawImage(canvasCopy, 0, 0, ow, oh, 0, 0, cw, ch);
    sizeContext(cw, ch);
  }
  
  function reloadWindow(){window.location = window.location;}
  
  window.onresize = windowGotResized;
  
  window.top.scrollTo(0, 1);

