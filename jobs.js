// Jobs page: first-week checklist (saved on this device only) and copy-prompt buttons.
(function () {
  const KEY = 'air-first-week';
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } };
  const save = v => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} };
  const boxes = document.querySelectorAll('#jc-list input[type="checkbox"]');
  const prog = document.getElementById('jc-progress');
  let done = load();
  function paint() {
    boxes.forEach(b => { b.checked = done.includes(b.dataset.k); b.closest('.jc-item').classList.toggle('done', b.checked); });
    if (prog) {
      const n = done.length, t = boxes.length;
      prog.textContent = n === 0 ? '' : n >= t ? "All done. That's a strong first week. Keep going." : n + ' of ' + t + ' done.';
    }
  }
  boxes.forEach(b => b.addEventListener('change', () => {
    done = done.filter(k => k !== b.dataset.k);
    if (b.checked) done.push(b.dataset.k);
    save(done); paint();
  }));
  paint();

  document.querySelectorAll('.copy-btn').forEach(btn => btn.addEventListener('click', () => {
    const text = btn.parentElement.querySelector('.prompt-text').textContent;
    const ok = () => { btn.textContent = 'Copied ✓'; setTimeout(() => { btn.textContent = 'Copy prompt'; }, 2000); };
    const fb = () => { try { const t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.position = 'absolute'; t.style.left = '-9999px'; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); ok(); } catch (e) {} };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fb); else fb();
  }));
})();
