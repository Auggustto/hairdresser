import type { Config } from 'jest'
const nextJest = require("next/jest");
 
const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})
 
// Add any custom config to be passed to Jest
const config: Config = {
  coverageProvider: 'babel',
  testEnvironment: 'jsdom',
  clearMocks: true,
  collectCoverage: true,
  coverageDirectory: "coverage",
  setupFilesAfterEnv: ['<rootDir>/test/setupTests.ts'],
  collectCoverageFrom: [
    '**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
  ],
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/.next/',
    '<rootDir>/cypress/',
  ],
  moduleFileExtensions: ['js', 'jsx', 'json', 'tsx', 'ts'],
  // transform: {
  //   '^.+\\.(js|jsx|ts|tsx)$': [
  //     '@swc/jest',
  //     {
  //       jsc: {
  //         baseUrl: __dirname,
  //         parser: {
  //           syntax: 'typescript',
  //           tsx: true,
  //           decorators: true,
  //           dynamicImport: true,
  //         },
  //         keepClassNames: true,
  //         transform: {
  //           legacyDecorator: true,
  //           decoratorMetadata: true,
  //           react: { runtime: 'automatic' },
  //         },
  //       },
  //       module: {
  //         type: 'es6',
  //         noInterop: false,
  //       },
  //     },
  //   ],
  // },
}
 
export default createJestConfig(config)