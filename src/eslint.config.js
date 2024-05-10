export default [
  {
    languageOptions: {
      ecmaVersion: 5,
      sourceType: "script",
    },
  },
  {
    overrides: [
      {
        files: ["tests/**/*"],
        env: {
          jest: true,
        },
      },
    ],
  },
];
