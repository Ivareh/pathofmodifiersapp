import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  colors: {
    ui: {
      main: "#1B1B1B",
      secondary: "#282828",
      success: "#215918",
      danger: "#FF1D1D",
      white: "#FFFFFF",
      grey: "#B3B3B3",
      dark: "#1A202C",
      input: "#2d3333",
      inputChanged: "#bea06a",
      lightInput: "#565b5b",
      queryBaseInput: "#1C5B39",
      queryMainInput: "#72AE8E",
      darkSlate: "#252D3D",
      darkBrown: "#572214",
    },
  },
  fonts: {
    body: "Josefin-Sans, Georgia, serif",
    heading: "Josefin-Sans, Georgia, serif",
    sidebar: "Inter, serif",
  },
  fontWeights: {
    hairline: 100,
    thin: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  fontSizes: {
    mini: 13,
    defaultRead: 15,
    input: 16,
    menu: 17,
  },
  lineHeights: {
    normal: "normal",
    none: 1,
    shorter: 1.25,
    short: 1.375,
    base: 1.5,
    tall: 1.625,
    taller: "2",
    "3": ".75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
  },
  letterSpacings: {
    tighter: "-0.05em",
    tight: "-0.025em",
    normal: "0",
    wide: "0.025em",
    wider: "0.05em",
    widest: "0.1em",
  },
  sizes: {
    inputSizes: {
      tinyBox: "1rem",
      miniBox: "2.5rem",
      smallBox: "6rem",
      smallPBox: "7rem",
      smallPPBox: "8rem",
      defaultBox: "13rem",
      mdBox: "15rem",
      lgBox: "280px",
      xlBox: "25rem",
      xlPlusBox: "40rem",
      gigaBox: "50rem",
      gigaPlusBox: "60rem",
      ultraBox: "67rem",
      ultraPlusBox: "80rem",
    },
    bgBoxes: {
      tinyBox: "20rem",
      smallBox: "50rem",
      mediumBox: "70rem",
      mediumPlusBox: "79rem",
      mediumPPBox: "93rem",
      defaultBox: "95rem",
      largeBox: "98rem",
      gigaBox: "130rem",
    },
  },
});

export default theme;
