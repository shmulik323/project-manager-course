<template>
  <div>
    <input type="file" @change="onFileChanged">
    <v-btn @click="onUpload">Upload!</v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null
    };
  },
  methods: {
    onFileChanged(event) {
      this.selectedFile = event.target.files[0];
    },
    onUpload() {
      const formData = new FormData();
      formData.append("image", this.selectedFile, this.selectedFile.name);
      this.$axios.post("http://127.0.0.1:5000/api/uploader", formData);
    }
  }
};
</script>

<style>
</style>
