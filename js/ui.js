/*
 * ui.js — small shared UI helpers: modal dialogs (no browser alert/confirm), motion check, formatting.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var el = MP.util.el;

  var overlayRoot = null, openDialog = null, lastFocus = null;

  function reducedMotion() {
    var m = MP.store.get().motion;
    if (m === 'reduce') return true;
    if (m === 'full') return false;
    try { return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (e) { return false; }
  }

  function root() {
    if (!overlayRoot) overlayRoot = document.getElementById('overlay');
    return overlayRoot;
  }

  function closeDialog() {
    if (!openDialog) return;
    var d = openDialog; openDialog = null;
    if (d.parentNode) d.parentNode.removeChild(d);
    document.removeEventListener('keydown', onKey, true);
    var main = document.getElementById('app'); if (main) main.removeAttribute('aria-hidden');
    if (lastFocus && document.contains(lastFocus)) { try { lastFocus.focus({ preventScroll: true }); } catch (e) { /* ignore */ } }
    lastFocus = null;
  }

  function onKey(e) {
    if (!openDialog) return;
    if (e.key === 'Escape' && openDialog.getAttribute('data-dismiss') === '1') { e.stopPropagation(); closeDialog(); return; }
    if (e.key === 'Tab') {            // keep keyboard focus inside the dialog
      var f = openDialog.querySelectorAll('button:not([disabled]),a[href],input,[tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!openDialog.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }
  }

  /**
   * dialog({ title, body: Node|string, buttons:[{label, cls, onClick, keep}], dismissable, cls, focus: index })
   * A button closes the dialog after onClick unless keep:true.
   */
  function dialog(o) {
    closeDialog();
    lastFocus = document.activeElement;
    var titleId = 'dlgt' + Math.floor(Math.random() * 1e6);
    var card = el('div', { class: 'dialog-card ' + (o.cls || ''), attrs: { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': titleId } });
    if (o.title) card.appendChild(el('h2', { id: titleId, text: o.title }));
    if (o.body) card.appendChild(typeof o.body === 'string' ? el('p', { text: o.body }) : o.body);
    var row = el('div', { class: 'dialog-btns' });
    var btns = [];
    (o.buttons || []).forEach(function (b) {
      var node = el('button', { class: 'btn ' + (b.cls || ''), text: b.label, attrs: { type: 'button' } });
      node.addEventListener('click', function () { MP.audio.unlock(); if (!b.keep) closeDialog(); if (b.onClick) b.onClick(); });
      btns.push(node); row.appendChild(node);
    });
    card.appendChild(row);
    var wrap = el('div', { class: 'dialog', attrs: { 'data-dismiss': o.dismissable === false ? '0' : '1' } }, [card]);
    wrap.addEventListener('click', function (e) { if (e.target === wrap && o.dismissable !== false) closeDialog(); });
    root().appendChild(wrap);
    openDialog = wrap;
    var main = document.getElementById('app'); if (main) main.setAttribute('aria-hidden', 'true');
    document.addEventListener('keydown', onKey, true);
    var target = btns[o.focus != null ? o.focus : 0] || card;
    if (target === card) card.setAttribute('tabindex', '-1');
    try { target.focus({ preventScroll: true }); } catch (e) { /* ignore */ }
    return wrap;
  }

  /** Two-button confirmation. The safe choice is focused first. */
  function confirmBox(o) {
    return dialog({
      title: o.title, body: o.body, dismissable: true,
      buttons: [
        { label: o.no, cls: 'primary', onClick: o.onNo },
        { label: o.yes, cls: 'ghost danger', onClick: o.onYes }
      ]
    });
  }

  MP.ui = { dialog: dialog, closeDialog: closeDialog, confirm: confirmBox, reducedMotion: reducedMotion, isDialogOpen: function () { return !!openDialog; } };
})();
