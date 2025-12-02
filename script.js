document.addEventListener('DOMContentLoaded', () => {
    
    // --- Sticky Header ---
    const header = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // --- Mobile Menu ---
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileLinks = document.querySelectorAll('.mobile-menu a');

    hamburger.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        hamburger.classList.toggle('toggle');
    });

    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            hamburger.classList.remove('toggle');
        });
    });

    // --- Image Slider Logic ---
    const track = document.querySelector('.slider-track');
    const slides = document.querySelectorAll('.slide');
    let currentIndex = 0;
    const slideCount = slides.length;
    
    // Determine slides per view based on screen width
    function getSlidesPerView() {
        return window.innerWidth < 768 ? 1 : 3;
    }

    function updateSlider() {
        const slidesPerView = getSlidesPerView();
        const slideWidth = 100 / slidesPerView;
        track.style.transform = `translateX(-${currentIndex * slideWidth}%)`;
    }

    function nextSlide() {
        const slidesPerView = getSlidesPerView();
        // Logic for infinite loop effect (simplified for this implementation)
        // We stop when we reach the end minus the visible slides
        if (currentIndex >= slideCount - slidesPerView) {
            currentIndex = 0;
        } else {
            currentIndex++;
        }
        updateSlider();
    }

    // Auto slide every 3 seconds
    setInterval(nextSlide, 3000);

    // Handle resize
    window.addEventListener('resize', updateSlider);


    // --- Booking Calculation ---
    const pickupInput = document.getElementById('pickup-date');
    const dropoffInput = document.getElementById('dropoff-date');
    const totalHoursInput = document.getElementById('total-hours');
    const driverToggle = document.getElementById('driver-toggle');
    const driverStatus = document.getElementById('driver-status');

    function calculateHours() {
        const pickup = new Date(pickupInput.value);
        const dropoff = new Date(dropoffInput.value);

        if (pickup && dropoff && dropoff > pickup) {
            const diffMs = dropoff - pickup;
            const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
            totalHoursInput.value = diffHrs;
        } else {
            totalHoursInput.value = "0";
        }
    }

    pickupInput.addEventListener('change', calculateHours);
    dropoffInput.addEventListener('change', calculateHours);

    driverToggle.addEventListener('change', () => {
        driverStatus.textContent = driverToggle.checked ? "Yes" : "No";
    });

    // --- WhatsApp Integration ---
    const whatsappBtn = document.getElementById('whatsapp-book-btn');
    
    whatsappBtn.addEventListener('click', () => {
        const location = document.getElementById('location').value;
        const pickup = pickupInput.value;
        const dropoff = dropoffInput.value;
        const vehicle = document.getElementById('vehicle-type').value;
        const driver = driverToggle.checked ? "Yes" : "No";
        const hours = totalHoursInput.value;

        // Validation
        if (!pickup || !dropoff) {
            alert("Please select pickup and drop-off dates.");
            return;
        }

        // Format Date for better readability
        const formatD = (dateStr) => {
            const d = new Date(dateStr);
            return d.toLocaleString();
        };

        const message = `Hello, I want to rent a car from Ignite Wheels.%0A%0A` +
                        `📍 *Location:* ${location}%0A` +
                        `🚗 *Vehicle:* ${vehicle}%0A` +
                        `📅 *Pickup:* ${formatD(pickup)}%0A` +
                        `📅 *Drop-off:* ${formatD(dropoff)}%0A` +
                        `⏳ *Total Duration:* ${hours} Hours%0A` +
                        `👨‍✈️ *Driver Required:* ${driver}`;

        // Replace with actual phone number
        const phoneNumber = "919999999999"; 
        const whatsappURL = `https://wa.me/${phoneNumber}?text=${message}`;

        window.open(whatsappURL, '_blank');
    });

});
