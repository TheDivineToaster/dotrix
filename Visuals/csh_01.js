// code is Chris Shier's https://www.csh.bz/april/05.html project. Check his stuff out!
// permission was granted to the Dotrix team for non-commercial purposes on 17APR2024

// Generated by CoffeeScript 1.6.2
(function() {
    'use strict';
    var Mouse, Square, animloop, canvas, ctx, decay, degToRad, hsla, radToDeg, rotateTo, squares;
  
    (function() {
      var i, lastTime, vendors, w, _i, _ref;
  
      w = window;
      lastTime = 0;
      vendors = ['webkit', 'moz'];
      if (!w.requestAnimationFrame) {
        for (i = _i = 0, _ref = vendors.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
          w.requestAnimationFrame = w["" + vendors[i] + "RequestAnimationFrame"];
          w.cancelAnimationFrame = w["" + vendors[i] + "CancelAnimationFrame"] || w["" + vendors[i] + "CancelRequestAnimationFrame"];
        }
      }
      if (!w.requestAnimationFrame) {
        w.requestAnimationFrame = function(callback, element) {
          var currTime, id, timeToCall;
  
          currTime = new Date().getTime();
          timeToCall = Math.max(0, 16 - (currTime - lastTime));
          id = w.setTimeout(function() {
            return callback(currTime + timeToCall);
          }, timeToCall);
          lastTime = currTime + timeToCall;
          return id;
        };
      }
      if (!w.cancelAnimationFrame) {
        return w.cancelAnimationFrame = function(id) {
          return clearTimeout(id);
        };
      }
    })();
  
    canvas = document.getElementById('canvas');
  
    ctx = canvas.getContext('2d');
  
    canvas.getWindowSize = function() {
      var d, e, g, w;
  
      w = window;
      d = document;
      e = d.documentElement;
      g = d.getElementsByTagName('body')[0];
      this.width = w.innerWidth || e.clientWidth || g.clientWidth;
      this.height = w.innerHeight || e.clientHeight || g.clientHeight;
      this.min = Math.min(this.width, this.height);
      return this.max = Math.max(this.width, this.height);
    };
  
    canvas.sizeCanvas = function(w, h) {
      if (w == null) {
        w = canvas.width;
      }
      if (h == null) {
        h = canvas.height;
      }
      this.setAttribute('width', w);
      this.setAttribute('height', h);
      this.top = -this.height / 2;
      this.left = -this.width / 2;
      this.right = this.width / 2;
      this.bottom = this.height / 2;
      ctx.restore();
      ctx.translate(w / 2, h / 2);
      return ctx.save();
    };
  
    canvas.getWindowSize();
  
    canvas.sizeCanvas(canvas.width, canvas.height);
  
    canvas.windowGotResized = function() {
      var canvasCopy, contextCopy, oh, ow;
  
      ctx.save();
      ctx.translate(-canvas.width / 2, -canvas.height / 2);
      ow = canvas.width;
      oh = canvas.height;
      canvasCopy = document.createElement('canvas');
      contextCopy = canvasCopy.getContext('2d');
      canvasCopy.setAttribute('width', ow);
      canvasCopy.setAttribute('height', oh);
      contextCopy.drawImage(canvas, 0, 0);
      canvas.getWindowSize();
      canvas.sizeCanvas(canvas.width, canvas.height);
      ctx.drawImage(canvasCopy, 0, 0, ow, oh, canvas.left, canvas.top, canvas.width, canvas.height);
      return ctx.restore();
    };
  
    window.addEventListener('resize', canvas.windowGotResized, false);
  
    window.addEventListener('orientationchange', canvas.windowGotResized, false);
  
    ctx.imageSmoothing = function(a) {
      if (a == null) {
        a = false;
      }
      ctx.webkitImageSmoothingEnabled = a;
      ctx.mozImageSmoothingEnabled = a;
      return ctx.imageSmoothingEnabled = a;
    };
  
    ctx.imageSmoothing(false);
  
    Mouse = {
      x: 0,
      y: 0,
      up: true,
      down: false,
      clicks: 0,
      events: {}
    };
  
    Mouse.events.move = function(e) {
      if ('touches' in e) {
        e.preventDefault();
        e = e.touches[0];
      }
      if (e.pageX === Mouse.x && e.pageY === Mouse.y) {
        return;
      }
      Mouse.x = e.pageX - canvas.right;
      return Mouse.y = e.pageY - canvas.bottom;
    };
  
    Mouse.events.up = function() {
      Mouse.up = true;
      return Mouse.down = !Mouse.down;
    };
  
    Mouse.events.down = function() {
      Mouse.down = true;
      Mouse.up = !Mouse.down;
      return Mouse.clicks += 1;
    };
  
    document.addEventListener('mousemove', Mouse.events.move, false);
  
    document.addEventListener('touchmove', Mouse.events.move, false);
  
    document.addEventListener('mousedown', Mouse.events.down, false);
  
    document.addEventListener('touchstart', Mouse.events.down, false);
  
    document.addEventListener('touchend', Mouse.events.up, false);
  
    document.addEventListener('mouseup', Mouse.events.up, false);
  
    ctx.drawText = function(string, x, y) {
      if (string == null) {
        string = "foo";
      }
      if (x == null) {
        x = 10;
      }
      if (y == null) {
        y = 10;
      }
      ctx.strokeWidth = 200;
      ctx.strokeStyle = "black";
      ctx.strokeText(string, x, y);
      ctx.fillStyle = "white";
      return ctx.fillText(string, x, y);
    };
  
    hsla = function(h, s, l, a) {
      if (h == null) {
        h = 0;
      }
      if (s == null) {
        s = 100;
      }
      if (l == null) {
        l = 50;
      }
      if (a == null) {
        a = 1;
      }
      return "hsla(" + h + ", " + s + "%, " + l + "%, " + a + ")";
    };
  
    Math.hyp = function(a, b) {
      if (a == null) {
        a = 0;
      }
      if (b == null) {
        b = 0;
      }
      return Math.sqrt(a * a + b * b);
    };
  
    radToDeg = function(rad) {
      return rad / (Math.PI / 180);
    };
  
    degToRad = function(deg) {
      return deg * (Math.PI / 180);
    };
  
    rotateTo = function(rise, run) {
      var rotation, slope, tangent;
  
      if (rise == null) {
        rise = 0;
      }
      if (run == null) {
        run = 0;
      }
      if (run === 0) {
        run = 1;
      }
      slope = rise / run;
      tangent = radToDeg(Math.atan(slope));
      if (run < 0) {
        rotation = degToRad(tangent - 180);
      } else {
        rotation = degToRad(tangent);
      }
      return rotation;
    };
  
    Square = (function() {
      function Square(index, x, y) {
        this.index = index;
        this.x = x;
        this.y = y;
      }
  
      Square.prototype.age = 0;
  
      Square.prototype.draw = function() {
        var h, hue, hypotenuse, i, light, rise, rotation, run, size, w, x, y;
  
        i = this.index;
        rise = this.x - Mouse.x;
        run = this.y - Mouse.y;
        hypotenuse = Math.ceil(Math.hyp(rise, run));
        size = Math.floor(canvas.max / 18);
        h = Math.sin(hypotenuse / 320 - Date.now() / 1800) * size + 1;
        w = h;
        x = -w / 2;
        y = -h / 2;
        rotation = -rotateTo(rise, run) - degToRad((Date.now() / 44) % 360);
        ctx.save();
        ctx.translate(Math.floor(this.x), Math.floor(this.y));
        ctx.rotate(rotation);
        hue = hypotenuse + radToDeg(rotation - 1);
        light = 50;
        ctx.fillStyle = hsla(hue % 359, 100, light, 0.5);
        ctx.fillRect(x, y, w, h);
        return ctx.restore();
      };
  
      return Square;
  
    })();
  
    squares = [];
  
    squares.draw = function() {
      var i, _i, _ref, _results;
  
      _results = [];
      for (i = _i = 0, _ref = squares.length; _i < _ref; i = _i += 1) {
        _results.push(squares[i].draw());
      }
      return _results;
    };
  
    squares.counter = 0;
  
    squares.make = function(x, y, limit) {
      var index, _results;
  
      if (limit == null) {
        limit = 180;
      }
      this.counter++;
      index = this.counter % limit;
      this.push(new Square(index, x, y));
      _results = [];
      while (this.length >= limit) {
        _results.push(this.shift());
      }
      return _results;
    };
  
    (squares.makeGrid = function() {
      var g, i, j, _i, _ref, _ref1, _ref2, _results;
  
      g = Math.floor(canvas.max / 16);
      _results = [];
      for (i = _i = _ref = canvas.top, _ref1 = canvas.bottom + g, _ref2 = g * 0.75; _ref2 > 0 ? _i <= _ref1 : _i >= _ref1; i = _i += _ref2) {
        _results.push((function() {
          var _j, _ref3, _ref4, _ref5, _results1;
  
          _results1 = [];
          for (j = _j = _ref3 = canvas.left, _ref4 = canvas.right + g, _ref5 = g * 0.75; _ref5 > 0 ? _j <= _ref4 : _j >= _ref4; j = _j += _ref5) {
            _results1.push(squares.make(j, i, (canvas.max * canvas.max) / g));
          }
          return _results1;
        })());
      }
      return _results;
    })();
  
    squares.refreshGrid = function() {
      squares.length = 0;
      return squares.makeGrid();
    };
  
    squares.makeGrid();
  
    window.addEventListener('resize', squares.refreshGrid, false);
  
    decay = function(hor, ver, spread, r) {
      var dh, dw, dx, dy, sh, sw, sx, sy;
  
      if (hor == null) {
        hor = 0;
      }
      if (ver == null) {
        ver = 0;
      }
      if (spread == null) {
        spread = 0;
      }
      if (r == null) {
        r = 0;
      }
      sx = canvas.left;
      sy = canvas.top;
      sw = canvas.width;
      sh = canvas.height;
      dx = sx - spread / 2;
      dy = sy - spread / 2;
      dw = sw + spread;
      dh = sh + spread;
      ctx.save();
      ctx.translate(hor, ver);
      ctx.rotate(r);
      ctx.drawImage(canvas, dx, dy, dw, dh);
      return ctx.restore();
    };
  
    decay.rotate = function(a) {
      var d, n;
  
      if (a == null) {
        a = 40;
      }
      n = Mouse.x / canvas.width - 0.5;
      d = canvas.height / (Mouse.y - canvas.height / 2) * a;
      return n / d;
    };
  
    decay.h = function(a) {
      if (a == null) {
        a = 2;
      }
      return ((Mouse.x / canvas.width) - 0.5) * a;
    };
  
    decay.v = function(a) {
      if (a == null) {
        a = 2;
      }
      return ((Mouse.y / canvas.height) - 0.5) * a;
    };
  
    decay.spread = 0;
  
    animloop = function() {
      window.requestAnimationFrame(animloop);
      ctx.imageSmoothing(true);
      ctx.clearRect(canvas.left, canvas.top, canvas.width, canvas.height);
      if (Mouse.down) {
        squares.make(Mouse.x, Mouse.y, 360);
      }
      return squares.draw();
    };
  
    animloop();
  
  }).call(this);
  
  /*
  //@ sourceMappingURL=05.map
  */
  