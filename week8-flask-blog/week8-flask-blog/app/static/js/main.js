// Confirm before submitting any form that declares data-confirm="message"
document.addEventListener('submit', function (e) {
  const msg = e.target.dataset && e.target.dataset.confirm;
  if (msg && !window.confirm(msg)) { e.preventDefault(); }
});
