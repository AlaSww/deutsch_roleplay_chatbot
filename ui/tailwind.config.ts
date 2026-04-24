import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      colors: {
        ink: "#16141b",
        mist: "#f7f5f1",
        sand: "#efe7da",
        accent: {
          DEFAULT: "#0e7a86",
          foreground: "#f4fffe"
        },
        ember: {
          DEFAULT: "#d97732",
          foreground: "#fff8f2"
        }
      },
      boxShadow: {
        soft: "0 12px 32px rgba(15, 23, 42, 0.06)",
        glass: "0 8px 24px rgba(15, 23, 42, 0.05)"
      },
      borderRadius: {
        xl2: "1.5rem"
      },
      backgroundImage: {
        mesh:
          "linear-gradient(180deg, rgba(250,250,249,1) 0%, rgba(246,246,244,1) 100%)"
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" }
        },
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        }
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        "fade-up": "fade-up .45s ease forwards"
      }
    }
  },
  plugins: []
};

export default config;
