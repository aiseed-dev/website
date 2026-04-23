document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');

    if (navToggle && nav) {
        navToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // Dropdown submenu (nav-group). Click on the parent button toggles
    // `.open` on the group — required for mobile accordion, harmless on
    // desktop (where the submenu also opens on :hover / :focus-within).
    document.querySelectorAll('.nav-group').forEach(group => {
        const parent = group.querySelector('.nav-parent');
        if (!parent) return;
        parent.addEventListener('click', event => {
            event.stopPropagation();
            const willOpen = !group.classList.contains('open');
            document.querySelectorAll('.nav-group.open').forEach(g => {
                if (g !== group) {
                    g.classList.remove('open');
                    const p = g.querySelector('.nav-parent');
                    if (p) p.setAttribute('aria-expanded', 'false');
                }
            });
            group.classList.toggle('open', willOpen);
            parent.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        });
    });

    // Click outside closes any open dropdown (desktop behaviour).
    document.addEventListener('click', event => {
        if (!event.target.closest('.nav-group')) {
            document.querySelectorAll('.nav-group.open').forEach(g => {
                g.classList.remove('open');
                const p = g.querySelector('.nav-parent');
                if (p) p.setAttribute('aria-expanded', 'false');
            });
        }
    });
});
