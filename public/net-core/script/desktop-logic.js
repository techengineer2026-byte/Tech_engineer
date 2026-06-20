document.addEventListener("DOMContentLoaded", function () {
    
    // Global scope functions so onclick works
    window.addComponent = function(type) {
        const canvas = document.getElementById('designCanvas');
        const xamlOutput = document.getElementById('dynamicXaml');
        const placeholder = document.querySelector('.placeholder-text');

        // Hide placeholder if it exists
        if(placeholder) placeholder.style.display = 'none';

        // 1. Create Visual Element
        let element = document.createElement('div');
        let xamlLine = "";

        if (type === 'button') {
            element.className = "btn btn-primary shadow-sm mb-2";
            element.innerText = "Click Me";
            xamlLine = `&nbsp;&nbsp;&nbsp;&nbsp;&lt;<span class="x-tag">Button</span> <span class="x-attr">Content</span>=<span class="x-val">"Click Me"</span> /&gt;<br>`;
        } 
        else if (type === 'input') {
            element.className = "form-control mb-2";
            element.placeholder = "Enter text...";
            xamlLine = `&nbsp;&nbsp;&nbsp;&nbsp;&lt;<span class="x-tag">TextBox</span> <span class="x-attr">Text</span>=<span class="x-val">"Enter text..."</span> /&gt;<br>`;
        }
        else if (type === 'switch') {
            element.innerHTML = `<div class="form-check form-switch"><input class="form-check-input" type="checkbox"><label class="form-check-label">Toggle</label></div>`;
            xamlLine = `&nbsp;&nbsp;&nbsp;&nbsp;&lt;<span class="x-tag">ToggleButton</span> <span class="x-attr">Content</span>=<span class="x-val">"Toggle"</span> /&gt;<br>`;
        }

        // Add to DOM
        canvas.appendChild(element);

        // Add to XAML Code (Append string)
        let currentXaml = xamlOutput.innerHTML;
        xamlOutput.innerHTML = currentXaml + xamlLine;
    };

    window.clearCanvas = function() {
        const canvas = document.getElementById('designCanvas');
        const xamlOutput = document.getElementById('dynamicXaml');
        
        // Reset
        canvas.innerHTML = '<p class="text-muted placeholder-text">Drag & Drop Controls Here (Click buttons above)</p>';
        xamlOutput.innerHTML = '';
    };

});