
  <template id="upload_temp">
  <div id="myapp">
    <file-upload></file-upload>

    <form id="upload_form" role="form" enctype="multipart/form-data" method="POST">
      <input type="file" name="file" id="file" v-on:change="onFileChange" class="form-control">
      <button class="btn btn-success btn-block" @click="upload">Upload</button>
    </form>
  </div>
</template>



<script type="text/javascript">
import Vue from "vue";
Vue.component("file-upload", {
  template: "#upload_temp",
  data() {
    return {
      file: null
    };
  },
  methods: {
    onFileChange(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.createFile(files[0]);
    },
    createFile(file) {
      let reader = new FileReader();
      let vm = this;
      reader.onload = e => {
        vm.file = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    upload() {
      var data = new FormData();
      data.append("foo", "bar");
      data.append("file", document.getElementById("file").files[0]);
      axios.post("/api/upload", data).then(function(response) {
        console.log(response);
      });
    }
  }
});

});
</script>
