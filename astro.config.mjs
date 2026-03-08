import { defineConfig } from 'astro/config';
export default defineConfig({
  output: 'static',
  site: 'https://firemaths.info',
  build: { format: 'file' },
});
