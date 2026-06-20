document.addEventListener("DOMContentLoaded", function () {

    const gravityToggle = document.getElementById('gravityToggle');
    const gravityStatus = document.getElementById('gravityStatus');
    const objects = document.querySelectorAll('.game-object');

    function updatePhysics() {
        if (gravityToggle.checked) {
            // GRAVITY ON
            gravityStatus.innerHTML = "ON (9.81)";
            gravityStatus.style.color = "#00ff9d"; // Neon Green

            objects.forEach((obj, index) => {
                // Add staggered delay for realism
                setTimeout(() => {
                    obj.classList.add('falling');
                    obj.classList.remove('floating');
                }, index * 200);
            });

        } else {
            // GRAVITY OFF (Zero G)
            gravityStatus.innerHTML = "OFF (Zero G)";
            gravityStatus.style.color = "#ff0055"; // Red

            objects.forEach(obj => {
                obj.classList.remove('falling');
                // Reset positions
                obj.style.top = "";

                // Add float animation
                setTimeout(() => {
                    obj.classList.add('floating');
                }, 100);
            });
        }
    }

    // Listener
    gravityToggle.addEventListener('change', updatePhysics);

    // Initial State
    updatePhysics();

});