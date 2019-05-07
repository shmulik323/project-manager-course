<template>
  <v-layout column>
    <v-text-field label="Project Name" box v-model="pdfName"></v-text-field>

    <v-layout align-center justify-center row fill-height>
      <v-flex xs12 sm2>
        <v-card>
          <v-card-title>
            <span class="title font-weight-dark">Load your prev project</span>
          </v-card-title>
          <v-sheet class="d-flex" color="grey lighten-3" height="600px" with="300px">
            <v-list>
              <v-btn :key="pdf.name" v-for="pdf in pdfs" @click="content=pdf.data">{{pdf.name}}</v-btn>
            </v-list>
          </v-sheet>
        </v-card>
      </v-flex>
      <v-flex>
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
            <a type="submit" id="pdf" @click="createPdf" target="_blank">Create PDF</a>
          </div>
        </section>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
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
  auth: true,
  data() {
    return {
      pdfs: null,
      content: "<p>I am Example</p>",
      editorOption: {
        // some quill options
        modules: {
          toolbar: toolbarOptions
        },
        theme: "snow"
      },
      pdfName: "your Project name"
    };
  },
  created() {
    getPdf: {
      this.$axios.get("api/pdf", {}).then(res => {
        this.pdfs = res.data.pdfs;
      });
    }
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
      const vm = this;
      this.$axios.post("api/pdf", {
        data: this.content,
        name: this.pdfName,
        user_id: this.$auth.user.id,
        responseType: "arraybuffer"
      });
      if (process.browser) {
        const margins = {
          top: 70,
          bottom: 40,
          left: 30,
          width: 550
        };
        const jsPDF = require("jspdf");
        require("jspdf-autotable");
        var pdf = new jsPDF("p", "pt", "a4");
        // ... you code
        pdf.fromHTML(
          this.content,
          margins.left, // x coord
          margins.top,
          {
            // y coord
            width: margins.width // max width of content on PDF
          },
          function(dispose) {
            headerFooterFormatting(pdf);
          },
          margins
        );
        function headerFooterFormatting(doc) {
          var totalPages = doc.internal.getNumberOfPages();

          for (var i = totalPages; i >= 1; i--) {
            //make this page, the current page we are currently working on.
            doc.setPage(i);

            header(doc);

            footer(doc, i, totalPages);
          }
        }
        function footer(doc, pageNumber, totalPages) {
          var str = "Page " + pageNumber + " of " + totalPages;

          doc.setFontSize(10);
          doc.text(str, margins.left, doc.internal.pageSize.height - 20);
        }
        function header(doc) {
          doc.setFontSize(30);
          doc.setTextColor(40);
          doc.setFontStyle("normal");

          doc.text(vm.pdfName, margins.left + 50, 40);

          doc.line(3, 70, margins.width + 43, 70); // horizontal line
        }
        pdf.save(this.pdfName + ".pdf");
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@charset "UTF-8";
.container {
  width: 75%;
  margin: 0 auto;
  padding: 50px 0;
  .quill-editor {
    min-height: 600px;
    max-height: 800px;
    overflow-y: auto;
  }
}
</style>
