<template>
  <section class="container">
    <form class="is-horizontal">
      <b-field
        label="Hotkey"
        message="The shortcut for opening the application. Format: Key+Key. E.g.: Ctrl+Shift+Alt+Space"
      >
        <b-input placeholder="Type your hotkey" v-model="hotkey">ctrl+shift+space</b-input>
      </b-field>
      <b-field
        label="Main Directory"
        message="The directory all the files you want to search are located in."
      >
        <b-input placeholder="E.g.: C:\" v-model="mainDirectory">D:\GDrive\School 19_20</b-input>
      </b-field>
      <b-field
        label="Fetch timeout"
        message="The timeout between re-creating the folder structure (for indexing the files)"
      >
        <b-numberinput v-model="fetchTiemout">5</b-numberinput>
      </b-field>
      <br />
      <div class="buttons">
        <b-button type="is-success">Save!</b-button>
        <b-button type="is-danger" outlined>Cancel</b-button>
      </div>
    </form>
  </section>
</template>

<script>
/**
 * The compnent for the settings page
 */
export default {
  name: 'Settings',
  data() {
    return {
      // Defaults should be loaded from the backend (settings)
      hotkey: 'ctr+shift+space',
      mainDirectory: 'D:GDriveSchool 19_20',
      fetchTiemout: 5
    };
  }
};
</script>

<style scoped lang="scss">
section {
  padding: 3rem;
}
</style>