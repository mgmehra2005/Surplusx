/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        parabolica: ['parabolica', 'sans-serif'],
        instrument: ['"Instrument Serif"', 'serif'],
      },
    },
  },
  plugins: [],
}
