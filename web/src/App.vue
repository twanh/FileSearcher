<template>
  <div id="app">
    <div class="panel">
      <div class="panel-block">
        <b-input placeholder="Search..." type="text" icon="magnify"></b-input>
      </div>
      <div class="body">
        <b-tabs v-model="activeTab" position="is-centered">
          <b-tab-item label="All" icon="file-search-outline">
            <file-item
              v-for="(file, indx) in files"
              :key="indx"
              :file="file"
              @click.native="handleOpen(file)"
            ></file-item>
          </b-tab-item>
          <b-tab-item label="Settings" icon="cog-outline">
            <settings></settings>
          </b-tab-item>
        </b-tabs>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * The main App component
 */
import FileItem from '@/components/FileItem.vue';
import Settings from '@/components/Settings.vue';
export default {
  name: 'App',
  components: {
    'file-item': FileItem,
    settings: Settings
  },
  data() {
    return {
      // Sample data
      files: [
        {
          name: 'Test File 1 ',
          file_type: 'doc',
          path: 'D:\\GDrive\\School 19_20\\Eco\\Marktgedrag'
        },
        {
          name: 'Samenvattingen ',
          file_type: 'dir',
          path: 'D:\\GDrive\\School 19_20\\Eco\\Marktgedrag'
        },
        {
          name: 'Rooster',
          file_type: 'img',
          path: 'D:\\GDrive\\School 19_20\\Eco\\Marktgedrag'
        },
        {
          name: 'Test File ',
          file_type: 'doc',
          path: 'D:\\GDrive\\School 19_20\\Eco\\Marktgedrag'
        }
      ]
    };
  },
  methods: {
    /**
     * Handles the click event on the file-item component, and opens the file
     * @param {Object} file The file that should be openend
     */
    handleOpen(file) {
      console.log(file.name);
      // TODO: Implment
    }
  }
};
</script>

<style lang="scss">
.body {
  .tab-content {
    padding: 0;
  }
}
</style>
