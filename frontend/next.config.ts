import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export', // <--- THIS is key for Cloudflare Pages (Static)
  images: {
    unoptimized: true, // Required for static export unless using a paid image loader
  },
  // We need to tell Next.js where the dist folder is if we want to customize it, 
  // but defaults are usually fine.
};

export default nextConfig;