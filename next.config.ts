import type { NextConfig } from "next";

const nextConfig: NextConfig = {
      cacheComponents: true,
      partialPrefetching: true,
      reactCompiler: true,

      async rewrites() {
            return [
                  {
                        source: "/api/ai/:path*",
                        destination: "http://127.0.0.1:8090/api/:path*",
                  },
            ];
      },
};

export default nextConfig;