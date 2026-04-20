// DataForge — Upload drag-and-drop
document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const fileList  = document.getElementById('file-list');
  const fileTypeSelect = document.getElementById('id_ds_filetype');
  const textSection = document.getElementById('text-items-section');
  const labelInput  = document.getElementById('id_label_classes_input');
  const labelPreview = document.getElementById('label-preview');
  const textArea    = document.getElementById('id_text_items');
  const textCount   = document.getElementById('text-count');

  // Show text section only for text datasets
  if (fileTypeSelect) {
    fileTypeSelect.addEventListener('change', () => {
      if (textSection) textSection.style.display = fileTypeSelect.value === 'text' ? '' : 'none';
    });
  }

  // Label preview chips
  if (labelInput && labelPreview) {
    labelInput.addEventListener('input', () => {
      const chips = labelInput.value.split(',').map(s => s.trim()).filter(Boolean);
      labelPreview.innerHTML = chips.map(c => `<span class="label-chip">${c}</span>`).join('');
    });
  }

  // Text item counter
  if (textArea && textCount) {
    textArea.addEventListener('input', () => {
      const n = textArea.value.split('\n').filter(l => l.trim()).length;
      textCount.textContent = `${n} item${n !== 1 ? 's' : ''}`;
    });
  }

  if (!dropZone || !fileInput) return;

  // Click to open file dialog
  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); });

  // Drag events
  ['dragenter', 'dragover'].forEach(ev => {
    dropZone.addEventListener(ev, e => { e.preventDefault(); dropZone.classList.add('dragging'); });
  });
  ['dragleave', 'drop'].forEach(ev => {
    dropZone.addEventListener(ev, () => dropZone.classList.remove('dragging'));
  });
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    renderFiles(e.dataTransfer.files);
  });
  fileInput.addEventListener('change', () => renderFiles(fileInput.files));

  function renderFiles(files) {
    if (!fileList) return;
    fileList.innerHTML = '';
    Array.from(files).forEach(f => {
      const size = (f.size / 1024).toFixed(1) + ' KB';
      const div = document.createElement('div');
      div.className = 'file-item';
      div.innerHTML = `<span class="file-icon">${f.type.startsWith('image') ? '🖼️' : '📄'}</span>
        <span class="file-name">${f.name}</span><span class="file-size">${size}</span>`;
      fileList.appendChild(div);
    });
  }
});
