document.addEventListener("DOMContentLoaded", () => {
    // ===== Mobile Navigation =====
    const mobileNavToggle = document.querySelector(".mobile-nav-toggle");
    const navList = document.querySelector("nav ul");
    const header = document.querySelector("header");
    const backToTopBtn = document.getElementById("backToTop");

    if (mobileNavToggle && navList) {
        mobileNavToggle.addEventListener("click", () => {
            const isActive = navList.classList.toggle("active");
            mobileNavToggle.classList.toggle("active");

            // ✅ Prevent body from scrolling when menu is open
            if (isActive) {
                document.body.style.overflow = "hidden";
            } else {
                document.body.style.overflow = "";
            }
        });

        // ✅ Also close menu & restore scroll when clicking a link
        document.querySelectorAll("nav a").forEach(link => {
            link.addEventListener("click", () => {
                navList.classList.remove("active");
                mobileNavToggle.classList.remove("active");
                document.body.style.overflow = "";
            });
        });
    }

    // ===== Smooth Scroll To Top =====
    window.scrollToTop = function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    // ===== Optimized Scroll Events (Sticky + Back To Top) =====
    let lastScrollY = 0;
    let ticking = false;

    function handleScroll(scroll) {
        if (scroll >= 50) header?.classList.add("sticky");
        else header?.classList.remove("sticky");

        if (backToTopBtn)
            backToTopBtn.style.display = scroll > 100 ? "block" : "none";
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

    // ===== Testimonial Slider =====
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

        nextBtn?.addEventListener("click", nextSlide);
        prevBtn?.addEventListener("click", prevSlide);

        dots.forEach((dot, index) =>
            dot.addEventListener("click", () => {
                currentSlide = index;
                showSlide(currentSlide);
            })
        );

        // Auto slide every 5 seconds (optimized)
        setInterval(nextSlide, 5000);
    }

    // ===== Portfolio Filter =====
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


    // ===== Animated Counters =====
    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {
        const target = +counter.getAttribute("data-target");
        let current = 0;
        const duration = 2000;
        const increment = target / (duration / 16); // smooth 60fps

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
});

window.addEventListener('scroll', function () {
    const nav = document.querySelector('header .navbar');
    if (!nav) return; // stop errors

    if (window.scrollY > 30) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});


const subheader = document.getElementById("subheader");
const modal = document.getElementById("autoModal");
const closeBtn = document.querySelector(".auto-close");

if (subheader) {
    // Drag/swipe events
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

    // Touch support
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

    // Auto scroll on hover (desktop)
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

// Show after 5 sec ONLY if exists
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


function clicktocall() {
    window.location.href = "tel:+918544884846";
}

function clicktowhatsapp() {
    window.location.href = "https://wa.me/918544884846";
}

fetch("states.json")
    .then(res => res.json())
    .then(data => {
        const stateSelect = document.getElementById("stateSelect");
        const citySelect = document.getElementById("citySelect");

        if (stateSelect && citySelect) {
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
        }

    });


document.getElementById("demoForm").addEventListener("submit", function (e) {
    e.preventDefault();

    emailjs.sendForm("service_p7eoq6c", "template_bzwdnei", this)
        .then(function () {
            alert("Your demo request has been submitted!");
        }, function (error) {
            alert("Error: " + JSON.stringify(error));
        });
});
document.getElementById("freebieForm").addEventListener("submit", function (e) {
    e.preventDefault();

    emailjs.sendForm("service_p7eoq6c", "template_bhvibor", this)
        .then(() => {
            alert("Your freebie request has been sent!");
        })
        .catch(err => {
            alert("Error sending message: " + JSON.stringify(err));
        });
});

// // 1. Mobile/Tablet Menu Toggle
// const mobileBtn = document.querySelector(".mobile-nav-toggle");
// const navMenu = document.querySelector(".nav-menu");
// const bars = document.querySelectorAll(".mobile-nav-toggle span");

// mobileBtn.addEventListener("click", () => {
//     navMenu.classList.toggle("active");

//     // Hamburger to X animation
//     if (navMenu.classList.contains("active")) {
//         bars[0].style.transform = "rotate(45deg) translate(5px, 6px)";
//         bars[1].style.opacity = "0";
//         bars[2].style.transform = "rotate(-45deg) translate(5px, -6px)";
//     } else {
//         bars[0].style.transform = "none";
//         bars[1].style.opacity = "1";
//         bars[2].style.transform = "none";
//     }
// });

// // 2. Sticky Header Effect
// window.addEventListener("scroll", () => {
//     const header = document.querySelector(".header");
//     header.classList.toggle("sticky", window.scrollY > 50);
// });
// // Portfolio Filtering Logic
// const filterButtons = document.querySelectorAll('.filter-btn');
// const portfolioItems = document.querySelectorAll('.portfolio-item');

// filterButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         filterButtons.forEach(btn => btn.classList.remove('active'));
//         button.classList.add('active');

//         const filterValue = button.getAttribute('data-filter');

//         portfolioItems.forEach(item => {
//             if (filterValue === 'all' || item.classList.contains(filterValue)) {
//                 item.style.display = 'block';
//                 setTimeout(() => {
//                     item.style.opacity = '1';
//                     item.style.transform = 'scale(1)';
//                 }, 50);
//             } else {
//                 item.style.opacity = '0';
//                 item.style.transform = 'scale(0.8)';
//                 setTimeout(() => {
//                     item.style.display = 'none';
//                 }, 300);
//             }
//         });
//     });
// });