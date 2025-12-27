/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/ocr',
        destination: 'http://localhost:4000/ocr',
      },
    ];
  },
};

module.exports = nextConfig;