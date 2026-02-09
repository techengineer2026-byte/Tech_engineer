document.addEventListener("DOMContentLoaded", function () {
    
    // Inputs
    const textInput = document.getElementById('btnTextInput');
    const colorInput = document.getElementById('btnColorInput');
    
    // Virtual Devices
    const iosBtn = document.getElementById('iosBtn');
    const androidBtn = document.getElementById('androidBtn');

    // Function to apply styles
    function updateHotReload() {
        const newText = textInput.value;
        const newColor = colorInput.value;

        // Apply to iOS
        iosBtn.innerText = newText;
        iosBtn.style.backgroundColor = newColor;
        iosBtn.style.color = isLight(newColor) ? 'black' : 'white'; // Smart text contrast

        // Apply to Android
        androidBtn.innerText = newText;
        androidBtn.style.backgroundColor = newColor;
        androidBtn.style.color = isLight(newColor) ? 'black' : 'white';
        
        // Android buttons are often uppercase by default, let's keep it simple
        androidBtn.style.textTransform = "uppercase"; 
    }

    // Helper: Determine if color is light or dark for contrast text
    function isLight(color) {
        const hex = color.replace('#', '');
        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);
        const brightness = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        return brightness > 155;
    }

    // Event Listeners
    textInput.addEventListener('input', updateHotReload);
    colorInput.addEventListener('input', updateHotReload);

    // Initial Run
    updateHotReload();
});