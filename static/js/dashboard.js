// DataForge — Dashboard live stats polling
function pollStats() {
  fetch('/api/dashboard/stats/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(r => r.json())
    .then(data => {
      const map = {
        'kpi-datasets': data.total_datasets,
        'kpi-items': data.total_items,
        'kpi-annotated': data.total_annotated,
        'kpi-verified': data.total_verified,
        'kpi-users': data.total_users,
        'kpi-corrupted': data.total_corrupted,
      };
      Object.entries(map).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el && val !== undefined) el.textContent = val;
      });
    })
    .catch(() => {});
}

// Poll every 30 seconds
if (document.getElementById('stats-grid')) {
  setInterval(pollStats, 30000);
}
