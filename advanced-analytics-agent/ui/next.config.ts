import { apiServer } from "@/lib/config";
import type { NextConfig } from "next";


const nextConfig: NextConfig = {
  serverExternalPackages: ["@copilotkit/runtime"],
  output: "standalone",
  async rewrites() {
    return [
      { // Proxy to backend, this must be available the "server" hostname
        source: '/api/sessions',
        destination: `${apiServer}/api/sessions` }
    ];
  },

};

export default nextConfig;
