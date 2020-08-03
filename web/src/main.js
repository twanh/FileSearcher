import Vue from 'vue';

import Buefy from 'buefy';
import 'buefy/dist/buefy.css';

import App from './App.vue';

Vue.config.productionTip = false;

// Setup the EEL websocket connection
if (!window.eel) {
  console.error(
    'EEL does not seem to be running, please make sure the application is stared using eel!'
  );
}
window.eel.set_host('ws://localhost:3020');

// Setup Beufy
Vue.use(Buefy, {
  defaultIconPack: 'fas'
});

new Vue({
  render: h => h(App)
}).$mount('#app');
