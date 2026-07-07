import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: [
    '172.26.0.1',
    '172.26.0.1:3000',
    '10.50.61.58',
    '10.50.61.58:3000',
    'localhost',
    'localhost:3000'
  ],
};

export default nextConfig;
