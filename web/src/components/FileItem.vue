<template>
  <div class="panel-block">
    <b-icon :icon="getIconName()" size="is-small"></b-icon>
    <span class="spaced is-size-6">{{file.name}}</span>
    <span class="small-file-path">{{file.path}}</span>
  </div>
</template>

<script>
/**
 * FileItem shows the information about a particular file.
 */
export default {
  name: 'FileItem',
  props: ['file', 'onOpen'],
  methods: {
    /**
     * getIconName uses the file_type property of the file to determine what icon should be shown
     * @returns {string} The name of the icon that should be displayed
     */
    getIconName() {
      switch (this.file.file_type) {
        case 'doc':
          return 'file-word';
        case 'dir':
          return 'folder';
        case 'img':
          return 'file-image';
        case 'any':
          return 'file';
        default:
          return 'file';
      }
    }
  }
};
</script>
e
<style lang="scss" scoped>
.panel-block {
  cursor: pointer;
  &:hover {
    span {
      i {
        color: #7957d5;
      }
    }
  }
}
.spaced {
  padding-left: 0.5rem;
}
.small-file-path {
  margin-left: 5px;
  color: 'gray';
  font-size: 10px;
}
</style>* 