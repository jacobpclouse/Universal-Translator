// access microphone to get input from user
// const player = document.getElementById('player');

// const handleSuccess = function (stream) {
//   if (window.URL) {
//     player.srcObject = stream;
//   } else {
//     player.src = stream;
//   }
// };

// navigator.mediaDevices
//   .getUserMedia({audio: true, video: false})
//   .then(handleSuccess);


// Stop and save data from the microphone
const startButton = document.getElementById('start');
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');


const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];  // this is where audio data will be stored -- can be made into a blob
  const mediaRecorder = new MediaRecorder(stream, options);

  // Event starts recording
  startButton.addEventListener('click', function() {
    mediaRecorder.start();
  });

  // Event makes sure that download is not empty
  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) recordedChunks.push(e.data);
  });

  // Event saves + downloads file
  mediaRecorder.addEventListener('stop', function() {
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    downloadLink.download = 'recordedAudio1.wav';
    const audioBlob = new Blob(recordedChunks, { type: "audio/wav" })

    const audioFile = new File(recordedChunks, "recordedAudio.wav")

    // // Send data to flask backend xhr
    // var xhr = new XMLHttpRequest();
    // var fd = new FormData();
    // fd.append("fileUpload0", audioBlob);

    // //fd.append("fileupload",URL.createObjectURL(new Blob(recordedChunks)))
    // fd.append("SourceLang", document.getElementById("sourceLang"));
    // fd.append("DestinationLang", document.getElementById("destinationLang"));

    // xhr.open("POST", "/");
    // xhr.send(fd);

    // ---- ----------------------------------

    // var data = new FormData()
    // data.append('file', audioBlob, 'file')

    // fetch('http://127.0.0.1:5000/', {

    //     method: 'POST',
    //     body: data

    // }).then(response => response.json()
    // ).then(json => {
    //     console.log(json)
    // });


   // ---- ----------------------------------


    var fd = new FormData();
    fd.append('fname', 'recordedAudio.wav');
    fd.append('data', audioBlob);
    $.ajax({
        type: 'POST',
        url: '/',
        data: fd,
        processData: false,
        contentType: 'audio/wav'
    }).done(function(data) {
          console.log(data);
    });



  });

  // Event stops recording
  stopButton.addEventListener('click', function() {
    mediaRecorder.stop();
  });

//   mediaRecorder.start();
};
// only want audio, not webcam
navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);





    //https://www.folkstalk.com/2022/09/upload-blob-to-server-with-code-examples.html