import type { CapacitorConfig } from '@capacitor/cli';
const config: CapacitorConfig = {
  appId: 'app.tuneez.mobile',
  appName: 'TuneEZ',
  webDir: '../frontend/public',
  server: {
    // For production point at deployed app, e.g. url: 'https://app.tuneez.com'
    cleartext: true
  }
};
export default config;
