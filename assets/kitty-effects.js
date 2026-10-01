(() => {
  const script = document.currentScript;
  const asset = name => new URL(`kitty/${name}`, script.src).href;
  document.querySelectorAll('.brand-mark').forEach(mark => {
    const icon = document.createElement('img');
    icon.src = asset('kitty-hug.png'); icon.alt = ''; icon.width = 44; icon.height = 44;
    mark.replaceChildren(icon);
  });
  if (document.body.classList.contains('kitty-legacy')) {
    const back = document.createElement('a');
    back.className = 'legacy-back'; back.href = new URL('../history.html', script.src).href;
    const icon = document.createElement('img'); icon.src = asset('kitty-hug.png'); icon.alt = '';
    back.append(icon, '← 과거 내역');
    document.querySelector('main').prepend(back);
  }

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let preference = true;
  try { preference = localStorage.getItem('kitty-motion') !== 'off'; } catch {}
  let timer;
  const layer = document.createElement('div'); layer.className = 'kitty-rain'; layer.setAttribute('aria-hidden', 'true');
  const toolbar = document.createElement('div'); toolbar.className = 'kitty-toolbar';
  const toggle = document.createElement('button'); toggle.className = 'kitty-toggle'; toggle.type = 'button';
  const label = document.createElement('span');
  const icon = document.createElement('img'); icon.src = asset('kitty-hug.png'); icon.alt = '';
  toggle.append(icon, label); toolbar.append(toggle); document.body.append(layer);
  const headerSlot = document.querySelector('.header-caption');
  if (headerSlot) headerSlot.replaceWith(toggle);
  else {
    const header = document.querySelector('.site-header');
    if (header) header.after(toolbar);
    else document.querySelector('main').before(toolbar);
  }
  const stickers = ['kitty-traveler.png', 'kitty-cloud.png', 'kitty-hug.png', 'kitty-pillow.png'];
  let stickerIndex = 0;
  const active = () => preference && !reduced.matches && !document.hidden;

  function sprinkle(progress = 0, side = Math.random() < .5 ? 'left' : 'right') {
    const mobile = innerWidth <= 760;
    if (!active() || layer.childElementCount >= (mobile ? 3 : 5)) return;
    const kitty = document.createElement('img'); kitty.className = 'kitty-flake'; kitty.alt = '';
    kitty.src = asset(stickers[stickerIndex++ % stickers.length]);
    // Keep movement in the outer margins, away from the text and map buttons.
    kitty.style.left = side === 'left' ? (mobile ? '2px' : '12px') : (mobile ? 'calc(100% - 36px)' : 'calc(100% - 60px)');
    kitty.style.width = `${mobile ? 32 : 44}px`; kitty.style.height = `${mobile ? 38 : 50}px`;
    const duration = 18 + Math.random() * 4;
    kitty.style.setProperty('--fall-time', `${duration}s`);
    kitty.style.animationDelay = `${-progress * duration}s`;
    kitty.addEventListener('animationend', () => kitty.remove(), { once: true });
    layer.append(kitty);
  }
  function update() {
    clearInterval(timer); layer.replaceChildren();
    toggle.disabled = reduced.matches;
    toggle.setAttribute('aria-pressed', String(preference && !reduced.matches));
    label.textContent = '키티 효과';
    toggle.setAttribute('aria-label', preference && !reduced.matches ? '키티 효과 끄기' : '키티 효과 켜기');
    toggle.title = preference ? '눌러서 키티 효과를 끌 수 있어요.' : '눌러서 키티 효과를 켤 수 있어요.';
    if (reduced.matches) { label.textContent = '효과 꺼짐'; toggle.setAttribute('aria-label', '키티 효과 꺼짐'); toggle.title = '기기의 움직임 줄이기 설정을 따르고 있어요.'; }
    if (active()) {
      // Seed two visible stickers immediately instead of waiting for them to enter the screen.
      sprinkle(.18, 'left'); sprinkle(.43, 'right');
      timer = setInterval(() => sprinkle(), 6000);
    }
  }
  toggle.addEventListener('click', () => {
    preference = !preference;
    try { localStorage.setItem('kitty-motion', preference ? 'on' : 'off'); } catch {}
    update();
  });
  document.addEventListener('visibilitychange', update);
  reduced.addEventListener('change', update);
  matchMedia('(max-width: 760px)').addEventListener('change', update);
  update();
})();
