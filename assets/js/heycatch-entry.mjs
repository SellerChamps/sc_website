import { analytics } from '@heycatch/sdk';

analytics.init({
  projectKey: 'hck_pk_DuduTtMpBcwMXzmDVcOqXVGkZW7QzNCR',
  site: 'landing',
  requestBatching: false,
  install: {
    framework: 'web',
    agent: 'cursor',
  },
});