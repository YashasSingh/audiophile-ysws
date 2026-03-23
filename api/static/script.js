document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach((item) => {
        const button = item.querySelector('.faq-question');
        button.addEventListener('click', () => {
            const isOpen = item.classList.contains('is-open');
            faqItems.forEach((other) => {
                other.classList.remove('is-open');
                other.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
            });
            if (!isOpen) {
                item.classList.add('is-open');
                button.setAttribute('aria-expanded', 'true');
            }
        });
    });

    const revealItems = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    revealItems.forEach((item) => observer.observe(item));

    const larpTrigger = document.querySelector('.larp-trigger');
    const larpPopup = document.querySelector('.larp-popup');

    if (larpTrigger && larpPopup) {
        const gifBase = larpTrigger.dataset.gifBase || '';
        const gifs = (larpTrigger.dataset.gifs || '').split('|').filter(Boolean);
        const img = larpPopup.querySelector('img');

        const showPopup = () => {
            if (!gifs.length) return;
            const pick = gifs[Math.floor(Math.random() * gifs.length)];
            if (img) {
                img.src = `${gifBase}/${encodeURIComponent(pick)}`;
            }
            larpPopup.classList.add('is-visible');
            larpPopup.setAttribute('aria-hidden', 'false');
        };

        const hidePopup = () => {
            larpPopup.classList.remove('is-visible');
            larpPopup.setAttribute('aria-hidden', 'true');
        };

        larpTrigger.addEventListener('mouseenter', showPopup);
        larpTrigger.addEventListener('mouseleave', hidePopup);
        larpTrigger.addEventListener('focus', showPopup);
        larpTrigger.addEventListener('blur', hidePopup);
    }
});
