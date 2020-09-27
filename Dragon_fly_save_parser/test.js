var db;
var blob;
var request = indexedDB.open("/idbfs", 21.0);
request.onerror = function(event) {
  alert("Почему Вы не позволяете моему веб-приложению использовать IndexedDB?!");
};
request.onsuccess = function(event) {
  db = event.target.result;
};
var transaction = db.transaction(["FILE_DATA"], IDBTransaction.READ_WRITE);
blob = transaction.objectStore("FILE_DATA").get("/idbfs/6f26623f55fa25e22bbd6307a03ed441/PlayerPrefs");

var downloadBlob, downloadURL;

downloadBlob = function(data, fileName, mimeType) {
  var blob, url;
  blob = new Blob([data], {
    type: mimeType
  });
  url = window.URL.createObjectURL(blob);
  downloadURL(url, fileName);
  setTimeout(function() {
    return window.URL.revokeObjectURL(url);
  }, 1000);
};

downloadURL = function(data, fileName) {
  var a;
  a = document.createElement('a');
  a.href = data;
  a.download = fileName;
  document.body.appendChild(a);
  a.style = 'display: none';
  a.click();
  a.remove();
};

downloadBlob(blob.result.contents, 'some-file.bin', 'application/octet-stream');