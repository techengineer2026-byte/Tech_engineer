document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const canvas = document.getElementById('canvasArea');
    const fontSelect = document.getElementById('fontSelect');
    const dots = document.querySelectorAll('.color-dot');

    window.changeBrand = function (color) {
        // Update Canvas Theme
        canvas.className = `canvas-area theme-${color} ${fontSelect.value}`; // Keep current font

        // Active Dot
        dots.forEach(d => d.classList.remove('active'));
        event.target.classList.add('active');
    };

    fontSelect.addEventListener('change', () => {
        // Get current color theme from class list
        const currentColor = canvas.className.match(/theme-(\w+)/)[0];
        canvas.className = `canvas-area ${currentColor} font-${fontSelect.value}`;
    });

    window.downloadMockup = function () {
        alert("Mockup generated! (This is a demo)");
    }
});