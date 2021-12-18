const { resolve } = require('path');

module.exports = {
  plugins: [],
  root: resolve('./backend/frontend/static/src'),
  base: '/static/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.js', '.json'],
  },
  build: {
    outDir: resolve('./static/dist'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: resolve('./backend/frontend/static/src/js/main.js'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
};
