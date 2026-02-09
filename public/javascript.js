document.addEventListener("DOMContentLoaded", () => {

    // --- 1. Mobile Navigation ---
    const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
    const navList = document.querySelector("nav ul");
    const header = document.querySelector("header");
    const navbar = document.querySelector('header .navbar'); // Added for scroll logic
    const backToTopBtn = document.getElementById("backToTop");

    if (mobileNavToggle && navList) {
        mobileNavToggle.addEventListener("click", () => {
            const isActive = navList.classList.toggle("active");
            mobileNavToggle.classList.toggle("active");
            document.body.style.overflow = isActive ? "hidden" : "";
        });

        document.querySelectorAll("nav a").forEach(link => {
            link.addEventListener("click", () => {
                navList.classList.remove("active");
                mobileNavToggle.classList.remove("active");
                document.body.style.overflow = "";
            });
        });
    }

    // --- 2. Scroll Handling (Sticky Header & Back to Top) ---
    window.scrollToTop = function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    let lastScrollY = 0;
    let ticking = false;

    function handleScroll(scroll) {
        // Sticky Header logic
        if (header) {
            if (scroll >= 50) header.classList.add("sticky");
            else header.classList.remove("sticky");
        }

        // Navbar scrolled class logic (Merged from your second scroll listener)
        if (navbar) {
            if (scroll > 30) navbar.classList.add('scrolled');
            else navbar.classList.remove('scrolled');
        }

        // Back to top button logic
        if (backToTopBtn) {
            backToTopBtn.style.display = scroll > 100 ? "block" : "none";
        }
    }

    window.addEventListener("scroll", () => {
        lastScrollY = window.scrollY;
        if (!ticking) {
            requestAnimationFrame(() => {
                handleScroll(lastScrollY);
                ticking = false;
            });
            ticking = true;
        }
    });

    // --- 3. Testimonials Slider ---
    const slides = document.querySelectorAll(".testimonial-content");
    const dots = document.querySelectorAll(".nav-dot");
    const prevBtn = document.querySelector(".nav-arrow.prev");
    const nextBtn = document.querySelector(".nav-arrow.next");
    let currentSlide = 0;

    if (slides.length && dots.length) {
        const showSlide = index => {
            slides.forEach(slide => slide.classList.remove("active"));
            dots.forEach(dot => dot.classList.remove("active"));
            slides[index].classList.add("active");
            dots[index].classList.add("active");
        };

        const nextSlide = () => {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        };

        const prevSlide = () => {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        };

        if (nextBtn) nextBtn.addEventListener("click", nextSlide);
        if (prevBtn) prevBtn.addEventListener("click", prevSlide);

        dots.forEach((dot, index) =>
            dot.addEventListener("click", () => {
                currentSlide = index;
                showSlide(currentSlide);
            })
        );
        setInterval(nextSlide, 5000);
    }

    // --- 4. Portfolio Filter ---
    const filterButtons = document.querySelectorAll(".filter-btn");
    const portfolioItems = document.querySelectorAll(".portfolio-item");

    if (filterButtons.length) {
        filterButtons.forEach(button => {
            button.addEventListener("click", () => {
                document.querySelector(".filter-btn.active")?.classList.remove("active");
                button.classList.add("active");
                const filter = button.getAttribute("data-filter");
                portfolioItems.forEach(item => {
                    item.classList.toggle(
                        "hidden",
                        !(filter === "all" || item.classList.contains(filter))
                    );
                });
            });
        });
    }

    // --- 5. Number Counters ---
    const counters = document.querySelectorAll(".counter");
    counters.forEach(counter => {
        const target = +counter.getAttribute("data-target");
        let current = 0;
        const duration = 2000;
        const increment = target / (duration / 16);
        const updateCount = () => {
            current += increment;
            if (current < target) {
                counter.innerText =
                    target > 999
                        ? Math.floor(current).toLocaleString()
                        : current.toFixed(1);
                requestAnimationFrame(updateCount);
            } else {
                counter.innerText =
                    target > 999 ? target.toLocaleString() : target;
            }
        };
        updateCount();
    });

    // --- 6. Subheader Drag/Scroll ---
    const subheader = document.getElementById("subheader");
    if (subheader) {
        let isDown = false;
        let startX;
        let scrollLeft;

        subheader.addEventListener("mousedown", e => {
            isDown = true;
            subheader.classList.add("active");
            startX = e.pageX - subheader.offsetLeft;
            scrollLeft = subheader.scrollLeft;
        });
        subheader.addEventListener("mouseleave", () => { isDown = false; subheader.classList.remove("active"); });
        subheader.addEventListener("mouseup", () => { isDown = false; subheader.classList.remove("active"); });
        subheader.addEventListener("mousemove", e => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - subheader.offsetLeft;
            const walk = (x - startX);
            subheader.scrollLeft = scrollLeft - walk;
        });

        // Touch events
        subheader.addEventListener("touchstart", e => {
            isDown = true;
            startX = e.touches[0].pageX - subheader.offsetLeft;
            scrollLeft = subheader.scrollLeft;
        });
        subheader.addEventListener("touchend", () => { isDown = false; });
        subheader.addEventListener("touchmove", e => {
            if (!isDown) return;
            const x = e.touches[0].pageX - subheader.offsetLeft;
            const walk = (x - startX);
            subheader.scrollLeft = scrollLeft - walk;
        });

        // Auto-scroll on edge hover
        subheader.addEventListener("mousemove", e => {
            const rect = subheader.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const width = rect.width;
            const edge = 100;
            let speed = 0;
            if (x < edge) {
                speed = -5 * (1 - x / edge);
            } else if (x > width - edge) {
                speed = 5 * (1 - (width - x) / edge);
            }
            if (speed !== 0) {
                if (subheader.autoScroll) cancelAnimationFrame(subheader.autoScroll);
                const step = () => {
                    subheader.scrollLeft += speed;
                    subheader.autoScroll = requestAnimationFrame(step);
                };
                step();
            } else {
                if (subheader.autoScroll) cancelAnimationFrame(subheader.autoScroll);
            }
        });
    }

    // --- 7. Auto Modal (Popup) ---
    const modal = document.getElementById("autoModal");
    const closeBtn = document.querySelector(".auto-close");

    if (modal) {
        setTimeout(() => {
            modal.style.display = "flex";
        }, 15000);

        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                modal.style.display = "none";
            });
        }
        window.addEventListener("click", e => {
            if (e.target === modal) modal.style.display = "none";
        });
    }

    // --- 8. Fetch States & Cities ---
    const stateSelect = document.getElementById("stateSelect");
    const citySelect = document.getElementById("citySelect");

    // Only fetch if elements exist to avoid wasted network calls
    if (stateSelect && citySelect) {
        fetch("states.json")
            .then(res => res.json())
            .then(data => {
                Object.keys(data).forEach(state => {
                    const opt = document.createElement("option");
                    opt.value = state;
                    opt.textContent = state;
                    stateSelect.appendChild(opt);
                });
                stateSelect.addEventListener("change", () => {
                    const cities = data[stateSelect.value] || [];
                    citySelect.innerHTML = "<option selected>Select City *</option>";
                    cities.forEach(city => {
                        const opt = document.createElement("option");
                        opt.value = city;
                        opt.textContent = city;
                        citySelect.appendChild(opt);
                    });
                });
            })
            .catch(err => console.log("States json not found or error"));
    }

    // --- 9. Forms (THE FIX IS HERE) ---

    // Fix: Check if demoForm exists before adding listener
    const demoForm = document.getElementById("demoForm");
    if (demoForm) {
        demoForm.addEventListener("submit", function (e) {
            e.preventDefault();
            // Ensure emailjs is loaded
            if (typeof emailjs !== 'undefined') {
                emailjs.sendForm("service_p7eoq6c", "template_bzwdnei", this)
                    .then(function () {
                        alert("Your demo request has been submitted!");
                    }, function (error) {
                        alert("Error: " + JSON.stringify(error));
                    });
            } else {
                alert("Email service not initialized.");
            }
        });
    }

    // Fix: Check if freebieForm exists before adding listener
    const freebieForm = document.getElementById("freebieForm");
    if (freebieForm) {
        freebieForm.addEventListener("submit", function (e) {
            e.preventDefault();
            if (typeof emailjs !== 'undefined') {
                emailjs.sendForm("service_p7eoq6c", "template_bhvibor", this)
                    .then(() => {
                        alert("Your freebie request has been sent!");
                    })
                    .catch(err => {
                        alert("Error sending message: " + JSON.stringify(err));
                    });
            } else {
                alert("Email service not initialized.");
            }
        });
    }


}); // End of DOMContentLoaded

// --- 10. Global Functions (Must be outside) ---
// These need to be global because they are called via onclick="clicktocall()" in HTML
function clicktocall() {
    window.location.href = "tel:+918544884846";
}

function clicktowhatsapp() {
    window.location.href = "https://wa.me/918544884846";
}
const jsHuman = document.getElementById('js-human');
const jsPupils = document.querySelectorAll('.js-pupil');
const jsMouth = document.querySelector('.js-mouth');
const bubble = document.getElementById('js-bubble');
const jsText = document.getElementById('js-text');

// Click / Touch Interaction
jsHuman.addEventListener('click', () => {
    jsHuman.classList.add('shake-active');
    bubble.style.opacity = '1';
    jsMouth.style.height = '18px'; // Open mouth
    jsMouth.style.borderRadius = '50%';
    jsText.innerText = "Function Executed!";

    setTimeout(() => {
        jsHuman.classList.remove('shake-active');
        bubble.style.opacity = '0';
        jsMouth.style.height = '8px'; // Close mouth
        jsMouth.style.borderRadius = '0 0 20px 20px';
        jsText.innerText = "Hover me or Click me!";
    }, 800);
});

// Mouse Move (Desktop)
document.addEventListener('mousemove', (e) => {
    // Check if JS tab is currently shown
    if (document.getElementById('tab-js').classList.contains('active')) {
        jsPupils.forEach(pupil => {
            const rect = pupil.getBoundingClientRect();
            const x = (rect.left + rect.width / 2);
            const y = (rect.top + rect.height / 2);
            const rad = Math.atan2(e.pageX - x, e.pageY - y);
            const rot = (rad * (180 / Math.PI) * -1) + 180;
            const mX = Math.sin(rad) * 4;
            const mY = Math.cos(rad) * 4;
            pupil.style.transform = `translate(${mX}px, ${mY}px)`;
        });
    }
});

