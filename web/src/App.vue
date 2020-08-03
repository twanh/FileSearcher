<template>
  <div id="app">
    <div class="panel">
      <div class="panel-block">
        <b-input placeholder="Search..." type="text" icon="magnify"></b-input>
      </div>
      <div class>
        <b-tabs v-model="activeTab" position="is-centered">
          <b-tab-item label="All" icon="file-search-outline">fff</b-tab-item>
          <b-tab-item label="Settings" icon="cog-outline">ff</b-tab-item>
        </b-tabs>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>
