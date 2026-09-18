const sections = [...document.querySelectorAll('main section[id]')];
const navLinks = [...document.querySelectorAll('nav a')];

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries.find((entry) => entry.isIntersecting);
    if (!visible) return;
    navLinks.forEach((link) => {
      const active = link.getAttribute('href') === `#${visible.target.id}`;
      link.toggleAttribute('aria-current', active);
    });
  },
  { rootMargin: '-35% 0px -55%', threshold: 0 }
);

sections.forEach((section) => observer.observe(section));

