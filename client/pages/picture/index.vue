<template>
  <div>
    <picture-input
      ref="pictureInput"
      width="400"
      height="400"
      margin="8"
      accept="image/jpeg, image/png"
      size="10"
      :removable="true"
      :customStrings="{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a image'
      }"
    ></picture-input>
    <b-button-group>
      <b-btn @click="onChange">update</b-btn>
      <b-btn>cancel</b-btn>
    </b-button-group>
  </div>
</template>

<script>
import PictureInput from "vue-picture-input";
export default {
  components: {
    PictureInput
  },
  methods: {
    sendUploadToBackend(name, data) {
      const path = "http://localhost:5000/api/update-image";
      this.$axios.post(path, {
        name: name,
        data: data,
        username: this.$auth.user.username
      });
      console.log("tried code in sendUploadToBackend");
    },
    onChange(image) {
      console.log("New picture selected!");
      if (this.$refs.pictureInput.image) {
        this.file_name = this.$refs.pictureInput.file.name;
        console.log("Picture is loaded.");
        this.sendUploadToBackend(
          this.$refs.pictureInput.file.name,
          this.$refs.pictureInput.image
        );
      } else {
        console.log("FileReader API not supported: use the <form>, Luke!");
      }
    }
  }
};
</script>
