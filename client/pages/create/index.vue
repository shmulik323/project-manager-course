<template >
  <v-layout column>
    <v-text-field label="Project Name" box v-model="pdfName"></v-text-field>

    <v-layout align-center justify-center row fill-height>
      <v-flex xs12 sm2>
        <v-card>
          <v-btn id="spmp" @click="content=srs">SRS</v-btn>
          <v-btn id="srs" @click="content=spmp">PMP</v-btn>
          <v-card-title>
            <span class="title font-weight-dark">Load your prev project</span>
          </v-card-title>
          <v-sheet class="d-flex" color="grey lighten-3" height="600px" with="300px">
            <v-list>
              <div :key="pdf.name" v-for="pdf in pdfs">
                <v-btn @click="loadData(pdf)">{{pdf.name}}</v-btn>
                <v-btn @click="deletePdf(pdf.name)">
                  <v-icon class="material-icons">delete</v-icon>
                </v-btn>
              </div>
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
            <v-btn id="download_pdf" type="submit" @click="createPdf" target="_blank">Create PDF</v-btn>
            <v-btn id="save_pdf" type="submit" @click="savePdf">Save PDF</v-btn>
            <v-btn
              v-if="$auth.user.premium"
              id="send_pdf"
              type="submit"
              @click="sendPdf2Mail"
            >Send PDF</v-btn>
          </div>
        </section>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
import doc from "!raw-loader!../../assets/docx/doc.txt";
import doc1 from "!raw-loader!../../assets/docx/doc1.txt";
import hljs from "highlight.js";
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
      srs: doc,
      spmp: doc1,
      content: "",
      editorOption: {
        // some quill options
        modules: {
          toolbar: [
            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],
            [{ header: 1 }, { header: 2 }],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ script: "sub" }, { script: "super" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ direction: "rtl" }],
            [{ size: ["small", false, "large", "huge"] }],
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ font: [] }],
            [{ color: [] }, { background: [] }],
            [{ align: [] }],
            ["clean"],
            ["link", "image", "video"]
          ],
          syntax: {
            highlight: text => hljs.highlightAuto(text).value
          }
        },
        theme: "snow"
      },
      pdfName: "your Project name"
    };
  },
  async created() {
    getPdf: {
      await this.$axios.get("api/pdf", {}).then(res => {
        this.pdfs = res.data.pdfs;
      });
    }
  },
  methods: {
    onEditorBlur(editor) {},
    onEditorFocus(editor) {},
    onEditorReady(editor) {},
    onEditorChange({ editor, html, text }) {
      this.content = html;
    },
    loadData(data) {
      this.content = data.data;
      this.pdfName = data.name;
    },
    async sendPdf2Mail() {
      await this.$axios.post("api/pdfMail", {
        name: this.pdfName + ".pdf",
        mail: this.$auth.user.email,
        message: "here is your pdf"
      });
    },
    async reloadPdf() {
      await this.$axios.get("api/pdf", {}).then(res => {
        this.pdfs = res.data.pdfs;
      });
    },
    async savePdf() {
      await this.$axios
        .post("api/pdf", {
          data: this.content,
          name: this.pdfName,
          user_id: this.$auth.user.id,
          responseType: "arraybuffer"
        })
        .then(result => {
          this.reloadPdf();
        })
        .catch(err => {
          console.log(err);
          this.reloadPdf();
        });
    },
    async deletePdf(name) {
      await this.$axios.post("api/remove_pdf", {
        name: name
      });
      this.reloadPdf();
    },
    createPdf() {
      const vm = this;

      if (process.browser) {
        const margins = {
          top: 50,
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
