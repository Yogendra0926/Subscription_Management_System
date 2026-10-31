/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    agentFeedback: true,
    // Prevent Windows environments with restrictive process policies from
    // spawning Next's default pool of static page-data workers.
    cpus: 1,
  },
  cacheComponents: true,
  partialPrefetching: true,
};

export default nextConfig;
