document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const screen = document.getElementById('videoScreen');
    const track = document.getElementById('videoTrack');
    const btns = document.querySelectorAll('.tool-btn');

    window.applyTool = function(tool) {
        // Reset buttons
        btns.forEach(b => b.classList.remove('active'));
        event.currentTarget.classList.add('active');

        if(tool === 'cut') {
            // Visualize Cut
            track.innerHTML = `
                <div class="clip clip-main" style="width: 45%">Clip_1</div>
                <div class="clip clip-main" style="width: 10%; background:transparent; border:none;"></div>
                <div class="clip clip-main" style="width: 45%">Clip_2</div>
            `;
            alert("Timeline Sliced!");
        } 
        else if(tool === 'grade') {
            // Apply Color Grade
            screen.classList.remove('glitch-effect');
            screen.classList.add('sepia-look'); // Add CSS filter
            track.innerHTML = `<div class="clip clip-main" style="background:#5e3c58;">Color_Graded.mp4</div>`;
        }
        else if(tool === 'fx') {
            // Apply Glitch FX
            screen.classList.remove('sepia-look');
            // Adding a temporary glitch animation via CSS class would go here
            screen.style.filter = "hue-rotate(90deg) contrast(150%)";
            setTimeout(() => { screen.style.filter = "none"; }, 500);
        }
    }
});