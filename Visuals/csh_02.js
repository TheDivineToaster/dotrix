// code is Chris Shier's https://www.csh.bz/line/05xp.html project. Check his stuff out!
// permission was granted to the Dotrix team for non-commercial purposes on 17APR2024

/**
 * User: chris
 * Date: 02/10/12
 * Time: 9:53 AM
 */
// todo: tool switching, path recording

var ctx = document.getElementById('canvas').getContext('2d'),
  Mouse = window.Mouse,
  cw = window.cw,
  ch = window.ch,
  cMin = window.cMin,
  cMax = window.cMax,
  time = 0;

function imageSmoothing(a) {
  ctx.imageSmoothingEnabled = a;
  ctx.mozImageSmoothingEnabled = a;
  ctx.webkitImageSmoothingEnabled = a;
}

window.requestAnimFrame = (function () {
  return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function (callback, element) {
      window.setTimeout(callback, 1000 / 60);
    };
})();

function timer() {
  time += 1;
}

function hsla(h, s, l, a) {
  var hue = h === undefined ? 1 : h,
    sat = s === undefined ? 1 : s,
    light = l === undefined ? 1 : l,
    alpha = a === undefined ? 1 : a;
  return "hsla" + "(" + hue + ", " + sat + "%, " + light + "%, " + alpha + ")";
}

function hypotenuse(a, b) {
  return Math.sqrt((a * a) + (b * b || a * a)) / 2;
};

function simple_moving_averager(period) {
  //http://rosettacode.org/wiki/Averages/Simple_moving_average#JavaScript
  var nums = [];
  return function(num) {
      nums.push(num);
      if (nums.length > period)
          nums.splice(0,1);  // remove the first element of the array
      var sum = 0;
      for (var i in nums)
          sum += nums[i];
      var n = period;
      if (nums.length < period)
          n = nums.length;
      return(sum/n);
  }
}

function clear(){
  ctx.clearRect(0,0,cw,ch);
}

function clearCanvas(a) {
  ctx.fillStyle = hsla(0, 0, 0, a);
  ctx.fillRect(0, 0, cw, ch);
}
clearCanvas(1);

function drawText(text, x, y) {
  ctx.lineWidth = 2;
  ctx.fillStyle = "white";
  ctx.strokeStyle = "black";
  ctx.strokeText(text, x, y );
  ctx.fillText(text, x, y);
}

function pointer() {
  var size = 20,
    a = Mouse.x - Mouse.xA[1],
    b = Mouse.y - Mouse.yA[1],
    hue = Math.abs(hypotenuse(a, b)) * 4 + 240;
  ctx.save();
  ctx.translate(Mouse.xA[2], Mouse.yA[2]);
  ctx.fillStyle = hsla(hue, 100, 50, 1);
  ctx.fillRect(-size / 2, -size / 2, size, size);
  ctx.restore();
}

var aRandomNumber = Math.random() * 360 + 1;
function line(width) {
  ctx.lineWidth = width||2;
  ctx.beginPath();
  ctx.moveTo(Mouse.path.x[1], Mouse.path.y[1]);
  for ( var i = 0; i < 64; i++) {
    ctx.lineTo(Mouse.xA[i-1],Mouse.yA[i-1]);
    ctx.lineTo(Mouse.xA[i],Mouse.yA[i]);
    var a = (Mouse.xA[i] - Mouse.xA[i-1])||1,
      b = (Mouse.yA[i] - Mouse.yA[i-1])||1,
      hue = Math.abs( Math.ceil(hypotenuse(a,b)) ) * 8 + 240;
      ctx.strokeStyle = hsla(hue + (time/2) - (i*4),100,50,1);
    ctx.stroke();
    ctx.beginPath();
  }
  ctx.stroke();
}

function lineb(width) {
  ctx.lineWidth = width||2;
  ctx.beginPath();
  for ( var i = 0; i < 64; i++) {
    ctx.moveTo(Mouse.xA[i-1],Mouse.yA[i-1]);
    ctx.lineTo(Mouse.xA[i],Mouse.yA[i]);
      var hue;
      if (i >= 32 ){
        hue = time/32 + (Mouse.clicks*90);
      } else {
        hue = time/32 + (Mouse.clicks*90) + 240;
      }
      var light;
      if (i % 32 < 16){
        light = 100;
      } else {
        light = 0;
      }
      var a = (Mouse.xA[i] - Mouse.xA[i-1])||1,
        b =( Mouse.yA[i] - Mouse.yA[i-1])||1;
      ctx.strokeStyle = hsla(0,100,light,1);
    ctx.stroke();
    ctx.beginPath();
  }
  ctx.stroke();
}

function linec(width) {
  ctx.lineWidth = width||2;
  ctx.beginPath();
  for ( var i = 0; i < 64; i++) {
    ctx.moveTo(Mouse.xA[i-1],Mouse.yA[i-1]);
    ctx.lineTo(Mouse.xA[i],Mouse.yA[i]);
      var hue;
      if (i >= 32 ){
        hue = time/32 + (Mouse.clicks*90);
      } else {
        hue = time/32 + (Mouse.clicks*90) + 240;
      }
      var light;
      if (i % 32 < 16){
        light = 50;
      } else {
        light = 0;
      }
      var a = (Mouse.xA[i] - Mouse.xA[i-1])||1,
        b = (Mouse.yA[i] - Mouse.yA[i-1])||1;
      ctx.strokeStyle = hsla(hue + hypotenuse(a,b)*4 ,100,light,1);
    ctx.stroke();
    ctx.beginPath();
  }
  ctx.stroke();
}

function decay(hor,ver, spread, rotate) {
  var h = hor,
    v = ver,
    s = spread||2;
  ctx.save();
  ctx.translate(h,v);
  ctx.rotate(rotate||0);
  ctx.drawImage(canvas, -s/2, -s/2, cw + s, ch + s);
  ctx.restore();
}

function decay2(hor,ver, spread, rotate){
    var h = hor,
    v = ver,
    s = spread||2;
  ctx.save();
  ctx.translate(cw/2 + h,ch/2 + v);
  ctx.rotate(rotate||0);
  ctx.drawImage(canvas, -s/2 - cw/2, -s/2 - ch/2, cw + s, ch + s);
  ctx.restore();
}

function decayR(rotate) {
  ctx.save();
  ctx.translate(cw/2, ch/2);
  ctx.rotate(rotate||0);
  ctx.drawImage(canvas, -cw/2, -ch/2, cw, ch);
  ctx.restore();
}

//EDIT THIS ONE DUMMY
function decay3(hor,ver, spread, rotate){
    var h = hor,
    v = ver,
    s = spread||2,
    cDif = cMax-cMin;
  ctx.save();
  ctx.translate( -cDif/2, -cDif/2 )//cw-cMax, ch-cMax
  ctx.drawImage(canvas, 0,0, cw+cDif, ch+cDif)
  // clearCanvas(1);
  // ctx.drawImage(canvas, 0,0, cw-cDif, ch-cDif)
  // ctx.drawImage(canvas, 0,0, cw-cDif, ch-cDif)
  ctx.restore();
  drawText(cDif)
}

function grid(interval, color){
  ctx.fillStyle = color||"black";
  for (i = 0; i <= cw; i+= interval){
    for (j = 0; j <= ch; j += interval){
      ctx.fillRect(i, j, interval/2, interval/2);
    }
  }
}

function dots(){
  var hAdj = (Math.random()-0.5) * (Mouse.xA[0] - Mouse.xA[100]),
    vAdj = (Math.random()-0.5)*10;
  ctx.strokeStyle =  hsla(time, 100, 50, 1);
  ctx.fillStyle = hsla(time + 180, 100, 50, 1);
  ctx.beginPath();
  ctx.arc(Mouse.x + hAdj ,Mouse.y + vAdj  ,5,0, Math.PI*2, true)
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}

function ray(){
  // var h = Mouse.x - Mouse.xA[0] ,
  //   v = Mouse.y - Mouse.yA[0];

    var a, b, c;
      a = {x: Mouse.xA[0], y: Mouse.yA[0] },
      b = {x: Mouse.x, y: Mouse.y},
      c = {
        x: 2 * Mouse.x - Mouse.xA[0],
        y: 2 * Mouse.y - Mouse.yA[0],
      } ;
      a.h = hypotenuse(a.x - b.x, a.y - b.y);
      b.h = hypotenuse(a.x - c.x, a.y - c.y);
      c.h = hypotenuse((c.x - b.x)||1, (c.y - b.y)||1);

  var size = (a.h/1.5) + 5,
    xPosition = a.x + a.h / 2 - c.h,
    yPosition = a.y + a.h / 2 - c.h;
   var a = Mouse.x - Mouse.xA[0],
      b = Mouse.y - Mouse.yA[0],
      hue = c.h * 1.5 + 240 + time/2;

  ctx.strokeStyle = hsla(0, 0, 0, 1);
  ctx.fillStyle = hsla(hue + aRandomNumber , 100, 50, 1)
  ctx.beginPath();
  ctx.arc(xPosition , yPosition, size , 0 , Math.PI*2 );
  ctx.closePath();
  ctx.fill();
}

var fps = {
 past : [0],
 capture : function(){
    var i = 0;
    while (this.past.length < cw) {
      i++;
      this.past.unshift(Date.now());
      this.past[i] = 1000/(this.past[i-1] - this.past[i]);
   }
   this.past.pop();
  },
  sma30 : simple_moving_averager(30),
  sma60 : simple_moving_averager(60),
  sma120 : simple_moving_averager(120),
  show : function (){
    this.capture();
    var i = 0,
      count = 80;
      ctx.fillStyle = hsla(0, 0, 0, 0.5);
      ctx.fillRect(cw-count,0,count,41);
    while (i < count){
      var n = fps.past[i];
      ctx.fillStyle = hsla(n * 6 + 180, 100, 40, 0.8);
      ctx.fillRect(-i + fps.past.length, 40, 1 , -n/3)
      ctx.fillStyle = hsla(this.sma30(n)*6 + 180, 100, 50, 1);
      ctx.fillRect(-i + fps.past.length +6 , 40 - this.sma30(n)/3, 1, 2)
      i++ ;
    }
    drawText(Math.round(this.sma60(fps.past[10])),cw-15, 10)
  }
}
window.fps = fps


window.requestSmoothMouse = (function () {
    //http://code.google.com/p/chromium/issues/detail?id=5598
    // ios
      return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (callback,  element) {
          window.setTimeout(callback, 1000 / 60);
        };
    })();
    
    
    
    var pos = [],
      Mouse = window.Mouse;
    
    Mouse = {
      x: -1, 
      y: -1, 
      xA: [cw / 2], 
      yA: [ch / 2], 
      xDown: -1, 
      xUp: -1, 
      yDown: -1,
      yUp: -1,
      up: true, 
      clicks: 0
    };
    
    Mouse.events = {};
    Mouse.events.move = function (e) {
      // ios
      if ("touches" in e) e = e.touches[0];
      if (e.pageX === Mouse.x && e.pageY === Mouse.y) { return; }
      Mouse.x = e.pageX;
      Mouse.y = e.pageY;
    };
    
    Mouse.path = [];
    Mouse.path.x = [];
    Mouse.path.y = [];
    Mouse.path.capture = function (x, y) {
      Mouse.path.x.unshift([x]);
      Mouse.path.y.unshift([y]);
      while (Mouse.path.x.length > 32) {
        Mouse.path.x.pop();
        Mouse.path.y.pop();
      }
    };
    Mouse.avg = function (a, followSpeed, x, y) {
    
      //if (!Array.isArray(pos[a])) {pos[a] = [Mouse.x, Mouse.y]; }
      if(!Array.isArray(pos[a])) pos[a] = [Mouse.x,Mouse.y];
      
      if (x > pos[a][0]) {
        pos[a][0] += (x - pos[a][0]) / followSpeed;
      } else if (x < pos[a][0]) {
        pos[a][0] -= (pos[a][0] - x) / followSpeed;
      } else {
        pos[a][0] += 0;
      }
      if (y > pos[a][1]) {
        pos[a][1] += (y - pos[a][1]) / followSpeed;
      } else if (y < pos[a][1]) {
        pos[a][1] -= (pos[a][1] - y) / followSpeed;
      } else {
        pos[a][1] += 0;
      }
      Mouse.xA[a] = Math.round(pos[a][0]);
      Mouse.yA[a] = Math.round(pos[a][1]);
    };
    
    Mouse.events.up = function (e) {
      Mouse.down = false;
      Mouse.up = true;
      Mouse.xUp = Mouse.x;
      Mouse.yUp = Mouse.y;
    };
    
    Mouse.events.down = function (e) {
      if ("touches" in e) {
        e.preventDefault();
        e = e.touches[0];
      }
      Mouse.down = true;
      Mouse.up = false;
      Mouse.clicks += 1;
      Mouse.xDown = Mouse.x;
      Mouse.yDown = Mouse.y  
      Mouse.xUp = Mouse.x;
      Mouse.yUp = Mouse.y;
    };
    
    function smoothMouse() {
      if (Mouse.x !== -1 && Mouse.y !== -1) 
      {  Mouse.avg(0, 2, Mouse.x, Mouse.y);
        for (var i = 1; i <= 64; i++) {
          Mouse.avg(i, 2, Mouse.xA[i - 1], Mouse.yA[i - 1]);
        }
        Mouse.path.capture(Mouse.xA[0], Mouse.yA[0]);}
      window.Mouse = Mouse;
      window.requestSmoothMouse(smoothMouse);
    }
    smoothMouse();
    
    document.addEventListener("mousemove", Mouse.events.move);
    
    document.addEventListener("touchmove", Mouse.events.move);
    document.addEventListener("mousedown", Mouse.events.down);
    
    document.addEventListener("touchstart", Mouse.events.down);
    document.addEventListener("touchend", Mouse.events.up);
    document.addEventListener("mouseup", Mouse.events.up);
    

    
/**
 * Author: tim baker http://bon.gs
 */
//var cw = window.cw,
//  ch = window.ch,
//  cMin = window.cMin,
//  cMax = window.cMax,
//  canvas = window.canvas,
//  ctx = window.ctx;

//var canvas, ctx, cw, ch, cMin, cMax;

function getWindowSize() {

    var w = window,
      d = document,
      e = d.documentElement,
      g = d.getElementsByTagName('body')[0];
  
    cw = w.innerWidth || e.clientWidth || g.clientWidth;
    ch = w.innerHeight || e.clientHeight || g.clientHeight;
    cMin = Math.min(cw, ch);
    cMax = Math.max(cw, ch);
  }
  
  getWindowSize();
  function sizeCanvas(w, h) {
    canvas = document.getElementById('canvas');
    canvas.setAttribute("height", h);
    canvas.setAttribute("width", w);
  }
  sizeCanvas(cw, ch);
  
  function sizeContext(w, h) {
    ctx = document.getElementById('canvas').getContext('2d');
  }
  sizeContext(cw, ch);
  
  function windowGotResized() {
    var canvasCopy = document.createElement("canvas"),
      ow = cw,
      oh = ch,
      contextCopy = canvasCopy.getContext('2d');
    canvasCopy.setAttribute("width", ow);
    canvasCopy.setAttribute("height", oh);
    contextCopy.drawImage(canvas, 0, 0);
  
    //resize canvas
    getWindowSize();
    sizeCanvas(cw, ch);
  
    //paste copied canvas onto resized canvas
    ctx.drawImage(canvasCopy, 0, 0, ow, oh, 0, 0, cw, ch);
    sizeContext(cw, ch);
  
  }
  
  function reloadWindow() {
    window.location = window.location;
  }
  
  window.onresize = windowGotResized;
  
  window.top.scrollTo(0, 1);