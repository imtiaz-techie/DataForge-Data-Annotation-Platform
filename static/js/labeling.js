// DataForge — Image zoom/rotate helpers
let zoomLevel = 1, rotation = 0;

function zoomIn() { zoomLevel = Math.min(zoomLevel + 0.2, 4); applyTransform(); }
function zoomOut() { zoomLevel = Math.max(zoomLevel - 0.2, 0.2); applyTransform(); }
function resetZoom() { zoomLevel = 1; rotation = 0; applyTransform(); }
function rotateImage() { rotation = (rotation + 90) % 360; applyTransform(); }

function applyTransform() {
  const img = document.getElementById('label-image');
  if (img) img.style.transform = `scale(${zoomLevel}) rotate(${rotation}deg)`;
}
