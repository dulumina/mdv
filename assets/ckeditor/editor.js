// Editor CKEditor 5 (UMD) dengan keluaran/masukan GitHub Flavored Markdown.
// Jembatan ke GTK: window.webkit.messageHandlers.mdv (didaftarkan Python),
// sedangkan Python memanggil window.mdv.setMarkdown / setDark.
(() => {
  const { ClassicEditor, Essentials, Autoformat, Heading, Bold, Italic, Underline,
    Strikethrough, Code, CodeBlock, BlockQuote, List, TodoList, Link, AutoLink,
    HorizontalLine, Table, TableToolbar, Image, ImageToolbar, ImageStyle, ImageCaption,
    ImageInsertViaUrl, ImageUpload, Base64UploadAdapter, RemoveFormat, SourceEditing,
    Markdown } = CKEDITOR;

  const PLUGINS = [Essentials, Autoformat, Heading, Bold, Italic, Underline,
    Strikethrough, Code, CodeBlock, BlockQuote, List, TodoList, Link, AutoLink,
    HorizontalLine, Table, TableToolbar, Image, ImageToolbar, ImageStyle, ImageCaption,
    ImageInsertViaUrl, ImageUpload, Base64UploadAdapter, RemoveFormat, SourceEditing,
    Markdown];

  const TOOLBAR = ['heading', '|', 'bold', 'italic', 'underline', 'strikethrough', 'code',
    '|', 'bulletedList', 'numberedList', 'todoList', '|', 'link', 'uploadImage',
    'insertTable', 'blockQuote', 'codeBlock', 'horizontalLine',
    '|', 'removeFormat', 'sourceEditing', '|', 'undo', 'redo'];

  let editor = null;
  let pending = '';
  let userTouched = false;   // interaksi manusia = perubahan boleh dikirim ke Python
  let lastSeen = null;
  let timer = null;

  if (location.hash === '#dark') document.body.classList.add('dark');

  const post = (obj) => {
    if (window.webkit && window.webkit.messageHandlers.mdv) {
      window.webkit.messageHandlers.mdv.postMessage(JSON.stringify(obj));
    }
  };

  window.mdv = {
    setMarkdown(md) {
      if (!editor) { pending = md; return; }
      userTouched = false;          // pantulan setData bukan suntingan pengguna
      editor.setData(md);
      lastSeen = editor.getData();  // normalisasi CKEditor bukan perubahan pengguna
    },
    setDark(dark) {
      document.body.classList.toggle('dark', !!dark);
    },
    // dipakai tes: mengubah data seperti pengguna mengetik
    simulateEdit(md) {
      userTouched = true;
      editor.setData(md);
    },
    roundTrip(md) {
      window.mdv.setMarkdown(md);
      return editor.getData();
    },
  };

  ClassicEditor
    .create(document.getElementById('editor'), {
      licenseKey: 'GPL',
      plugins: PLUGINS,
      toolbar: TOOLBAR,
      heading: {
        options: [
          { model: 'paragraph', title: 'Paragraf', class: 'ck-heading_paragraph' },
          { model: 'heading1', view: 'h1', title: 'Judul 1', class: 'ck-heading_heading1' },
          { model: 'heading2', view: 'h2', title: 'Judul 2', class: 'ck-heading_heading2' },
          { model: 'heading3', view: 'h3', title: 'Judul 3', class: 'ck-heading_heading3' },
          { model: 'heading4', view: 'h4', title: 'Judul 4', class: 'ck-heading_heading4' },
          { model: 'heading5', view: 'h5', title: 'Judul 5', class: 'ck-heading_heading5' },
          { model: 'heading6', view: 'h6', title: 'Judul 6', class: 'ck-heading_heading6' },
        ],
      },
    })
    .then((e) => {
      editor = e;
      // hanya interaksi manusia yang dikirim balik; setData programatik diabaikan
      document.addEventListener('keydown', () => { userTouched = true; }, true);
      document.addEventListener('mousedown', () => { userTouched = true; }, true);
      e.model.document.on('change:data', () => {
        if (!userTouched) return;
        const md = e.getData();
        if (md === lastSeen) return;
        lastSeen = md;
        clearTimeout(timer);
        timer = setTimeout(() => post({ md: md }), 250);
      });
      post({ ready: true });
      if (pending) window.mdv.setMarkdown(pending);
    })
    .catch((err) => {
      document.body.innerHTML = '<pre style="padding:16px;white-space:pre-wrap;color:#c00">'
        + 'CKEditor gagal dimuat:\n' + (err && (err.stack || err)) + '</pre>';
    });
})();
