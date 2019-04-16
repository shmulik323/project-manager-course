<template>
  <section class="container">
    <div
      class="quill-editor"
      :content="content"
      @change="onEditorChange($event)"
      @blur="onEditorBlur($event)"
      @focus="onEditorFocus($event)"
      @ready="onEditorReady($event)"
      v-quill:myQuillEditor="editorOption"
    ></div>
    <div>
      <a type="submit" @click="createPdf">Create PDF</a>
    </div>
  </section>
</template>

<script>
if (process.browser) {
  const jsPDF = require("jspdf");
  require("jspdf-autotable");
  let doc = new jsPDF();
  // ... you code
}

var toolbarOptions = [
  ["bold", "italic", "underline", "strike"], // toggled buttons
  ["blockquote", "code-block"],

  [{ header: 1 }, { header: 2 }], // custom button values
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }], // superscript/subscript
  [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
  [{ direction: "rtl" }], // text direction

  [{ size: ["small", false, "large", "huge"] }], // custom dropdown
  [{ header: [1, 2, 3, 4, 5, 6, false] }],

  [{ color: [] }, { background: [] }], // dropdown with defaults from theme
  [{ font: [] }],
  [{ align: [] }],

  ["clean"] // remove formatting button
];
export default {
  data() {
    return {
      content: "<p>I am Example</p>",
      editorOption: {
        // some quill options
        modules: {
          toolbar: toolbarOptions
        },
        theme: "snow"
      }
    };
  },
  mounted() {
    console.log("app init, my quill insrance object is:", this.myQuillEditor);
    setTimeout(() => {
      this.content = "i am changed";
    }, 3000);
  },
  methods: {
    onEditorBlur(editor) {
      console.log("editor blur!", editor);
    },
    onEditorFocus(editor) {
      console.log("editor focus!", editor);
    },
    onEditorReady(editor) {
      console.log("editor ready!", editor);
    },
    onEditorChange({ editor, html, text }) {
      console.log("editor change!", editor, html, text);
      this.content = html;
    },
    createPdf() {
      this.$axios
        .post("api/pdf", {
          html: this.content,
          responseType: "arraybuffer"
        })
        .then(response => {
          const url = window.URL.createObjectURL(
            new Blob([response.data], { type: "application/pdf" })
          );
          console.log(response);
          const link = document.createElement("a");
          link.href = url;

          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.container {
  width: 60%;
  margin: 0 auto;
  padding: 50px 0;
  .quill-editor {
    min-height: 600px;
    max-height: 400px;
    overflow-y: auto;
  }
}
</style>
