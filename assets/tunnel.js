// Туннель кадров на WebGL2 — как в hero у ArtCraft:
// работы и видео летят на зрителя, края изогнуты линзой, радужная аберрация по краям, цветные кольца.
// Списки берутся из window.TUNNEL_IMAGES и window.TUNNEL_VIDEOS. Без WebGL2 main.js рисует 2D-версию.
(() => {
  const cvs = document.getElementById('tunnel');
  if (!cvs) return;
  const gl = cvs.getContext('webgl2', { alpha: true, premultipliedAlpha: true, antialias: true });
  if (!gl) return;
  cvs.dataset.gl = '1';

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mobile = innerWidth < 760;
  const F = 1.6;            // фокус камеры (≈ 64° обзора)
  const K = 0.16;           // сила линзы
  const Z_FAR = 7, Z_NEAR = 0.45;

  // ---------- кольца — отдельный 2D-слой под кадрами ----------
  const rc = document.createElement('canvas');
  rc.className = 'hero__canvas hero__rings';
  rc.setAttribute('aria-hidden', 'true');
  cvs.before(rc);
  const rctx = rc.getContext('2d');

  // ---------- шейдеры ----------
  const VS = `#version 300 es
  in vec2 a_uv;
  uniform vec3 u_c; uniform vec2 u_s; uniform float u_rot, u_aspect, u_f, u_k; uniform vec2 u_cam;
  out vec2 v_uv; out vec2 v_ndc; out vec2 v_n;
  void main(){
    vec2 l = (a_uv - .5) * u_s;
    float c = cos(u_rot), s = sin(u_rot);
    l = vec2(c*l.x - s*l.y, s*l.x + c*l.y);
    vec3 p = vec3(u_c.xy + l - u_cam, u_c.z);
    vec2 q = p.xy * u_f / p.z;             // экран, y ∈ [-1,1]
    q *= 1. + u_k * dot(q, q);             // искажение линзы
    vec2 n = vec2(q.x / u_aspect, q.y);
    gl_Position = vec4(n, 0., 1.);
    v_uv = a_uv; v_ndc = q; v_n = n;
  }`;
  const FS = `#version 300 es
  precision highp float;
  in vec2 v_uv; in vec2 v_ndc; in vec2 v_n; out vec4 o;
  uniform sampler2D u_t; uniform vec4 u_crop; uniform float u_a, u_ca; uniform vec2 u_px, u_hole;
  float sdr(vec2 p, vec2 b, float r){ vec2 q = abs(p) - b + r; return length(max(q, 0.)) + min(max(q.x, q.y), 0.) - r; }
  void main(){
    vec2 p = (v_uv - .5) * u_px;
    float rad = min(u_px.x, u_px.y) * .07;
    float d = sdr(p, u_px * .5, rad);
    float m = clamp(.5 - d, 0., 1.);
    if (m <= 0.) discard;
    float edge = 1. - smoothstep(0., min(u_px.x, u_px.y) * .14, -d);
    vec2 uv = u_crop.xy + v_uv * u_crop.zw;
    vec2 dir = v_ndc * u_ca * (1. + edge * 4.);
    vec3 col = vec3(texture(u_t, uv + dir).r, texture(u_t, uv).g, texture(u_t, uv - dir).b);
    col += edge * vec3(.05, .055, .07);
    // за текстом в центре кадры почти гаснут, чтобы текст читался
    float e = length(v_n / u_hole);
    float a = u_a * m * mix(.08, 1., smoothstep(.75, 1.25, e));
    o = vec4(col * a, a);
  }`;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(s)); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
  gl.useProgram(prog);
  const U = {}; ['u_hole', 'u_c', 'u_s', 'u_rot', 'u_aspect', 'u_f', 'u_k', 'u_cam', 'u_t', 'u_crop', 'u_a', 'u_ca', 'u_px'].forEach(n => U[n] = gl.getUniformLocation(prog, n));

  // сетка 16×16 — чтобы линза гнула края кадра
  const G = 16, uv = [], idx = [];
  for (let y = 0; y <= G; y++) for (let x = 0; x <= G; x++) uv.push(x / G, y / G);
  for (let y = 0; y < G; y++) for (let x = 0; x < G; x++) { const i = y * (G + 1) + x; idx.push(i, i + 1, i + G + 1, i + 1, i + G + 2, i + G + 1); }
  const vao = gl.createVertexArray(); gl.bindVertexArray(vao);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(uv), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'a_uv'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(idx), gl.STATIC_DRAW);
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);

  // ---------- текстуры: картинки и видео ----------
  const sources = [];
  const newTex = () => {
    const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([28, 30, 34, 255]));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    return t;
  };
  (window.TUNNEL_IMAGES || []).forEach(src => {
    const s = { tex: newTex(), w: 16, h: 10, ready: false };
    const im = new Image();
    im.onload = () => {
      gl.bindTexture(gl.TEXTURE_2D, s.tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      s.w = im.naturalWidth; s.h = im.naturalHeight; s.ready = true;
      if (reduce) draw(0);
    };
    im.src = src; sources.push(s);
  });
  const vids = (window.TUNNEL_VIDEOS || []).slice(0, mobile ? 3 : 12);
  vids.forEach(src => {
    const v = document.createElement('video');
    Object.assign(v, { src, muted: true, loop: true, playsInline: true, autoplay: true, preload: 'auto' });
    v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
    const s = { tex: newTex(), w: 16, h: 9, ready: false, video: v, dirty: false };
    const mark = () => { s.dirty = true; v.requestVideoFrameCallback && v.requestVideoFrameCallback(mark); };
    v.addEventListener('loadeddata', () => { s.w = v.videoWidth; s.h = v.videoHeight; s.ready = true; s.dirty = true; mark(); });
    v.play().catch(() => {});
    sources.push(s);
  });
  if (!sources.length) return;

  // ---------- кадры ----------
  const N = mobile ? 26 : 46;
  const rnd = (a, b) => a + Math.random() * (b - a);
  const pickSource = () => {
    const ready = sources.filter(s => s.ready);
    const pool = ready.length > 4 ? ready : sources;
    return pool[Math.random() * pool.length | 0];
  };
  const spawn = (c, z) => {
    let x, y, tries = 0;
    do { x = rnd(-3.2, 3.2); y = rnd(-2, 2); tries++; }
    while (tries < 8 && Math.abs(x) < 1.1 && Math.abs(y) < 0.7);
    const s = pickSource();
    const asp = Math.min(1.9, Math.max(0.8, s.w / s.h));
    const w = rnd(0.42, 0.95);
    Object.assign(c, { x, y, z: z ?? Z_FAR + rnd(0, 0.8), s, w, h: w / asp, rot: 0 });
  };
  const cards = Array.from({ length: N }, (_, i) => { const c = {}; spawn(c, Z_NEAR + 0.3 + (i / N) * (Z_FAR - Z_NEAR)); return c; });

  // ---------- кольца ----------
  const RING_COLORS = [['#7b3cff', '#2d81ff'], ['#2d81ff', '#00c2a8'], ['#22c55e', '#2d81ff'], ['#ff3b3b', '#7b3cff'], ['#2d81ff', '#22c55e']];
  const rings = Array.from({ length: 5 }, (_, i) => ({ z: Z_NEAR + 0.6 + i * (Z_FAR - Z_NEAR) / 5, a: rnd(0, 6.28), c: RING_COLORS[i % RING_COLORS.length] }));

  // ---------- размеры, мышь, скролл ----------
  let W = 0, H = 0, dpr = 1;
  const resize = () => {
    dpr = Math.min(devicePixelRatio || 1, mobile ? 1.25 : 1.6);
    W = cvs.clientWidth; H = cvs.clientHeight;
    for (const c of [cvs, rc]) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); }
    gl.viewport(0, 0, cvs.width, cvs.height);
    rctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  resize(); addEventListener('resize', resize);
  let mx = 0, my = 0, cx = 0, cy = 0;
  addEventListener('pointermove', e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; });

  // ---------- отрисовка ----------
  let angle = 0, last = performance.now(), running = true;
  function drawRings(boost) {
    rctx.clearRect(0, 0, W, H);
    const ox = W / 2 - cx * 120, oy = H / 2 + cy * 80, half = H / 2;
    for (const r of rings) {
      const q = 2.9 * F / r.z;                      // радиус в долях полуэкрана
      const rad = q * (1 + K * q * q) * half;
      if (rad > Math.hypot(W, H)) continue;
      const fade = Math.min(1, (Z_FAR - r.z) / 1.6) * Math.min(1, (r.z - Z_NEAR) / 0.6);
      if (fade <= 0) continue;
      const g = rctx.createConicGradient(r.a + angle * 2, ox, oy);
      g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.12, r.c[0]); g.addColorStop(.3, 'rgba(0,0,0,0)');
      g.addColorStop(.52, 'rgba(0,0,0,0)'); g.addColorStop(.66, r.c[1]); g.addColorStop(.82, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0)');
      rctx.globalAlpha = fade * .85;
      rctx.strokeStyle = g; rctx.lineWidth = Math.min(5, Math.max(1, 3.2 / r.z * (1 + boost)));
      rctx.beginPath(); rctx.arc(ox, oy, rad, 0, Math.PI * 2); rctx.stroke();
      // тонкая серая основа кольца
      rctx.globalAlpha = fade * .18; rctx.strokeStyle = '#f2f1ee'; rctx.lineWidth = 1;
      rctx.beginPath(); rctx.arc(ox, oy, rad, 0, Math.PI * 2); rctx.stroke();
    }
    rctx.globalAlpha = 1;
  }

  function draw(now) {
    const dt = Math.min(0.05, (now - last) / 1000 || 0); last = now;
    const prog = Math.min(1, Math.max(0, scrollY / innerHeight));
    const boost = prog * 3.5;                         // при скролле кадры летят быстрее
    cx += (mx - cx) * .05; cy += (my - cy) * .05;
    angle += dt * 0.035;

    // видео → текстуры
    for (const s of sources) if (s.video && s.dirty && s.video.readyState >= 2) {
      gl.bindTexture(gl.TEXTURE_2D, s.tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, s.video);
      s.dirty = false;
    }

    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform1f(U.u_aspect, W / H); gl.uniform1f(U.u_f, F); gl.uniform1f(U.u_k, K);
    gl.uniform2f(U.u_cam, cx * 0.9, -cy * 0.6); gl.uniform1f(U.u_ca, 0.006);
    gl.activeTexture(gl.TEXTURE0); gl.uniform1i(U.u_t, 0);
    // «дырка» под текст: половина ширины/высоты блока текста в долях экрана
    gl.uniform2f(U.u_hole, Math.min(.92, 640 / W), Math.min(.8, 330 / H));

    const speed = (reduce ? 0 : 0.42) * (1 + boost);
    for (const c of cards) { c.z -= dt * speed; if (c.z < Z_NEAR) spawn(c); }
    for (const r of rings) { r.z -= dt * speed * 0.8; if (r.z < Z_NEAR) { r.z = Z_FAR; r.a = rnd(0, 6.28); } }
    drawRings(boost);

    cards.sort((a, b) => b.z - a.z);
    const ca = Math.cos(angle), sa = Math.sin(angle);
    for (const c of cards) {
      const fade = Math.min(1, (Z_FAR - c.z) / 1.4) * Math.min(1, (c.z - Z_NEAR) / 0.35);
      if (fade <= 0.01) continue;
      const s = c.s, cardAsp = c.w / c.h, texAsp = s.w / s.h;
      let sx = 1, sy = 1;
      if (texAsp > cardAsp) sx = cardAsp / texAsp; else sy = texAsp / cardAsp;
      gl.uniform4f(U.u_crop, (1 - sx) / 2, (1 - sy) / 2, sx, sy);
      gl.uniform3f(U.u_c, c.x * ca - c.y * sa, c.x * sa + c.y * ca, c.z);
      gl.uniform2f(U.u_s, c.w, c.h);
      gl.uniform1f(U.u_rot, 0);           // кадры всегда ровные, по кругу движется только поле
      const pxH = c.h * F / c.z * (H / 2) * dpr;
      gl.uniform2f(U.u_px, pxH * cardAsp, pxH);
      gl.uniform1f(U.u_a, fade);
      gl.bindTexture(gl.TEXTURE_2D, s.tex);
      gl.drawElements(gl.TRIANGLES, idx.length, gl.UNSIGNED_SHORT, 0);
    }
    cvs.style.opacity = rc.style.opacity = String(1 - prog * 0.7);
    if (running && !reduce) requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);

  // пауза, когда hero не виден
  new IntersectionObserver(([e]) => {
    const was = running; running = e.isIntersecting;
    sources.forEach(s => s.video && (running ? s.video.play().catch(() => {}) : s.video.pause()));
    if (running && !was && !reduce) { last = performance.now(); requestAnimationFrame(draw); }
  }).observe(cvs);
})();
