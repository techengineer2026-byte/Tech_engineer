document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const marketInput = document.getElementById('marketingRange');
    const priceInput = document.getElementById('priceRange');
    const marketDisplay = document.getElementById('marketingVal');
    const priceDisplay = document.getElementById('priceVal');
    
    const salesEl = document.getElementById('salesCount');
    const revenueEl = document.getElementById('revenueVal');
    const profitEl = document.getElementById('profitVal');
    const revBar = document.getElementById('revBar');

    function calculate() {
        const marketing = parseInt(marketInput.value);
        const price = parseInt(priceInput.value);

        // Update UI Text
        marketDisplay.innerText = `₹${marketing.toLocaleString()}`;
        priceDisplay.innerText = `₹${price.toLocaleString()}`;

        // Business Logic Simulation
        // Higher marketing = more traffic. Higher price = less conversion.
        const traffic = marketing / 10; 
        const conversionRate = Math.max(0.01, 0.1 - (price / 5000)); // Price sensitivity
        
        const sales = Math.floor(traffic * conversionRate * 1000);
        const revenue = sales * price;
        const profit = revenue - marketing - (sales * 100); // Assuming 100 cost per unit

        // Update Dashboard
        salesEl.innerText = sales.toLocaleString();
        revenueEl.innerText = `₹${(revenue/100000).toFixed(2)}L`;
        
        if(profit > 0) {
            profitEl.innerText = `+₹${(profit/100000).toFixed(2)}L`;
            profitEl.className = "text-gold";
            revBar.style.backgroundColor = "#FFD700";
        } else {
            profitEl.innerText = `-₹${(Math.abs(profit)/100000).toFixed(2)}L`;
            profitEl.className = "text-danger";
            revBar.style.backgroundColor = "#dc3545"; // Red for loss
        }

        // Animate Bar Height (Max Rev assumed 10L for scaling)
        let heightPct = Math.min(100, (revenue / 1000000) * 100);
        revBar.style.height = `${Math.max(5, heightPct)}%`;
    }

    marketInput.addEventListener('input', calculate);
    priceInput.addEventListener('input', calculate);

    // Init
    calculate();
});