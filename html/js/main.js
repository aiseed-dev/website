// Theme toggle (light / dark). The actual theme is applied earlier by an
// inline script in <head> to avoid a flash of unstyled content; this block
// just wires up the toggle button after DOMContentLoaded.
function aiseedSetTheme(theme) {
    try {
        if (theme === 'light' || theme === 'dark') {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('aiseed-theme', theme);
        } else {
            document.documentElement.removeAttribute('data-theme');
            localStorage.removeItem('aiseed-theme');
        }
    } catch (e) { /* localStorage may be blocked */ }
}

document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle button — flips between light and dark explicitly.
    document.querySelectorAll('.theme-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const osDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const isDarkNow = current === 'dark' || (current === null && osDark);
            aiseedSetTheme(isDarkNow ? 'light' : 'dark');
        });
    });

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

    // Series TOC sidebar — mobile hamburger
    const seriesToc = document.getElementById('seriesToc');
    const tocToggle = document.querySelector('.series-toc-toggle');
    const tocClose = document.querySelector('.series-toc-close');
    const tocBackdrop = document.querySelector('.series-toc-backdrop');
    if (seriesToc && tocToggle) {
        const openToc = () => {
            seriesToc.classList.add('is-open');
            if (tocBackdrop) tocBackdrop.classList.add('is-open');
            document.body.classList.add('series-toc-open');
            tocToggle.setAttribute('aria-expanded', 'true');
        };
        const closeToc = () => {
            seriesToc.classList.remove('is-open');
            if (tocBackdrop) tocBackdrop.classList.remove('is-open');
            document.body.classList.remove('series-toc-open');
            tocToggle.setAttribute('aria-expanded', 'false');
        };
        tocToggle.addEventListener('click', () => {
            seriesToc.classList.contains('is-open') ? closeToc() : openToc();
        });
        if (tocClose) tocClose.addEventListener('click', closeToc);
        if (tocBackdrop) tocBackdrop.addEventListener('click', closeToc);
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && seriesToc.classList.contains('is-open')) {
                closeToc();
            }
        });
        // Tapping a chapter link inside the open mobile drawer should close it
        seriesToc.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (seriesToc.classList.contains('is-open')) closeToc();
            });
        });
    }
});
