/* Progress page motion: count-ups, level-up celebration and a shareable rank card. */
window.ProgressFX = (() => {
  'use strict';
  const S = window.GlasshouseStorage, P = window.Progression;
  const calm = () => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  const seenKey = () => 'glasshouse-rank-seen-v1:' + (S?.scope?.() || 'guest');
  const pad = v => String(v).padStart(2, '0');
  const accent = () => {
    const el = document.querySelector('.journey') || document.documentElement;
    const v = getComputedStyle(el).getPropertyValue('--reward').trim() || getComputedStyle(document.documentElement).getPropertyValue('--appearance-accent').trim();
    return /^#[0-9a-f]{6}$/i.test(v) ? v : '#ff674f';
  };
  const esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  /* ---------- count-ups ---------- */
  function countUp(root) {
    if (calm()) return;
    root.querySelectorAll('[data-countup]').forEach(el => {
      const target = Number(el.dataset.countup) || 0;
      if (!target) return;
      const start = performance.now(), dur = Math.min(1600, 700 + target * 2);
      el.textContent = '0';
      const tick = now => {
        const t = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(target * e).toLocaleString();
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }

  /* ---------- confetti ---------- */
  function confetti(color) {
    if (calm()) return;
    const c = document.createElement('canvas'), x = c.getContext('2d'), dpr = Math.min(2, window.devicePixelRatio || 1);
    c.className = 'levelup-confetti';
    const W = innerWidth, H = innerHeight;
    c.width = W * dpr; c.height = H * dpr; x.scale(dpr, dpr);
    document.body.appendChild(c);
    const colors = [color, '#ffffff', '#ffd166', '#7ad7f0', color];
    const bits = Array.from({ length: 160 }, (_, i) => {
      const side = i % 2 ? 1 : -1, a = (-Math.PI / 2) + side * (0.25 + Math.random() * 0.55);
      const v = 9 + Math.random() * 9;
      return { x: W / 2 + side * W * 0.18, y: H * 0.62, vx: Math.cos(a) * v, vy: Math.sin(a) * v, r: Math.random() * 6.283, vr: (Math.random() - .5) * .35, w: 6 + Math.random() * 6, h: 3 + Math.random() * 4, c: colors[i % colors.length] };
    });
    const start = performance.now();
    const frame = now => {
      const t = now - start;
      x.clearRect(0, 0, W, H);
      for (const b of bits) {
        b.vy += .32; b.vx *= .99; b.x += b.vx; b.y += b.vy; b.r += b.vr;
        x.save(); x.globalAlpha = Math.max(0, 1 - t / 2600); x.translate(b.x, b.y); x.rotate(b.r);
        x.fillStyle = b.c; x.fillRect(-b.w / 2, -b.h / 2, b.w, b.h); x.restore();
      }
      if (t < 2600) requestAnimationFrame(frame); else c.remove();
    };
    requestAnimationFrame(frame);
  }

  /* ---------- level-up overlay ---------- */
  function levelUp(st) {
    const rank = P.ranks[st.index];
    document.querySelector('.levelup')?.remove();
    const el = document.createElement('div');
    el.className = 'levelup';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-labelledby', 'levelup-title');
    el.innerHTML = `<div class="levelup-card"><span class="journey-eyebrow">LEVEL UP</span><div class="levelup-medallion"><span>✦</span><b>${pad(st.index + 1)}</b></div><p class="levelup-kicker">You're now a</p><h2 id="levelup-title">${esc(rank[0])}</h2><p class="levelup-line">${esc(rank[2])}</p><div class="levelup-actions"><button type="button" class="btn light" data-levelup-share>Share it</button><button type="button" class="btn primary" data-levelup-close>Keep going</button></div></div>`;
    document.body.appendChild(el);
    const close = () => { el.classList.add('closing'); setTimeout(() => el.remove(), calm() ? 0 : 220); document.removeEventListener('keydown', key); };
    const key = e => { if (e.key === 'Escape') close(); };
    el.addEventListener('click', e => {
      if (e.target === el || e.target.closest('[data-levelup-close]')) close();
      else if (e.target.closest('[data-levelup-share]')) { close(); share(); }
    });
    document.addEventListener('keydown', key);
    el.querySelector('[data-levelup-close]').focus({ preventScroll: true });
    confetti(accent());
  }

  function checkRank(silentIfNew) {
    let st; try { st = P.stats(); } catch { return; }
    let seen = null; try { seen = localStorage.getItem(seenKey()); } catch {}
    const store = () => { try { localStorage.setItem(seenKey(), String(st.index)); } catch {} };
    if (seen === null) { store(); if (silentIfNew || st.index === 0) return; return; }
    if (st.index > Number(seen)) { store(); levelUp(st); }
    else if (st.index < Number(seen)) store();
  }

  /* ---------- share card ---------- */
  function roundRect(x, X, Y, w, h, r) { x.beginPath(); x.moveTo(X + r, Y); x.arcTo(X + w, Y, X + w, Y + h, r); x.arcTo(X + w, Y + h, X, Y + h, r); x.arcTo(X, Y + h, X, Y, r); x.arcTo(X, Y, X + w, Y, r); x.closePath(); }
  async function drawCard() {
    const st = P.stats(), rank = P.ranks[st.index], col = accent();
    try { await document.fonts?.ready; } catch {}
    const W = 1080, H = 1350, c = document.createElement('canvas'), x = c.getContext('2d');
    c.width = W; c.height = H;
    const font = (w, s) => `${w} ${s}px Inter, Arial, sans-serif`;
    // background
    const bg = x.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#141821'); bg.addColorStop(1, '#0b0d12');
    x.fillStyle = bg; x.fillRect(0, 0, W, H);
    const glow = x.createRadialGradient(W * .78, H * .2, 0, W * .78, H * .2, 720);
    glow.addColorStop(0, col + '66'); glow.addColorStop(1, col + '00');
    x.fillStyle = glow; x.fillRect(0, 0, W, H);
    // subtle grid
    x.strokeStyle = 'rgba(255,255,255,.045)'; x.lineWidth = 1;
    for (let g = 0; g <= W; g += 60) { x.beginPath(); x.moveTo(g, 0); x.lineTo(g, H); x.stroke(); }
    for (let g = 0; g <= H; g += 60) { x.beginPath(); x.moveTo(0, g); x.lineTo(W, g); x.stroke(); }
    // brand
    x.fillStyle = '#f4f5f7'; x.font = font(700, 44); x.textBaseline = 'alphabetic'; x.fillText('Glasshouse', 90, 140);
    const bw = x.measureText('Glasshouse').width; x.fillStyle = col; x.font = font(700, 34); x.fillText('✳', 90 + bw + 8, 118);
    x.fillStyle = 'rgba(244,245,247,.55)'; x.font = font(600, 24);
    x.fillText('MY LEARNING JOURNEY', 90, 200);
    // medallion
    const mx = W - 250, my = 300, R = 120;
    x.save(); x.beginPath();
    for (let i = 0; i < 6; i++) { const a = Math.PI / 6 + i * Math.PI / 3 - Math.PI / 2 + Math.PI / 6; const px = mx + R * Math.cos(a), py = my + R * Math.sin(a); i ? x.lineTo(px, py) : x.moveTo(px, py); }
    x.closePath(); const mg = x.createLinearGradient(mx - R, my - R, mx + R, my + R); mg.addColorStop(0, col); mg.addColorStop(1, '#ffffff');
    x.shadowColor = col; x.shadowBlur = 60; x.fillStyle = mg; x.fill(); x.restore();
    x.fillStyle = '#161a22'; x.textAlign = 'center'; x.font = font(700, 30); x.fillText('✦', mx, my - 38);
    x.font = font(700, 96); x.fillText(pad(st.index + 1), mx, my + 52); x.textAlign = 'left';
    // rank
    x.fillStyle = col; x.font = font(700, 28); x.fillText('LEVEL ' + (st.index + 1), 90, 560);
    x.fillStyle = '#ffffff'; let size = 112; x.font = font(800, size);
    while (x.measureText(rank[0]).width > W - 180 && size > 60) { size -= 4; x.font = font(800, size); }
    // wrap rank name onto two lines if it has two words and is long
    const words = rank[0].split(' ');
    if (words.length > 1 && x.measureText(rank[0]).width > W - 180 - 10) { x.fillText(words[0], 90, 680); x.fillText(words.slice(1).join(' '), 90, 680 + size); }
    else if (words.length > 1) { x.fillText(words[0], 90, 680); x.fillText(words.slice(1).join(' '), 90, 680 + size); }
    else x.fillText(rank[0], 90, 680);
    x.fillStyle = 'rgba(244,245,247,.7)'; x.font = font(400, 32); x.fillText(rank[2], 90, 680 + size + 70);
    // stats
    const stats = [[st.xp.toLocaleString(), 'XP EARNED'], [st.solved.toLocaleString(), 'PROBLEMS SOLVED'], [st.concepts.toLocaleString(), 'CONCEPTS CHECKED']];
    const top = 1000, cw = (W - 180 - 40) / 3;
    stats.forEach(([v, l], i) => {
      const X = 90 + i * (cw + 20);
      x.fillStyle = 'rgba(255,255,255,.06)'; roundRect(x, X, top, cw, 150, 22); x.fill();
      x.strokeStyle = 'rgba(255,255,255,.1)'; x.lineWidth = 2; x.stroke();
      x.fillStyle = '#ffffff'; x.font = font(700, 56); x.fillText(v, X + 28, top + 82);
      x.fillStyle = 'rgba(244,245,247,.55)'; x.font = font(600, 18); x.fillText(l, X + 28, top + 120);
    });
    // progress to next rank
    const by = 1210;
    x.fillStyle = 'rgba(255,255,255,.1)'; roundRect(x, 90, by, W - 180, 14, 7); x.fill();
    if (st.fraction > 0) { x.fillStyle = col; roundRect(x, 90, by, Math.max(14, (W - 180) * Math.min(1, st.fraction)), 14, 7); x.fill(); }
    x.fillStyle = 'rgba(244,245,247,.6)'; x.font = font(500, 24);
    x.fillText(st.next ? `${Math.round(st.fraction * 100)}% to ${st.next[0]}` : 'Highest rank reached', 90, by + 60);
    x.textAlign = 'right'; x.fillStyle = 'rgba(244,245,247,.85)'; x.font = font(600, 24);
    x.fillText('glasshouse.jackchobanian.com', W - 90, by + 60); x.textAlign = 'left';
    return { canvas: c, rank: rank[0] };
  }

  async function share() {
    let card; try { card = await drawCard(); } catch { return; }
    const blob = await new Promise(r => card.canvas.toBlob(r, 'image/png'));
    if (!blob) return;
    const file = new File([blob], 'glasshouse-rank.png', { type: 'image/png' }), url = URL.createObjectURL(blob);
    const canShare = !!(navigator.canShare && navigator.canShare({ files: [file] }));
    document.querySelector('.share-sheet')?.remove();
    const el = document.createElement('div');
    el.className = 'share-sheet';
    el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', 'Share your rank');
    el.innerHTML = `<div class="share-card"><img src="${url}" alt="Your Glasshouse rank card: ${esc(card.rank)}"><div class="share-actions">${canShare ? '<button type="button" class="btn primary" data-share-native>Share</button>' : ''}<a class="btn ${canShare ? 'light' : 'primary'}" href="${url}" download="glasshouse-rank.png">Download image</a><button type="button" class="btn light" data-share-close>Close</button></div></div>`;
    document.body.appendChild(el);
    const close = () => { el.remove(); URL.revokeObjectURL(url); document.removeEventListener('keydown', key); };
    const key = e => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', key);
    el.addEventListener('click', async e => {
      if (e.target === el || e.target.closest('[data-share-close]')) close();
      else if (e.target.closest('[data-share-native]')) { try { await navigator.share({ files: [file], title: 'My Glasshouse rank', text: `I'm a ${card.rank} on Glasshouse ✳` }); } catch {} }
    });
    (el.querySelector('[data-share-native]') || el.querySelector('a')).focus({ preventScroll: true });
  }

  /* ---------- wiring ---------- */
  function mount() {
    const root = document.querySelector('.journey');
    if (!root) return;
    countUp(root);
    root.querySelector('[data-share-rank]')?.addEventListener('click', share);
    const spin = card => { card.classList.remove('spin'); void card.offsetWidth; card.classList.add('spin'); clearTimeout(card._spin); card._spin = setTimeout(() => card.classList.remove('spin'), 1000); };
    root.querySelectorAll('.milestone').forEach(card => {
      card.addEventListener('click', () => spin(card));
      card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); spin(card); } });
    });
    setTimeout(() => checkRank(true), calm() ? 0 : 900);
  }
  // Rank-ups that happen while practicing anywhere on the site.
  let t;
  S?.onChange?.(k => { if (String(k).startsWith('foundry-answer-v1-rewards-')) { clearTimeout(t); t = setTimeout(() => checkRank(false), 700); } });
  try { checkRank(true); } catch {}
  return { mount, share, levelUp: () => levelUp(P.stats()) };
})();
