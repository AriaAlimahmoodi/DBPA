// tailwind.config.js
module.exports = {
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./users/templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        militaryOlive: '#4B5320',
        militaryDark: '#1F2421',
        militaryGrayGreen: '#6B6B47',
        militaryBrown: '#3B2F2F',
        militaryLightGray: '#9A9A7C',
        militaryOffWhite: '#D9D9D9',
      }
    },
  },
  plugins: [],
}
