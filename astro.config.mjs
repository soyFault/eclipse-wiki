import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://soyfault.github.io/eclipse-wiki/
export default defineConfig({
  site: 'https://soyfault.github.io',
  base: '/eclipse-wiki',
  integrations: [
    starlight({
      title: 'Eclipse',
      description: 'Wiki de Eclipse, el mod de Among Us.',
      defaultLocale: 'root',
      locales: { root: { label: 'Español', lang: 'es' } },
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/soyFault/Eclipse' }],
      components: { Footer: './src/components/Footer.astro' },
      sidebar: [
        { label: 'Instalación', slug: 'instalacion' },
        { label: 'Roles', items: [{ autogenerate: { directory: 'roles' } }] },
        { label: 'Modificadores', items: [{ autogenerate: { directory: 'modificadores' } }] },
        { label: 'DevLog', slug: 'devlog' },
        { label: 'Android', slug: 'android' },
      ],
    }),
  ],
});
