/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['raw.githubusercontent.com', 'images.thetombomb.com'],
  },
  async redirects() {
    return [
      {
        source: '/feature/redirect',
        destination: '/feature/redirected',
        permanent: true,
      },
    ]
  },
  async rewrites() {
    return [
      {
        source: '/feature/rewrite',
        destination: '/feature/rewritten',
      },
    ]
  },
  i18n: {
    locales: ['en-US', 'fr'],
    defaultLocale: 'en-US',
  },
cacheHandler: process.env.NODE_ENV === "production" ? "./cache-handler.mjs" : undefined,
  cacheMaxMemorySize: 0,};

export default nextConfig;