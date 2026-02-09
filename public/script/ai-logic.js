document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    // 1. HERO TYPEWRITER
    const heroText = "I can help you analyze data, design logos, and write emails in seconds.";
    const heroDisplay = document.getElementById('chatTypewriter');
    let i = 0;

    function typeHero() {
        if (i < heroText.length) {
            heroDisplay.innerHTML += heroText.charAt(i);
            i++;
            setTimeout(typeHero, 50);
        }
    }
    setTimeout(typeHero, 1000); // Start after 1s

    // 2. PROMPT SIMULATOR
    window.runAISimulation = function() {
        const output = document.getElementById('aiOutputText');
        const loader = document.querySelector('.loader');
        
        output.innerText = "";
        loader.style.display = "inline-block";

        setTimeout(() => {
            loader.style.display = "none";
            const response = "Strategy: 1. Launch Instagram Ads targeting students. 2. Offer 'Buy 1 Get 1' on Fridays. 3. Use AI-generated posters for local events.";
            
            let j = 0;
            function typeResponse() {
                if (j < response.length) {
                    output.innerHTML += response.charAt(j);
                    j++;
                    setTimeout(typeResponse, 30);
                }
            }
            typeResponse();
        }, 1500);
    }
});