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
  toggle.append(icon, label); toolbar.append(toggle); document.body.append(layer, toolbar);
  const active = () => preference && !reduced.matches && !document.hidden;

  function sprinkle() {
    const mobile = innerWidth <= 760;
    if (!active() || layer.childElementCount >= (mobile ? 3 : 5)) return;
    const kitty = document.createElement('img'); kitty.className = 'kitty-flake'; kitty.alt = '';
    kitty.src = asset(Math.random() < .5 ? 'kitty-hug.png' : 'kitty-pillow.png');
    // Keep movement in the outer margins, away from the text and map buttons.
    kitty.style.left = Math.random() < .5 ? (mobile ? '-7px' : '1%') : (mobile ? 'calc(100% - 19px)' : 'calc(100% - 42px)');
    kitty.style.width = `${mobile ? 26 : 34}px`; kitty.style.height = `${mobile ? 30 : 38}px`;
    kitty.style.setProperty('--fall-time', `${20 + Math.random() * 6}s`);
    kitty.addEventListener('animationend', () => kitty.remove(), { once: true });
    layer.append(kitty);
  }
  function update() {
    clearInterval(timer); layer.replaceChildren();
    toggle.disabled = reduced.matches;
    toggle.setAttribute('aria-pressed', String(preference && !reduced.matches));
    label.textContent = preference && !reduced.matches ? '키티 효과 끄기' : '키티 효과 켜기';
    if (reduced.matches) { label.textContent = '키티 효과 꺼짐'; toggle.title = '기기의 움직임 줄이기 설정을 따르고 있어요.'; }
    if (active()) { sprinkle(); timer = setInterval(sprinkle, 8500); }
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
