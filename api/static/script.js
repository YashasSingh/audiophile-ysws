document.addEventListener('DOMContentLoaded', () => {
    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach((item) => {
        const summary = item.querySelector('summary');
        if (summary) {
            summary.addEventListener('click', (e) => {
                // Browser handles details/summary automatically
            });
        }
    });

    // Journal Form Handler
    const journalForm = document.getElementById('journalForm');
    const journalEntry = document.getElementById('journalEntry');
    const journalEntries = document.getElementById('journalEntries');

    if (journalForm && journalEntry && journalEntries) {
        journalForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const text = journalEntry.value.trim();
            if (!text) return;

            // Create new journal entry element
            const entryDiv = document.createElement('div');
            entryDiv.className = 'journal-entry';
            entryDiv.innerHTML = `
                <strong>Entry</strong> — ${text}
                <div style="font-size: 12px; color: var(--text-muted); margin-top: 8px;">
                    ${new Date().toLocaleString()}
                </div>
            `;

            // Add to beginning of entries list
            journalEntries.insertBefore(entryDiv, journalEntries.firstChild);

            // Clear input
            journalEntry.value = '';
            journalEntry.focus();
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});

