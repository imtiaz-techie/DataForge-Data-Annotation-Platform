document.addEventListener("DOMContentLoaded", function() {
    const img = document.getElementById('label-image');
    const canvas = document.getElementById('bbox-canvas');
    const ctx = canvas.getContext('2d');
    const boxListEl = document.getElementById('box-list');
    const inputEl = document.getElementById('bounding-boxes-input');
    
    let activeLabel = null;
    let isDrawing = false;
    let startX = 0, startY = 0;
    let currentX = 0, currentY = 0;
    
    // Parse existing boxes
    let boxes = [];
    try {
        const existingDataStr = document.getElementById('existing-boxes-data').textContent;
        boxes = JSON.parse(existingDataStr) || [];
    } catch(e) {
        boxes = [];
    }
    
    function initCanvas() {
        canvas.width = img.clientWidth;
        canvas.height = img.clientHeight;
        render();
    }
    
    if (img.complete) {
        initCanvas();
    } else {
        img.onload = initCanvas;
    }
    
    window.addEventListener('resize', initCanvas);
    
    window.selectActiveLabel = function(label) {
        activeLabel = label;
        document.querySelectorAll('.label-option').forEach(el => el.classList.remove('selected'));
        const input = document.querySelector(`input[value="${label}"]`);
        if (input) input.closest('.label-option').classList.add('selected');
    };
    
    // Select first label by default if available
    try {
        const labels = JSON.parse(document.getElementById('label-classes-data').textContent);
        if (labels && labels.length > 0) {
            document.querySelector(`input[value="${labels[0]}"]`).click();
        }
    } catch(e){}
    
    canvas.addEventListener('mousedown', (e) => {
        if (!activeLabel) {
            alert('Please select a label first!');
            return;
        }
        isDrawing = true;
        const rect = canvas.getBoundingClientRect();
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        const rect = canvas.getBoundingClientRect();
        currentX = e.clientX - rect.left;
        currentY = e.clientY - rect.top;
        render();
        // Draw the current box being drawn
        ctx.strokeStyle = '#3b82f6'; // blue
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.strokeRect(startX, startY, currentX - startX, currentY - startY);
        ctx.setLineDash([]);
    });
    
    canvas.addEventListener('mouseup', (e) => {
        if (!isDrawing) return;
        isDrawing = false;
        
        const rect = canvas.getBoundingClientRect();
        currentX = e.clientX - rect.left;
        currentY = e.clientY - rect.top;
        
        let x = Math.min(startX, currentX);
        let y = Math.min(startY, currentY);
        let w = Math.abs(currentX - startX);
        let h = Math.abs(currentY - startY);
        
        // Ignore tiny accidental clicks
        if (w > 5 && h > 5) {
            // Convert to original image coordinates
            const scaleX = img.naturalWidth / canvas.width;
            const scaleY = img.naturalHeight / canvas.height;
            
            boxes.push({
                label: activeLabel,
                x: Math.round(x * scaleX),
                y: Math.round(y * scaleY),
                w: Math.round(w * scaleX),
                h: Math.round(h * scaleY)
            });
            updateState();
        }
        render();
    });
    
    canvas.addEventListener('mouseleave', () => {
        if (isDrawing) {
            isDrawing = false;
            render();
        }
    });
    
    window.removeBox = function(index) {
        boxes.splice(index, 1);
        updateState();
    };
    
    function updateState() {
        inputEl.value = JSON.stringify(boxes);
        render();
        renderBoxList();
    }
    
    function renderBoxList() {
        boxListEl.innerHTML = '';
        boxes.forEach((box, index) => {
            const li = document.createElement('li');
            li.style.padding = '8px';
            li.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
            li.style.display = 'flex';
            li.style.justifyContent = 'space-between';
            li.style.alignItems = 'center';
            
            li.innerHTML = `
                <span><span class="badge badge-type">${box.label}</span></span>
                <button type="button" class="btn btn-xs btn-ghost" onclick="removeBox(${index})" style="color: #ef4444;">&times;</button>
            `;
            boxListEl.appendChild(li);
        });
    }
    
    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const scaleX = canvas.width / img.naturalWidth;
        const scaleY = canvas.height / img.naturalHeight;
        
        boxes.forEach(box => {
            const rx = box.x * scaleX;
            const ry = box.y * scaleY;
            const rw = box.w * scaleX;
            const rh = box.h * scaleY;
            
            ctx.strokeStyle = '#10b981'; // green
            ctx.lineWidth = 2;
            ctx.strokeRect(rx, ry, rw, rh);
            
            ctx.fillStyle = 'rgba(16, 185, 129, 0.5)';
            ctx.fillRect(rx, ry, rw, rh);
            
            ctx.fillStyle = '#fff';
            ctx.font = '14px sans-serif';
            ctx.fillText(box.label, rx, ry > 14 ? ry - 4 : ry + 14);
        });
    }
    
    window.prepareSubmit = function() {
        inputEl.value = JSON.stringify(boxes);
    };
    
    // Initial render
    updateState();
});
