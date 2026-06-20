document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const promptText = document.getElementById('promptText');
    const generateBtn = document.getElementById('generateBtn');
    const aiResponse = document.getElementById('aiResponse');
    const qLabel = document.querySelector('.q-label');
    const pBar = document.querySelector('.progress-bar');

    let currentMode = 'basic';

    const data = {
        basic: {
            prompt: "Write a blog about coffee.",
            response: "Coffee is a brewed drink prepared from roasted coffee beans. It is very popular around the world. People drink it in the morning. It has caffeine.",
            quality: "Low (Generic)",
            color: "bg-danger",
            width: "20%"
        },
        pro: {
            prompt: "Act as a Coffee Connoisseur. Write a captivating intro about the aroma of Ethiopian Arabica.",
            response: "As the steam rises, the floral notes of Jasmine dance with a hint of citrus bergamot. This isn't just caffeine; it's Ethiopian Yirgacheffe—a liquid legacy harvested from the birthplace of coffee...",
            quality: "High (Expert)",
            color: "bg-success",
            width: "95%"
        }
    };

    window.setMode = function (mode) {
        currentMode = mode;
        // Toggle Buttons
        document.getElementById('btnBasic').classList.toggle('active', mode === 'basic');
        document.getElementById('btnPro').classList.toggle('active', mode === 'pro');

        // Type Prompt Effect
        typeEffect(promptText, data[mode].prompt);

        // Reset Output
        aiResponse.innerHTML = '<span class="text-muted opacity-50">Waiting for generation...</span>';
        qLabel.innerText = "Quality: Unknown";
        pBar.style.width = "0%";
    };

    generateBtn.addEventListener('click', () => {
        // Loading
        generateBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Generating...';

        setTimeout(() => {
            // Type Response
            typeEffect(aiResponse, data[currentMode].response);

            // Update Meters
            qLabel.innerText = "Quality: " + data[currentMode].quality;
            pBar.className = "progress-bar " + data[currentMode].color;
            pBar.style.width = data[currentMode].width;

            generateBtn.innerHTML = 'GENERATE';
        }, 800);
    });

    function typeEffect(element, text) {
        element.innerText = "";
        let i = 0;
        let speed = 20;

        function typing() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(typing, speed);
            }
        }
        typing();
    }
});