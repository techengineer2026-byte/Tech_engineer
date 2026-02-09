document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const box = document.getElementById('previewBox');
    const radiusInput = document.getElementById('radiusRange');
    const shadowInput = document.getElementById('shadowRange');
    const rotateInput = document.getElementById('rotateRange');
    const codeBlock = document.getElementById('cssCode');

    function updateStyle() {
        const r = radiusInput.value;
        const s = shadowInput.value;
        const deg = rotateInput.value;

        // Apply Styles
        box.style.borderRadius = `${r}px`;
        box.style.boxShadow = `0 10px ${s}px rgba(45, 212, 191, ${s / 100 + 0.1})`; // Teal shadow
        box.style.transform = `rotate(${deg}deg)`;

        // Update Code Snippet
        codeBlock.innerHTML = `
border-radius: ${r}px;<br>
box-shadow: 0 10px ${s}px rgba(...);<br>
transform: rotate(${deg}deg);`;
    }

    // Listeners
    radiusInput.addEventListener('input', updateStyle);
    shadowInput.addEventListener('input', updateStyle);
    rotateInput.addEventListener('input', updateStyle);

    // Initial call
    updateStyle();
});